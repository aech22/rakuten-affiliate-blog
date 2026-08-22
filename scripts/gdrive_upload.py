# scripts/gdrive_upload.py
# 投稿キット（social_kit.csv / pins/*.jpg / posts/*.txt）を Google Drive の指定フォルダへ反映する。
# 既存ファイルは書き換えない（下の【不変方針】を参照）。
# 生成そのものは別リポジトリ aech22/pinterest-kit が行う（2026-08-12〜。それ以前は
# scripts/gen_social_kit.py + gen_pins.py だったが、Pinterest運用仕様の 3バリアント化に
# 追随できず旧仕様のまま Drive へ上がり続けていたため退役させた）。
# 読み取り元は KIT_DIR で差し替えられる（既定 social/picknavi = pinterest-kit の PINKIT_OUT 配下）。
#
# 【不変方針 2026-08-22】一度Driveに置いた投稿文・投稿画像は二度と書き換えない。
# SNSは予約投稿・投稿済みの内容を後から差し替えられないため、Drive側だけが新しくなると
# 「手元の資産と実際に世に出た投稿が食い違う」状態になる。よって pins/*.jpg と 投稿文/*.txt は
# 新規作成のみ（既存名はスキップ）。social_kit.csv は索引なので消さずに済むよう、
# 既存行はそのまま残して新しい行だけ追記するマージ方式にする。
# 同じ理由で既定では削除もしない（KIT_PRUNE=1 のときだけ旧ファイルを掃除する）。
# 個人Gmail向けに「あなた自身のOAuth」で動く（ファイルはあなた所有＝あなたの容量を使う）。
# 4つの環境変数が未設定なら何もせず終了＝完全オプトイン。
from __future__ import annotations
import csv, io, os, sys
from pathlib import Path

# drive.file スコープ（アプリが作成したファイルのみ扱える最小権限）。
# アプリ自身が「picknavi_投稿キット」フォルダを作って管理するので、フォルダIDの登録は不要。
CREDS = ["GDRIVE_CLIENT_ID", "GDRIVE_CLIENT_SECRET", "GDRIVE_REFRESH_TOKEN"]
ROOT_FOLDER_NAME = "picknavi_投稿キット"
KIT_DIR = Path(os.environ.get("KIT_DIR") or "social/picknavi")

def main() -> None:
    if not all(os.environ.get(k) for k in CREDS):
        print("Google Drive の認証情報が未設定のためスキップ（オプトイン機能）")
        return
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload

    creds = Credentials(
        None,
        refresh_token=os.environ["GDRIVE_REFRESH_TOKEN"],
        client_id=os.environ["GDRIVE_CLIENT_ID"],
        client_secret=os.environ["GDRIVE_CLIENT_SECRET"],
        token_uri="https://oauth2.googleapis.com/token",
        scopes=["https://www.googleapis.com/auth/drive.file"],
    )
    svc = build("drive", "v3", credentials=creds)

    def find(name: str, parent: str | None, is_folder: bool = False):
        esc = name.replace("\\", "\\\\").replace("'", "\\'")
        q = f"name = '{esc}' and trashed = false"
        if parent:
            q += f" and '{parent}' in parents"
        if is_folder:
            q += " and mimeType = 'application/vnd.google-apps.folder'"
        res = svc.files().list(q=q, fields="files(id)", pageSize=1,
                               supportsAllDrives=True, includeItemsFromAllDrives=True).execute()
        files = res.get("files", [])
        return files[0]["id"] if files else None

    def ensure_folder(name: str, parent: str | None) -> str:
        fid = find(name, parent, is_folder=True)
        if fid:
            return fid
        meta = {"name": name, "mimeType": "application/vnd.google-apps.folder"}
        if parent:
            meta["parents"] = [parent]
        return svc.files().create(body=meta, fields="id", supportsAllDrives=True).execute()["id"]

    def prune_stale(folder_id: str, keep: set) -> None:
        """今回の生成に無いファイルを削除する。既定では走らない（KIT_PRUNE=1 のときだけ）。

        削除も「作ったあとに変える」操作の一種で、予約投稿に組み込み済みの素材を消しうる。
        旧ファイル名の掃除が必要になったときだけ、人が明示的に KIT_PRUNE=1 を付けて実行する。
        """
        if os.environ.get("KIT_PRUNE") != "1":
            return
        res = svc.files().list(q=f"'{folder_id}' in parents and trashed = false",
                               fields="files(id,name)", pageSize=1000,
                               supportsAllDrives=True, includeItemsFromAllDrives=True).execute()
        for f in res.get("files", []):
            if f["name"] not in keep:
                try:
                    svc.files().delete(fileId=f["id"], supportsAllDrives=True).execute()
                    print(f"deleted stale: {f['name']}")
                except Exception as e:
                    print(f"delete失敗 {f['name']}: {e}")

    # アプリ管理の保存先フォルダ（drive.file なのでアプリが作った物だけ見える＝重複作成を避けて再利用）
    folder = ensure_folder(ROOT_FOLDER_NAME, None)

    def create_only(path: Path, parent: str, mime: str) -> str:
        """同名が既にあれば何もしない。無いときだけ作る。

        戻り値は "created" / "kept"。既存を update しないのがこの関数の存在理由で、
        ここを upsert に戻すと投稿済みの素材が毎日書き換わる。
        """
        if find(path.name, parent):
            return "kept"
        media = MediaFileUpload(str(path), mimetype=mime, resumable=False)
        svc.files().create(body={"name": path.name, "parents": [parent]}, media_body=media,
                           fields="id", supportsAllDrives=True).execute()
        print(f"created: {path.name}")
        return "created"

    def merge_csv(local: Path, parent: str) -> None:
        """索引CSVを「既存行は据え置き・新規行だけ追記」でマージして置き直す。

        CSVはピンタイトルと説明文（＝投稿文そのもの）を持つので、全体を上書きすると
        投稿済みの文面が変わってしまう。かといって凍結すると新しいピンが索引に載らない。
        そこで画像ファイル名をキーに、既に載っている行は一字も変えずに残し、
        まだ無い行だけを足す。生成されなくなった行も消さずに末尾へ送る。
        """
        KEY = "画像ファイル"
        with local.open(encoding="utf-8-sig", newline="") as f:
            new_rows = list(csv.DictReader(f))
        if not new_rows:
            print("csv: 新規生成が空のため据え置き")
            return
        header = list(new_rows[0].keys())

        fid = find(local.name, parent)
        old_rows: list[dict] = []
        if fid:
            try:
                raw = svc.files().get_media(fileId=fid).execute()
                old_rows = list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig"))))
            except Exception as e:
                # 読めないときに上書きすると既存の文面を失う。安全側に倒して中止する。
                print(f"csv: 既存の読み取りに失敗したため更新を見送る: {e}")
                return

        def keyof(r: dict) -> str:
            return (r.get(KEY) or "").strip()

        merged: list[dict] = []
        seen: set[str] = set()
        old_by_key = {keyof(r): r for r in old_rows if keyof(r)}
        for r in new_rows:
            k = keyof(r)
            prev = old_by_key.get(k)
            if prev:
                # 既存行は文面をそのまま維持する。新しく増えた列だけ新値で埋める。
                merged.append({c: (prev[c] if c in prev else r.get(c, "")) for c in header})
            else:
                merged.append({c: r.get(c, "") for c in header})
            seen.add(k)
        # 今回生成されなかった過去の行も落とさずに残す
        kept_old = [r for k, r in old_by_key.items() if k not in seen]
        for r in kept_old:
            merged.append({c: r.get(c, "") for c in header})

        buf = io.StringIO()
        w = csv.DictWriter(buf, fieldnames=header)
        w.writeheader()
        w.writerows(merged)
        tmp = local.parent / "_merged_social_kit.csv"
        tmp.write_text(buf.getvalue(), encoding="utf-8-sig")

        media = MediaFileUpload(str(tmp), mimetype="text/csv", resumable=False)
        if fid:
            svc.files().update(fileId=fid, media_body=media, supportsAllDrives=True).execute()
        else:
            svc.files().create(body={"name": local.name, "parents": [parent]}, media_body=media,
                               fields="id", supportsAllDrives=True).execute()
        print(f"csv: 既存 {len(old_by_key)} 行を据え置き / 新規 {len(merged) - len(old_by_key)} 行を追記 / "
              f"生成対象外で残した行 {len(kept_old)}")

    csv_path = KIT_DIR / "social_kit.csv"
    if csv_path.exists():
        merge_csv(csv_path, folder)

    pins_dir = KIT_DIR / "pins"
    if pins_dir.exists():
        pins_folder = ensure_folder("pins", folder)
        names, created = set(), 0
        for img in sorted(pins_dir.glob("*.jpg")):
            if create_only(img, pins_folder, "image/jpeg") == "created":
                created += 1
            names.add(img.name)
        prune_stale(pins_folder, names)
        print(f"pins: 新規 {created} / 既存据え置き {len(names) - created} / 生成 {len(names)}")

    posts_dir = KIT_DIR / "posts"
    if posts_dir.exists():
        posts_folder = ensure_folder("投稿文", folder)
        names, created = set(), 0
        for txt in sorted(posts_dir.glob("*.txt")):
            if create_only(txt, posts_folder, "text/plain") == "created":
                created += 1
            names.add(txt.name)
        prune_stale(posts_folder, names)
        print(f"posts: 新規 {created} / 既存据え置き {len(names) - created} / 生成 {len(names)}")
    print("done")

if __name__ == "__main__":
    main()

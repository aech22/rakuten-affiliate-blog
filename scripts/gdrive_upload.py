# scripts/gdrive_upload.py
# 投稿キット（social/social_kit.csv と social/pins/*.jpg）を Google Drive の指定フォルダへ upsert する。
# 個人Gmail向けに「あなた自身のOAuth」で動く（ファイルはあなた所有＝あなたの容量を使う）。
# 4つの環境変数が未設定なら何もせず終了＝完全オプトイン。
from __future__ import annotations
import os, sys
from pathlib import Path

# drive.file スコープ（アプリが作成したファイルのみ扱える最小権限）。
# アプリ自身が「picknavi_投稿キット」フォルダを作って管理するので、フォルダIDの登録は不要。
CREDS = ["GDRIVE_CLIENT_ID", "GDRIVE_CLIENT_SECRET", "GDRIVE_REFRESH_TOKEN"]
ROOT_FOLDER_NAME = "picknavi_投稿キット"

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
        """フォルダ内の、今回アップロードした集合に無いファイルを削除（旧ファイル名の掃除・トピック削除対応）。"""
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

    def upsert(path: Path, parent: str, mime: str) -> None:
        media = MediaFileUpload(str(path), mimetype=mime, resumable=False)
        fid = find(path.name, parent)
        if fid:
            svc.files().update(fileId=fid, media_body=media, supportsAllDrives=True).execute()
            print(f"updated: {path.name}")
        else:
            svc.files().create(body={"name": path.name, "parents": [parent]}, media_body=media,
                               fields="id", supportsAllDrives=True).execute()
            print(f"created: {path.name}")

    csv_path = Path("social/social_kit.csv")
    if csv_path.exists():
        upsert(csv_path, folder, "text/csv")

    pins_dir = Path("social/pins")
    if pins_dir.exists():
        pins_folder = ensure_folder("pins", folder)
        names = set()
        for img in sorted(pins_dir.glob("*.jpg")):
            upsert(img, pins_folder, "image/jpeg")
            names.add(img.name)
        prune_stale(pins_folder, names)
        print(f"pins uploaded: {len(names)}")

    posts_dir = Path("social/posts")
    if posts_dir.exists():
        posts_folder = ensure_folder("投稿文", folder)
        names = set()
        for txt in sorted(posts_dir.glob("*.txt")):
            upsert(txt, posts_folder, "text/plain")
            names.add(txt.name)
        prune_stale(posts_folder, names)
        print(f"posts uploaded: {len(names)}")
    print("done")

if __name__ == "__main__":
    main()

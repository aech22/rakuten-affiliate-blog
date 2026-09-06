# scripts/quality_check.py — 公開前の機械ゲート。CLI: python scripts/quality_check.py content/articles
# 新フォーマット（frontmatterに products 配列と講評文を持つ）に対応。
# 不合格が1件でもあれば非ゼロ終了で workflow を止める＝低品質記事を公開しない。
import sys
from pathlib import Path
import yaml

MIN_PROSE_CHARS = 450                       # intro+outro+各商品の講評 の合計下限（4商品比較の実測下限に合わせる）
AFFILIATE_HOST = "hb.afl.rakuten.co.jp"

# ── 表現ゲート（2026-09-06 追加）──────────────────────────────────
#
# ★なぜ「商材の分類」ではなく「表現」で切るのか
#   アフィリエイトサイトは販売しないので、販売に必要な資格（登録販売者・酒類販売業免許・
#   古物商）は一つもこちらに掛からない。掛かるのは広告表現の側で、薬機法66条・
#   健康増進法65条・景表法はいずれも「その商品が何か」ではなく「何と書いたか」で判定される。
#   プロテインは販売資格が不要だが「疲労回復に効く」と書けば抵触しうる。
#   だから fitness / beauty カテゴリは残し、代わりにここで表現を弾く。
#   出典: 2026-09-06 のユーザー決定（プロテインを許可し、判断軸を表現へ移す）。
#
# ★選語の方針
#   偽陽性で全記事が落ちると誰も直さなくなるので、日常語と衝突する語は入れない。
#   「改善」「回復」単体は収納・家電の講評で普通に使うため、効能の主張になる形でだけ拾う。
EXPRESSION_RULES = {
    "景表法": ["最安値", "絶対", "No.1", "ｎｏ.1", "日本一", "業界最安", "完全無料"],
    "薬機法": [
        "治る", "治す", "完治", "疾患",
        "症状が改善", "体質が改善", "症状を改善",
        "予防できます", "予防効果",
        "痩せます", "痩せられます", "脂肪が燃焼", "脂肪燃焼",
        "デトックス", "免疫力が上がる", "免疫力アップ",
        "血行が良くなる", "代謝が上がる", "疲労回復",
        "育毛", "発毛", "アンチエイジング", "老化を防ぐ",
        "シミが消える", "シワが消える",
    ],
    "健康増進法": ["飲むだけで", "食べるだけで", "誰でも痩せ", "医師推奨", "医師も推奨", "医師も認め"],
}

# 表現ゲートでは守れない商材。効能効果が承認事項なので、触れること自体がリスクになる。
# ここだけは「販売に資格が要るもの」という線引きとほぼ一致する。
#
# ⚠️ 「医薬部外品」を入れてはいけない。薬用化粧水・薬用美容液・制汗剤など
#    普通に売られている化粧品の表示で、楽天の商品名にそのまま入っている。
#    初回実装で入れたところ、公開済み61本のうち3本（makeup-primer・美容液・化粧水）が
#    誤検出で落ちた（2026-09-06 実測）。医薬部外品で本当に危ないのは
#    「承認範囲を超えた効能を書くこと」なので、それは上の薬機法の表現リストが受け持つ。
PROHIBITED_GOODS = ["医薬品", "処方薬", "医療機器", "コンタクトレンズ", "カラコン"]


def expression_violations(text: str) -> list:
    """編集文に含まれる禁止表現を「法令: 語」の形で返す。空リストなら合格。"""
    out = []
    for law, words in EXPRESSION_RULES.items():
        hit = [w for w in words if w in text]
        if hit:
            out.append(f"{law}: " + ", ".join(hit))
    return out

def _prose_text(fm: dict) -> str:
    parts = [fm.get("intro", ""), fm.get("outro", "")]
    for p in fm.get("products", []) or []:
        parts += (p.get("pros") or [])
        parts += [p.get("cons", ""), p.get("target", "")]
    for g in fm.get("guide", []) or []:
        parts += [g.get("point", ""), g.get("desc", "")]
    for q in fm.get("faqs", []) or []:
        parts += [q.get("q", ""), q.get("a", "")]
    return " ".join(x for x in parts if x).strip()

def check(md: str) -> list:
    errors = []
    if not md.startswith("---"):
        return ["frontmatter が無い"]
    try:
        fm = yaml.safe_load(md.split("---", 2)[1]) or {}
    except Exception as e:
        return [f"frontmatter を YAML として解釈できない: {e}"]

    if not fm.get("title") or not fm.get("date"):
        errors.append("frontmatter に title / date が無い")

    if not fm.get("categorySlug"):
        errors.append("categorySlug が無い")
    if fm.get("gender") not in ("men", "women", "unisex"):
        errors.append(f"gender が不正（{fm.get('gender')!r}）")

    products = fm.get("products") or []
    if not products:
        errors.append("products が空")

    if not any(AFFILIATE_HOST in (p.get("url") or "") for p in products):
        errors.append(f"アフィリンク（{AFFILIATE_HOST}）が無い")

    noimg = [str(p.get("name", "?"))[:16] for p in products if not p.get("image")]
    if noimg:
        errors.append("商品画像が無い: " + ", ".join(noimg))

    prose = _prose_text(fm)
    if len(prose) < MIN_PROSE_CHARS:
        errors.append(f"講評文が短すぎる（{len(prose)}字 < {MIN_PROSE_CHARS}）")

    # 禁止語は「自社の編集文（タイトル＋講評）」だけを対象にする。
    # 商品名は楽天の実データ（例: 商品名に「No.1」を含む）で、こちらが変更できず事実表記なので対象外。
    editorial = (fm.get("title", "") or "") + " " + prose
    errors.extend(expression_violations(editorial))

    # 扱わない商材。こちらはタイトルと商品名の両方を見る
    # （楽天から医薬品・医療機器が混ざって返ってきたら、講評を書かせる前に落とす）。
    goods = editorial + " " + " ".join(str(p.get("name", "")) for p in products)
    bad_goods = [w for w in PROHIBITED_GOODS if w in goods]
    if bad_goods:
        errors.append("扱わない商材を含む: " + ", ".join(bad_goods))
    return errors

def main(dir_path: str, prune: bool = False) -> None:
    """prune=False（ローカル/既定）: NGが1件でもあれば非ゼロ終了。
       prune=True（日次workflow）: NG記事だけ除外して他は公開し、全滅時のみ失敗。
       →1記事の講評が短い等でサイト全体の公開が止まるのを防ぐ。"""
    files = sorted(Path(dir_path).glob("*.md"))
    if not files:
        print(f"[WARN] {dir_path} に記事がありません")
    ok_count, ng = 0, []
    for path in files:
        errors = check(path.read_text(encoding="utf-8"))
        if errors:
            ng.append(path)
            print(f"[NG] {path.name}: {'; '.join(errors)}")
        else:
            ok_count += 1
            print(f"[OK] {path.name}")

    if prune:
        for path in ng:
            path.unlink()
            print(f"[PRUNED] {path.name} を今回の公開から除外（次回再生成で再挑戦）")
        if ok_count == 0:
            print("[FATAL] 公開可能な記事が0件のため中止")
            sys.exit(1)
        return
    if ng:
        sys.exit(1)   # 非ゼロ終了で workflow を止める（厳格モード）

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    prune = "--prune" in sys.argv
    main(args[0] if args else "content/articles", prune=prune)

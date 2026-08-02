# scripts/quality_check.py — 公開前の機械ゲート。CLI: python scripts/quality_check.py content/articles
# 新フォーマット（frontmatterに products 配列と講評文を持つ）に対応。
# 不合格が1件でもあれば非ゼロ終了で workflow を止める＝低品質記事を公開しない。
import sys
from pathlib import Path
import yaml

MIN_PROSE_CHARS = 600                       # intro+outro+各商品の講評 の合計下限
BANNED = ["最安値", "絶対", "No.1", "ｎｏ.1", "日本一", "業界最安", "完全無料"]
AFFILIATE_HOST = "hb.afl.rakuten.co.jp"

def _prose_text(fm: dict) -> str:
    parts = [fm.get("intro", ""), fm.get("outro", "")]
    for p in fm.get("products", []) or []:
        parts += (p.get("pros") or [])
        parts += [p.get("cons", ""), p.get("target", "")]
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

    hit = [w for w in BANNED if w in md]
    if hit:
        errors.append("禁止語を含む: " + ", ".join(hit))
    return errors

def main(dir_path: str) -> None:
    failed = False
    files = sorted(Path(dir_path).glob("*.md"))
    if not files:
        print(f"[WARN] {dir_path} に記事がありません")
    for path in files:
        errors = check(path.read_text(encoding="utf-8"))
        if errors:
            failed = True
            print(f"[NG] {path.name}: {'; '.join(errors)}")
        else:
            print(f"[OK] {path.name}")
    if failed:
        sys.exit(1)   # 非ゼロ終了で workflow を止める（＝公開しない）

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "content/articles")

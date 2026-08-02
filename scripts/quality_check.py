# scripts/quality_check.py — 公開前の機械ゲート。CLI: python scripts/quality_check.py content/articles
import re, sys
from pathlib import Path

MIN_CHARS = 800
BANNED = ["最安値", "絶対", "No.1", "ｎｏ.1", "日本一", "業界最安", "完全無料"]

def check(md: str) -> list:
    errors = []
    body = re.sub(r"^---.*?---", "", md, count=1, flags=re.S)  # frontmatter除外
    if len(body.strip()) < MIN_CHARS:
        errors.append(f"本文が短すぎる（{len(body.strip())}字 < {MIN_CHARS}）")
    if "hb.afl.rakuten.co.jp" not in md:
        errors.append("アフィリンク（affiliateUrl）が無い")
    fm = md.split("---")[1] if md.startswith("---") else ""
    if "title" not in fm or "date" not in fm:
        errors.append("frontmatter に title / date が無い")
    hit = [w for w in BANNED if w in md]
    if hit:
        errors.append(f"禁止語を含む: {', '.join(hit)}")
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

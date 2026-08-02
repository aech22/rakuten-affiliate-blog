# scripts/main.py — エントリーポイント（リポジトリルートから `python scripts/main.py`）
import datetime, os, sys
from pathlib import Path

# どのCWDから実行しても scripts/ 内の同階層モジュールを import できるようにする
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import TOPICS
from fetch_products import fetch_products      # 内部で 1req/秒 のレート制御
from generate_article import generate_article

# 出力先は常にリポジトリルート直下の content/articles（scripts の1つ上）
OUT_DIR = Path(__file__).resolve().parent.parent / "content" / "articles"

def slugify(theme: str) -> str:
    return "".join(c if c.isalnum() else "-" for c in theme).strip("-").lower()[:50]

def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.date.today().isoformat()
    for topic in TOPICS:
        products = fetch_products(topic["keyword"], topic["hits"])  # sleep はこの中
        md = generate_article(products, topic["theme"])
        path = OUT_DIR / f"{today}-{slugify(topic['theme'])}.md"
        path.write_text(md, encoding="utf-8")
        print(f"generated -> {path}")

if __name__ == "__main__":
    main()

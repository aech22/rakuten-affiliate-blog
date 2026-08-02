# scripts/main.py — エントリーポイント（workflow の `python scripts/main.py`）
import datetime
from pathlib import Path

from config import TOPICS
from fetch_products import fetch_products      # 内部で 1req/秒 のレート制御
from generate_article import generate_article

OUT_DIR = Path("content/articles")

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

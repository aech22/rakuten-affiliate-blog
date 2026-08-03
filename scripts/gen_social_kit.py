# scripts/gen_social_kit.py
# 各記事から「手動投稿用キット」を1つのCSVに書き出す。
# 列: カテゴリ / タイトル / 記事URL / ピンタイトル / ピン説明文 / X投稿文 / 画像URL
# Pinterest・X に手動投稿するとき、この表からコピペするだけで済むようにする。
from __future__ import annotations
import csv, sys
from pathlib import Path
import yaml

SITE = "https://picknavi.net"
ART_DIR = Path(__file__).resolve().parent.parent / "content" / "articles"

def x_text(title: str, cat: str, url: str) -> str:
    tag = f"【{cat}】" if cat else ""
    body = f"{tag}{title}\n楽天で売れている商品を写真・価格・レビューで比較👇\n{url}\n#おすすめ #比較"
    return body[:275]

def main(out_path: str) -> None:
    rows = []
    for p in sorted(ART_DIR.glob("*.md")):
        try:
            fm = yaml.safe_load(p.read_text(encoding="utf-8").split("---", 2)[1]) or {}
        except Exception:
            continue
        slug = p.stem
        title = fm.get("title", slug)
        desc = fm.get("description", "") or ""
        cat = fm.get("category", "") or ""
        url = f"{SITE}/articles/{slug}/"
        products = fm.get("products") or []
        image = (products[0] or {}).get("image", "") if products else ""
        pin_desc = f"{title}｜{desc}" if desc else f"{title}｜picknavi"
        rows.append({
            "カテゴリ": cat,
            "タイトル": title,
            "記事URL": url,
            "ピンタイトル": title[:100],
            "ピン説明文": pin_desc[:490],
            "X投稿文": x_text(title, cat, url),
            "画像URL": image,
        })
    fields = ["カテゴリ", "タイトル", "記事URL", "ピンタイトル", "ピン説明文", "X投稿文", "画像URL"]
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)   # social/ が無い場合に作る
    with open(out_path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {len(rows)} rows -> {out_path}")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "social_kit.csv")

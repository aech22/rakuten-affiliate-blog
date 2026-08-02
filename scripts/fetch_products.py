# scripts/fetch_products.py
import argparse, json, os, time
import requests

RAKUTEN_APP_ID = os.environ["RAKUTEN_APP_ID"]
AFFILIATE_ID   = os.environ["RAKUTEN_AFFILIATE_ID"]

# 楽天API制限（1秒1リクエスト）を守るための最小間隔。
# 複数キーワードを回すときはこの sleep でスロットリングする。
RATE_LIMIT_SEC = 1.0

def fetch_products(keyword: str, hits: int = 5) -> list:
    url = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20220601"
    params = {
        "applicationId": RAKUTEN_APP_ID,
        "affiliateId":   AFFILIATE_ID,   # これを付けると affiliateUrl が返る
        "keyword":       keyword,
        "hits":          hits,
        "sort":          "-reviewCount",  # レビュー数降順
        "imageFlag":     1,
    }
    res = requests.get(url, params=params)
    res.raise_for_status()
    time.sleep(RATE_LIMIT_SEC)            # レート制御（1req/秒）
    items = res.json()["Items"]
    return [item["Item"] for item in items]

# CLI: python scripts/fetch_products.py --keyword "..." --hits 3 --output products.json
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--keyword", required=True)
    ap.add_argument("--hits", type=int, default=5)
    ap.add_argument("--output", default="products.json")
    args = ap.parse_args()

    products = fetch_products(args.keyword, args.hits)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=2)
    print(f"wrote {len(products)} products -> {args.output}")

# scripts/fetch_products.py
import argparse, json, os, time
import requests

RAKUTEN_APP_ID     = os.environ["RAKUTEN_APP_ID"]
RAKUTEN_ACCESS_KEY = os.environ["RAKUTEN_ACCESS_KEY"]
AFFILIATE_ID       = os.environ["RAKUTEN_AFFILIATE_ID"]

# 新コンソール(Rakuten Developers)発行の UUID Application ID + Access Key に対応した
# 新エンドポイント(2026-07-01)。旧 app.rakuten.co.jp/services/api/...20220601 は
# UUID の applicationId を受け付けない（wrong_parameter）ため使わない。
ENDPOINT = "https://openapi.rakuten.co.jp/ichibams/api/IchibaItem/Search/20260701"

# 楽天API制限（1秒1リクエスト）を守るための最小間隔。
RATE_LIMIT_SEC = 1.0

def fetch_products(keyword: str, hits: int = 5) -> list:
    params = {
        "applicationId": RAKUTEN_APP_ID,
        "accessKey":     RAKUTEN_ACCESS_KEY,   # 新方式で必須（クエリ or ヘッダ）
        "affiliateId":   AFFILIATE_ID,         # 付けると affiliateUrl が返る
        "keyword":       keyword,
        "hits":          hits,
        "sort":          "-reviewCount",        # レビュー数降順（人気順）
        "imageFlag":     1,
        "formatVersion": 2,                     # items[] の各要素が商品dict直下になる新形式
    }
    res = requests.get(ENDPOINT, params=params)
    res.raise_for_status()
    time.sleep(RATE_LIMIT_SEC)                  # レート制御（1req/秒）
    # formatVersion=2: {"items": [ {itemName, itemPrice, affiliateUrl, mediumImageUrls, ...}, ... ]}
    return res.json()["items"]

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

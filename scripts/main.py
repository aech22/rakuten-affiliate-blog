# scripts/main.py — エントリーポイント（リポジトリルートから `python scripts/main.py`）
from __future__ import annotations
import datetime, os, sys
from pathlib import Path

# どのCWDから実行しても scripts/ 内の同階層モジュールを import できるようにする
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import yaml
from config import TOPICS, TOPIC_POOL, CATEGORIES, DAILY_NEW_LIMIT
from fetch_products import fetch_products          # 内部で 1req/秒 のレート制御
from generate_article import build_article, to_markdown

# 日付は日本時間(JST)で確定する（GitHub ActionsはUTCで動くため、指定しないと日付が1日ずれる）
JST = datetime.timezone(datetime.timedelta(hours=9))

# 出力先は常にリポジトリルート直下の content/articles（scripts の1つ上）
OUT_DIR = Path(__file__).resolve().parent.parent / "content" / "articles"

def slugify(theme: str) -> str:
    # 日本語は isalnum()=True のため保持される。URLは固定（トピック単位・日付を含めない＝重複コンテンツ回避）。
    return "".join(c if c.isalnum() else "-" for c in theme).strip("-")[:60]

def _existing_publish_date(path: Path) -> str | None:
    """既存記事があれば公開日(date)を引き継ぐ（固定URLで公開日を安定させSEO評価を維持）。"""
    if not path.exists():
        return None
    try:
        fm = yaml.safe_load(path.read_text(encoding="utf-8").split("---", 2)[1]) or {}
        d = fm.get("date")
        return d.isoformat() if hasattr(d, "isoformat") else (str(d) if d else None)
    except Exception:
        return None

def gen_one(topic: dict, today: str) -> Path | None:
    cat_slug = topic["cat"]
    cat = CATEGORIES.get(cat_slug, {})
    label = cat.get("label", cat_slug)
    gender = cat.get("gender", "unisex")
    products = fetch_products(topic["keyword"], topic["hits"])   # sleep はこの中
    if not products:
        print(f"[SKIP] {topic['theme']}: 商品が0件")
        return None
    path = OUT_DIR / f"{slugify(topic['theme'])}.md"
    publish_date = _existing_publish_date(path) or today          # 初回のみ today、以降は維持
    fm = build_article(products, topic["theme"], publish_date, label,
                       category_slug=cat_slug, gender=gender, updated_str=today)
    path.write_text(to_markdown(fm), encoding="utf-8")
    return path

def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.datetime.now(JST).date().isoformat()
    refreshed, added = 0, 0
    new_budget = DAILY_NEW_LIMIT                                   # 本日追加できる新規記事の残数

    # 公開済み(TOPICS)は毎日すべて更新。TOPIC_POOL の未公開分は 1日 DAILY_NEW_LIMIT 本だけ追加。
    for topic in list(TOPICS) + list(TOPIC_POOL):
        path = OUT_DIR / f"{slugify(topic['theme'])}.md"
        is_new = not path.exists()
        if is_new and new_budget <= 0:
            continue                                              # 本日の新規上限に到達→次回以降に回す
        try:
            written = gen_one(topic, today)
            if not written:
                continue
            if is_new:
                added += 1
                new_budget -= 1
                print(f"added(new) -> {written.name}")
            else:
                refreshed += 1
                print(f"generated -> {written.name}")
        except Exception as e:
            # 1テーマ失敗しても他を継続（日次ジョブを止めない）。原因は簡潔に表示。
            print(f"[SKIP] {topic['theme']}: {type(e).__name__}: {e}")

    print(f"done: 更新{refreshed}本・新規追加{added}本（本日上限{DAILY_NEW_LIMIT}）")

if __name__ == "__main__":
    main()

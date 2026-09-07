# scripts/main.py — エントリーポイント（リポジトリルートから `python scripts/main.py`）
from __future__ import annotations
import datetime, os, sys
from pathlib import Path

# どのCWDから実行しても scripts/ 内の同階層モジュールを import できるようにする
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import yaml
from config import TOPICS, TOPIC_POOL, CATEGORIES, DAILY_NEW_LIMIT
from fetch_products import fetch_products          # 内部で 1req/秒 のレート制御
from generate_article import build_article, rebuild_article, reusable_prose, to_markdown

# 日付は日本時間(JST)で確定する（GitHub ActionsはUTCで動くため、指定しないと日付が1日ずれる）
JST = datetime.timezone(datetime.timedelta(hours=9))

# 出力先は常にリポジトリルート直下の content/articles（scripts の1つ上）
OUT_DIR = Path(__file__).resolve().parent.parent / "content" / "articles"

# FORCE_PROSE=1 で「商品が入れ替わっていないから講評文は据え置き」の最適化を無効にする。
# 生成プロンプト（SYSTEM_PROMPT）の文体ルールを変えても、通常運転では商品が変わらない記事の
# 講評文が古い文体のまま残り続ける。文体の基準を変えたときに既存記事を追随させるための入口。
# 全記事でLLMを呼ぶので日次運転では使わない（workflow の force_prose 入力から手動でのみ渡す）。
FORCE_PROSE = os.environ.get("FORCE_PROSE", "").lower() in ("1", "true", "yes")

def legacy_slugify(theme: str) -> str:
    # 2026-08-31 まで使っていた採番。日本語は isalnum()=True のため保持され、URLではパーセント
    # エンコードされる。この関数は「既にこの名前で公開されている記事」を見つけるためだけに残す。
    return "".join(c if c.isalnum() else "-" for c in theme).strip("-")[:60]

def article_path(topic: dict) -> Path:
    """記事ファイルのパスを決める。ファイル名がそのまま記事URLのスラッグになる。

    公開済み記事のURLは変えない（変えると被リンクとインデックスを捨てることになる）ので、
    日本語スラッグのファイルが既にあるならそれを使い続ける。無ければ config.py の
    英数 slug で作る。結果として**次に新規生成される記事から英数URLに切り替わる**。
    """
    legacy = OUT_DIR / f"{legacy_slugify(topic['theme'])}.md"
    if legacy.exists():
        return legacy
    slug = topic.get("slug")
    if not slug:
        # config.py の assert で弾かれるはずだが、日次ジョブを落とさないための保険。
        print(f"[WARN] slug 未設定のため日本語スラッグで作成します: {topic['theme']}")
        return legacy
    return OUT_DIR / f"{slug}.md"

def _existing_frontmatter(path: Path) -> dict | None:
    """既存記事の frontmatter を読む（無い・壊れている場合は None）。"""
    if not path.exists():
        return None
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8").split("---", 2)[1]) or {}
    except Exception:
        return None

def _publish_date(prev: dict | None) -> str | None:
    """既存記事があれば公開日(date)を引き継ぐ（固定URLで公開日を安定させSEO評価を維持）。"""
    d = (prev or {}).get("date")
    return d.isoformat() if hasattr(d, "isoformat") else (str(d) if d else None)

def gen_one(topic: dict, today: str) -> tuple[Path | None, bool]:
    """記事を1本書き出す。戻り値は (パス, LLMを呼ばずに事実だけ更新したか)。"""
    cat_slug = topic["cat"]
    cat = CATEGORIES.get(cat_slug, {})
    label = cat.get("label", cat_slug)
    gender = cat.get("gender", "unisex")
    products = fetch_products(topic["keyword"], topic["hits"])   # sleep はこの中
    if not products:
        print(f"[SKIP] {topic['theme']}: 商品が0件")
        return None, False
    path = article_path(topic)
    prev = _existing_frontmatter(path)
    publish_date = _publish_date(prev) or today                   # 初回のみ today、以降は維持
    reused = reusable_prose(products, prev) and not FORCE_PROSE
    if reused:
        # 商品が1件も入れ替わっていない → 講評文は据え置き、価格・レビューだけ最新にする
        fm = rebuild_article(products, prev, publish_date, label,
                             category_slug=cat_slug, gender=gender, updated_str=today)
    else:
        fm = build_article(products, topic["theme"], publish_date, label,
                           category_slug=cat_slug, gender=gender, updated_str=today)
    path.write_text(to_markdown(fm), encoding="utf-8")
    return path, reused

def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.datetime.now(JST).date().isoformat()
    refreshed, added, facts_only = 0, 0, 0
    new_budget = DAILY_NEW_LIMIT                                   # 本日追加できる新規記事の残数

    # 公開済み(TOPICS)は毎日すべて更新。TOPIC_POOL の未公開分は 1日 DAILY_NEW_LIMIT 本だけ追加。
    for topic in list(TOPICS) + list(TOPIC_POOL):
        path = article_path(topic)
        is_new = not path.exists()
        if is_new and new_budget <= 0:
            continue                                              # 本日の新規上限に到達→次回以降に回す
        try:
            written, reused = gen_one(topic, today)
            if not written:
                continue                                          # 商品0件。枠は消費せず次のトピックへ
            if is_new:
                added += 1
                new_budget -= 1
                print(f"added(new) -> {written.name}")
            else:
                refreshed += 1
                if reused:
                    facts_only += 1
                print(f"{'facts-only' if reused else 'generated'} -> {written.name}")
        except Exception as e:
            # 1テーマ失敗しても他を継続（日次ジョブを止めない）。原因は簡潔に表示。
            # 新規は失敗しても枠を消費する。減らさないと、生成が落ちている日に
            # TOPIC_POOL 全件へ順に手を出してしまう（2026-08-11〜16 は毎日78件試していた）。
            if is_new:
                new_budget -= 1
            print(f"[SKIP] {topic['theme']}: {type(e).__name__}: {e}")

    llm_calls = refreshed - facts_only + added
    print(f"done: 更新{refreshed}本（うちLLM未呼び出し{facts_only}本）・新規追加{added}本"
          f"（本日上限{DAILY_NEW_LIMIT}）／LLM呼び出し{llm_calls}回")

if __name__ == "__main__":
    main()

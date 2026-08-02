# scripts/generate_article.py
import argparse, json
import anthropic

client = anthropic.Anthropic()

SYSTEM_PROMPT = """
あなたはアフィリエイトブログの記事ライターです。
以下のルールで記事を書いてください:
- 読者目線で正直なレビュー風に書く
- 商品の特徴を具体的に3つ挙げる
- 価格帯と対象ユーザーを明記する
- 誇大表現・根拠のない最上級表現は使わない（楽天規約準拠）
- 出力形式: Markdownのみ（frontmatterを含む。title と date を必須で入れる）
- 重要: コードフェンス（```）で囲まないこと。1文字目を frontmatter の `---` から始め、前置きや後書きを付けない

frontmatter の形式（先頭に必ず付ける）:
---
title: "記事タイトル"
date: 2026-08-02
description: "記事の要約（100字程度）"
---
"""

def _clean_markdown(md: str) -> str:
    """LLMが付けがちな ```markdown 囲みや前置きを除去し、frontmatterの --- から始める。"""
    md = md.strip()
    if md.startswith("```"):
        nl = md.find("\n")
        md = md[nl + 1:] if nl != -1 else md      # 先頭の ```lang 行を落とす
        md = md.rstrip()
        if md.endswith("```"):
            md = md[:-3].rstrip()                  # 末尾の ``` を落とす
    if not md.startswith("---"):                   # 前置きがあれば最初の --- から
        i = md.find("---")
        if i != -1:
            md = md[i:]
    return md.strip() + "\n"

def generate_article(products: list, theme: str) -> str:
    product_json = json.dumps(products[:3], ensure_ascii=False, indent=2)

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",  # コスト最適化
        max_tokens=2048,
        system=SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": f"""
テーマ: {theme}
以下の商品データを元に、比較記事を生成してください。
affiliateUrlをそのままリンクに使用してください。

{product_json}
"""
        }]
    )
    return _clean_markdown(message.content[0].text)

# CLI: python scripts/generate_article.py --input products.json --theme "..." --output content/articles/test.md
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="fetch_products.py が出力した products.json")
    ap.add_argument("--theme", default="おすすめ商品比較")
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    with open(args.input, encoding="utf-8") as f:
        products = json.load(f)
    md = generate_article(products, args.theme)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"wrote article -> {args.output}")

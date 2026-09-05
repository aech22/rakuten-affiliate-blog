# CLAUDE.md — picknavi

**⚠️ 作業前に共通正本を必ず読むこと:**
`/Users/hiroshi/Documents/Obsidian Vault/Projects/アフィリエイト/AFFILIATE.md`

技術スタック・デプロイ手順・禁止事項（A8のURLを開かない／株式会社を名乗らない等）・ハマりどころは全て共通正本にある。このファイルには**picknavi 固有の情報だけ**を書く。

---

## サイト固有情報

| 項目 | 内容 |
|---|---|
| ブランド | picknavi |
| 本番URL | https://picknavi.net（独自ドメイン・ルート配信・`base` なし） |
| GitHub | `aech22/rakuten-affiliate-blog`（public） |
| 収益モデル | 楽天アフィリエイト（物販） |
| 記事生成 | GitHub Actions が毎日 JST 10:00（cron `0 1 * * *`）に生成→品質ゲート→gh-pages |

## カテゴリ（14種）

ジャンル軸 × 性別軸の2軸。**`src/data/taxonomy.ts`（Astro）と `scripts/config.py` の `CATEGORIES`（生成）で slug 一致が必須。**

- 既存6: beauty / daily / mens-fashion / ladies-fashion / accessories / outdoor
- Tier1: gourmet / makeup / fitness / disaster
- Tier2: pet / interior / kitchen / seasonal
- 性別軸: men / women / unisex（`/[gender].astro` で静的ページ生成）

記事 frontmatter に `categorySlug` ＋ `gender`。トップは性別タブ＋カテゴリチップのクライアント側フィルタ（`.article-card` の `data-gender` / `data-category` をトグル）。

⚠️ 健康・サプリは YMYL ＋薬機法で**見送り中**（カテゴリに追加しない）。

## A8 広告の掲載状況（サイドバー・2026-09-05 新設）

比較記事は楽天APIの商品で組む設計なので、**ASP案件はサービスカードにせずサイドバーのテキストリンクだけ**に置く。「広告 · ◯◯」ラベルはステマ規制対応なので外さない。**A8の広告コードは規約に従い原文のまま使う**（`&` の JSX パース回避で `set:html`）。

| 枠 | 案件 | 文脈 |
|---|---|---|
| 広告 · 家事の手間を減らす | フラットクリーニング（宅配クリーニング）＋シャークニンジャ（掃除機・キッチン家電）（1枠に2本） | daily / kitchen / interior |

⚠️ **画像バナーではなくテキストリンクを選んでいる。** 画像バナーはページを開くだけでインプレッションが立ち、動作確認の自由度が落ちるため。

## 記事URL

日付プレフィックスなしの**トピック単位の固定URL**。毎日の再生成は同URLを更新し、`date` は初回維持・`updated` を更新する（重複コンテンツ回避＝SEO）。ファイル名がそのままスラッグになる。

**スラッグは2026-08-31に日本語から英数へ切り替えた。** 決めているのは `scripts/main.py` の `article_path()` で、解決順は次の2段:

1. `legacy_slugify(theme)`（＝旧採番・日本語保持）のファイルが `content/articles/` に既にあるなら**それを使い続ける**
2. 無ければ `config.py` の各トピックの `"slug"`（英小文字・数字・ハイフン）で作る

この順序にしているのは、**公開済み記事のURLを変えないため**。URLを変えると被リンクとインデックスを捨てることになり、GitHub Pages ではリダイレクトも張れない。切替時点で公開済みだった55本は日本語URLのまま、未公開だった23トピックは新規生成時に英数URLになる。

- **トピックを追加するときは `slug` を必ず書く**（未設定・重複は `config.py` 末尾の assert が import 時に落とす）
- 旧日本語URLの記事を英数へ移したくなった場合、ファイル名を変えるだけでは**旧URLが404になる**。移行するならリダイレクトの手当てとセットで判断する（現時点では未対応・やらない方針）

## SEO の決めごと（2026-09-06）

`affiliate-seo-baseline` の7項目のうち、このサイトに欠けていた構造的なものを埋めた。**公開済み記事のタイトル・description・カテゴリページの文言は触っていない**（既存URLの評価が動くため、需要データと Search Console の実績を見てから人が判断する）。

- **記事ページは `BlogPosting` の構造化データを出す**（`ArticleLayout.astro`）。それまで `ItemList` と `FAQPage` しか無く、「いつ書かれた、誰の、何についての記事か」が伝わっていなかった。`author` は about ページが名乗っている運営者表記に合わせて屋号「TODGE」の `Organization`（**「株式会社」とは書かない**）。`publisher` は `BaseLayout` の `Organization` を `@id`（`/#organization`）で参照し、実体を二重に書かない
- **sitemap は記事に `<lastmod>` を出す**（`astro.config.mjs`）。Content Collections は設定ファイルから読めないので frontmatter を直接パースする。priority はトップ1.0・記事0.8・カテゴリ/性別/ランキング0.6・固定ページ0.3。`.md` / `.mdx` 両対応
- ⚠️ **lastmod の突き合わせは slug のデコードと小文字化が要る。** picknavi の記事 slug は**大半が日本語**（上の「記事URL」参照）なので sitemap の URL はパーセントエンコードされており、さらに Astro は slug を小文字化する（`キャンプ用LEDランタン…` → `キャンプ用ledランタン…`）。素直にファイル名でキーを作ると 61本中 6本しか一致しない。コドナビ（slug が英数）からそのまま移植すると黙って落ちる箇所
- **`404.astro` を置いた**（GitHub Pages が `dist/404.html` を使う）。`noindex` 付きで、sitemap からは `filter` で除外。カテゴリ14種へ戻す導線だけを持つ
- 記事末の関連記事（`[...slug].astro` が同カテゴリ→同性別で最大4件）は以前から入っているので触っていない

⚠️ **検証はビルド後の `dist/` の grep で行う。** 楽天アフィリリンクとサイドバーの A8 テキストリンクを含むので、レンダリングすると誤インプレッションになる。

## 品質ゲート

`scripts/quality_check.py`。workflow は `--prune`（NG記事だけ除外して他は公開・全滅時のみ失敗）。

- **禁止語チェックは編集文（タイトル＋講評）限定**。楽天の実商品名に「No.1」等があっても弾かない
- `MIN_PROSE_CHARS=450`。腕時計等は講評が短くなりがちでプルーンされることがある

## 外部サービスの設定状況（`src/consts.ts`）

| 定数 | 値 |
|---|---|
| `GA_MEASUREMENT_ID` | `G-P972NYBW02`（設定済み） |
| `PINTEREST_VERIFY` | `58cff8b4406d806c92d5571422abefa9`（設定済み・**5サイトで唯一**） |
| `SEARCH_CONSOLE_VERIFY` | `tacSjOdy0Bcf5FU6fGROr-ugbH3UQ7zwz41oHxakpx4`（設定済み） |
| `TWITTER_SITE` | 未設定 |

## 投稿キットの Drive 自動保存

日次 workflow が **別リポジトリ [aech22/pinterest-kit](https://github.com/aech22/pinterest-kit) を clone して** `gen_pins.py`（1000×1500 ピン画像）→ `gen_social_kit.py`（投稿文CSV＋投稿文テキスト）の順に実行し、`gdrive_upload.py` で Drive の「picknavi_投稿キット」へ upsert。**Drive secrets 未設定なら丸ごとスキップ（オプトイン）。**

- **生成スクリプトをこのリポジトリに複製しない。** 2026-08-12 まで `scripts/gen_social_kit.py` + `scripts/gen_pins.py` という複製が日次で動いていたが、Pinterest運用仕様が「1記事3バリアント」へ変わった後も複製側は旧仕様のままで、**Drive には旧仕様の投稿文が毎日上書きされ続けていた**。この2本は退役・削除済み
- CI では pinterest-kit の既定パス（作者のローカル）を環境変数で差し替える: `PINKIT_OUT` / `PINKIT_ARTICLES_PICKNAVI`。`--site picknavi --no-calendar` で単一サイト実行にする（カレンダーは全サイト横断の表なので CI では書かない）
- 重複台帳 `pins_ledger.json` は CI では持ち回さない。毎回全記事を生成し直すため、重複検出はその1回の実行内で完結する

- 個人 Gmail は純サービスアカウントだと容量0で upload 失敗 → **ユーザー自身の OAuth** を採用
- フル `drive` スコープ＋同意画面「テスト」状態は**リフレッシュトークンが7日で失効**するため、**`drive.file` スコープ＋アプリが自前フォルダ管理＋同意画面を本番公開**の構成にしてある
- secrets は `GDRIVE_CLIENT_ID` / `GDRIVE_CLIENT_SECRET` / `GDRIVE_REFRESH_TOKEN` の3つ（フォルダID不要）。トークン取得は `scripts/gdrive_auth.py` をローカル実行

## X 自動投稿bot

`scripts/post_to_x.py`（tweepy）。**新規 slug のみ・最大3件/回・`scripts/posted_x.json` で再投稿防止。** workflow のデプロイ後 step でオプトイン実行。X APIキーは GitHub Secrets（`X_API_KEY` / `X_API_SECRET` / `X_ACCESS_TOKEN` / `X_ACCESS_SECRET`）にユーザーがUIで設定。未設定ならスキップ。

## ローカル生成

`.env`（gitignore）に楽天4キー。実行は:

```bash
set -a && . ./.env && set +a && python3 scripts/main.py
```

ローカル python に `anthropic` / `PyYAML` の user install が必要。

## 固有のハマりどころ

- **HTTPS証明書がスタックしたら**「カスタムドメインを一度外して再設定」で発行がトリガーされる（`gh api -X PUT repos/aech22/rakuten-affiliate-blog/pages --field cname=""` → 45秒 → 再設定 → `-F https_enforced=true`）
- **ローカルDNS否定キャッシュ**: ドメイン作成前の NXDOMAIN を macOS が保持し、`dig` は通るのに `curl`/ブラウザが解決できない状態が起きる。`sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder`（sudo 必要＝ユーザー実行）。検証は `curl --resolve picknavi.net:443:185.199.108.153` で回避できる
- **OGP画像** `public/ogp.png`（1200×630）。Playwright の `file://` は不可なので、`python3 -m http.server` で配信→スクショ→`public/` で生成した

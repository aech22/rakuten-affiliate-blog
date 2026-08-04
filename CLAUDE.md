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

## 記事URL

日付プレフィックスなしの**トピック単位の固定URL**（`slugify(theme)`・日本語保持）。毎日の再生成は同URLを更新し、`date` は初回維持・`updated` を更新する（重複コンテンツ回避＝SEO）。

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

日次 workflow が `gen_social_kit.py`（投稿テキストCSV）＋ `gen_pins.py`（1000×1500 ピン画像）＋ `gdrive_upload.py` を実行し、Drive の「picknavi_投稿キット」へ upsert。**Drive secrets 未設定なら丸ごとスキップ（オプトイン）。**

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

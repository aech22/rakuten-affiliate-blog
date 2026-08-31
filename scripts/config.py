# scripts/config.py
# 1日に新規追加する記事の上限（ドリップ）。既存記事は毎日そのまま更新され、
# TOPIC_POOL の未公開トピックがこの本数だけ毎日 追加生成される（SEO健全な自然増）。
DAILY_NEW_LIMIT = 1

# ── カテゴリ体系（大元の性別軸 gender × ジャンル軸 category）──
# gender: "men" | "women" | "unisex"
# CATEGORIES の slug は Astro 側 src/data/taxonomy.ts と一致させること（記事URL・カテゴリページの結合キー）。
CATEGORIES = {
    "beauty":         {"label": "美容系",             "gender": "unisex"},
    "daily":          {"label": "日常系",             "gender": "unisex"},
    "mens-fashion":   {"label": "メンズファッション", "gender": "men"},
    "ladies-fashion": {"label": "レディースファッション", "gender": "women"},
    "accessories":    {"label": "小物系",             "gender": "unisex"},
    "outdoor":        {"label": "アウトドア系",       "gender": "unisex"},
    # Tier 1
    "gourmet":        {"label": "スイーツ・グルメ",   "gender": "unisex"},
    "makeup":         {"label": "メイクコスメ",       "gender": "women"},
    "fitness":        {"label": "フィットネス",       "gender": "unisex"},
    "disaster":       {"label": "防災グッズ",         "gender": "unisex"},
    # Tier 2
    "pet":            {"label": "ペット用品",         "gender": "unisex"},
    "interior":       {"label": "インテリア・収納",   "gender": "unisex"},
    "kitchen":        {"label": "キッチン用品",       "gender": "unisex"},
    "seasonal":       {"label": "季節家電",           "gender": "unisex"},
}

# ── 生成対象。1エントリ = 1記事。cat は CATEGORIES のキー。gender は cat から自動導出。──
#
# slug: 記事URL（https://picknavi.net/articles/<slug>/）に使う英数スラッグ。
#   2026-08-31 追加。それ以前に公開した記事は theme をそのまま使った日本語スラッグ
#   （パーセントエンコードされる）で既にインデックスされているため、main.py の
#   article_path() が「日本語スラッグのファイルが既にあるならそれを使う」順序で解決する。
#   つまり**公開済み記事のURLは変わらず、次に新規生成されるものから slug が効く**。
#   新しいトピックを足すときは slug を必ず書く（英小文字・数字・ハイフンのみ・他と重複しない）。
TOPICS = [
    # 美容系
    {"theme": "うるおいで選ぶ人気の美容液",         "slug": "serum",                    "keyword": "美容液",           "cat": "beauty",         "hits": 4},
    {"theme": "市販で買えるサロン級シャンプー",     "slug": "shampoo",                  "keyword": "シャンプー",       "cat": "beauty",         "hits": 4},
    # 日常系
    {"theme": "一人暮らし向けコーヒーメーカー比較", "slug": "coffee-maker",             "keyword": "コーヒーメーカー", "cat": "daily",          "hits": 4},
    {"theme": "コスパ重視のワイヤレスイヤホンの選び方", "slug": "wireless-earbuds",     "keyword": "ワイヤレスイヤホン", "cat": "daily",   "hits": 4},
    {"theme": "共働き家庭のロボット掃除機比較",     "slug": "robot-vacuum",             "keyword": "ロボット掃除機",   "cat": "daily",          "hits": 4},
    {"theme": "時短に効く電気ケトルの選び方",       "slug": "electric-kettle",          "keyword": "電気ケトル",       "cat": "daily",          "hits": 4},
    # メンズファッション
    {"theme": "定番から選ぶメンズスニーカー",       "slug": "mens-sneakers",            "keyword": "メンズ スニーカー", "cat": "mens-fashion",  "hits": 4},
    {"theme": "大人のメンズ二つ折り財布",           "slug": "mens-wallet",              "keyword": "メンズ 財布",      "cat": "mens-fashion",   "hits": 4},
    # レディースファッション
    {"theme": "通勤にも使えるレディースバッグ",     "slug": "ladies-bag",               "keyword": "レディース バッグ", "cat": "ladies-fashion","hits": 4},
    {"theme": "歩きやすいレディーススニーカー",     "slug": "ladies-sneakers",          "keyword": "レディース スニーカー", "cat": "ladies-fashion", "hits": 4},
    # 小物系
    {"theme": "毎日つけたい腕時計の選び方",         "slug": "watch",                    "keyword": "腕時計",           "cat": "accessories",    "hits": 4},
    {"theme": "コーデが締まるサングラスの選び方",   "slug": "sunglasses",               "keyword": "サングラス",       "cat": "accessories",    "hits": 4},
    # アウトドア系
    {"theme": "初心者向けソロキャンプ用テント",     "slug": "tent",                     "keyword": "テント",           "cat": "outdoor",        "hits": 4},
    # スイーツ・グルメ
    {"theme": "お取り寄せスイーツの人気比較",       "slug": "sweets",                   "keyword": "スイーツ",         "cat": "gourmet",        "hits": 4},
    {"theme": "ご当地グルメ・お取り寄せの選び方",   "slug": "gourmet-gift",             "keyword": "お取り寄せグルメ", "cat": "gourmet",        "hits": 4},
    # メイクコスメ
    {"theme": "プチプラで選ぶファンデーション",     "slug": "foundation",               "keyword": "ファンデーション", "cat": "makeup",         "hits": 4},
    {"theme": "落ちにくいリップの選び方",           "slug": "lipstick",                 "keyword": "口紅",             "cat": "makeup",         "hits": 4},
    # フィットネス
    {"theme": "家トレ向けプロテインの選び方",       "slug": "protein",                  "keyword": "プロテイン",       "cat": "fitness",        "hits": 4},
    {"theme": "自宅で使えるダンベル比較",           "slug": "dumbbell",                 "keyword": "ダンベル",         "cat": "fitness",        "hits": 4},
    # 防災グッズ
    {"theme": "備えておきたい防災セット比較",       "slug": "emergency-kit",            "keyword": "防災セット",       "cat": "disaster",       "hits": 4},
    {"theme": "長期保存できる非常食の選び方",       "slug": "emergency-food",           "keyword": "非常食",           "cat": "disaster",       "hits": 4},
    # ペット用品
    {"theme": "毎日使うペット用品の選び方",         "slug": "pet-supplies",             "keyword": "ペット用品",       "cat": "pet",            "hits": 4},
    # インテリア・収納
    {"theme": "部屋が片づく収納ラック比較",         "slug": "storage-rack",             "keyword": "収納 ラック",      "cat": "interior",       "hits": 4},
    # キッチン用品
    {"theme": "使いやすいフライパンの選び方",       "slug": "frying-pan",               "keyword": "フライパン",       "cat": "kitchen",        "hits": 4},
    # 季節家電
    {"theme": "乾燥対策の加湿器比較",               "slug": "humidifier",               "keyword": "加湿器",           "cat": "seasonal",       "hits": 4},
    # ── 第2弾（カテゴリ拡充）──
    {"theme": "軽くて涼しいアウトドアチェア比較",   "slug": "outdoor-chair",            "keyword": "アウトドア チェア", "cat": "outdoor",       "hits": 4},
    {"theme": "保冷力で選ぶクーラーボックス",       "slug": "cooler-box",               "keyword": "クーラーボックス", "cat": "outdoor",        "hits": 4},
    {"theme": "掃除がラクな猫用トイレの選び方",     "slug": "cat-litter-box",           "keyword": "猫 トイレ",        "cat": "pet",            "hits": 4},
    {"theme": "愛犬が喜ぶドッグフードの選び方",     "slug": "dog-food",                 "keyword": "ドッグフード",     "cat": "pet",            "hits": 4},
    {"theme": "在宅ワークが捗るパソコンデスク比較", "slug": "computer-desk",            "keyword": "パソコンデスク",   "cat": "interior",       "hits": 4},
    {"theme": "時短調理の電気圧力鍋比較",           "slug": "electric-pressure-cooker", "keyword": "電気圧力鍋",       "cat": "kitchen",        "hits": 4},
    {"theme": "静音で選ぶ扇風機・サーキュレーター", "slug": "electric-fan",             "keyword": "扇風機",           "cat": "seasonal",       "hits": 4},
    {"theme": "冬の必需品 電気毛布の選び方",        "slug": "electric-blanket",         "keyword": "電気毛布",         "cat": "seasonal",       "hits": 4},
    {"theme": "大容量モバイルバッテリー比較",       "slug": "power-bank",               "keyword": "モバイルバッテリー", "cat": "daily",         "hits": 4},
    {"theme": "自宅で楽しむコーヒー豆の選び方",     "slug": "coffee-beans",             "keyword": "コーヒー豆",       "cat": "gourmet",        "hits": 4},
    # 追加はここに1行ずつ（cat は CATEGORIES のキーから選ぶ。slug は必須）
]

# ── トピックプール（未公開の候補）──
# ここから毎日 DAILY_NEW_LIMIT 本ずつ「まだ記事が無いもの」を自動で追加生成する。
# 公開済みになったら通常の更新対象になる。枯渇したら良質キーワードを追記して補充する。
TOPIC_POOL = [
    # 美容系
    {"theme": "乾燥肌向け化粧水の選び方",           "slug": "toner",                    "keyword": "化粧水",           "cat": "beauty",         "hits": 4},
    {"theme": "紫外線対策の日焼け止め比較",         "slug": "sunscreen",                "keyword": "日焼け止め",       "cat": "beauty",         "hits": 4},
    {"theme": "毛穴ケアできるクレンジング比較",     "slug": "cleansing",                "keyword": "クレンジング",     "cat": "beauty",         "hits": 4},
    # 日常系
    {"theme": "花粉・ハウスダスト対策の空気清浄機比較", "slug": "air-purifier",         "keyword": "空気清浄機",   "cat": "daily",          "hits": 4},
    {"theme": "速乾で選ぶヘアドライヤー比較",       "slug": "hair-dryer",               "keyword": "ドライヤー",       "cat": "daily",          "hits": 4},
    {"theme": "コスパで選ぶ電動歯ブラシ比較",       "slug": "electric-toothbrush",      "keyword": "電動歯ブラシ",     "cat": "daily",          "hits": 4},
    {"theme": "体組成計・体重計の選び方",           "slug": "body-scale",               "keyword": "体重計",           "cat": "daily",          "hits": 4},
    # メンズファッション
    {"theme": "着回せるメンズTシャツの選び方",      "slug": "mens-tshirt",              "keyword": "メンズ Tシャツ",   "cat": "mens-fashion",   "hits": 4},
    {"theme": "通勤に使えるメンズリュック比較",     "slug": "mens-backpack",            "keyword": "メンズ リュック",  "cat": "mens-fashion",   "hits": 4},
    {"theme": "本革メンズベルトの選び方",           "slug": "mens-belt",                "keyword": "メンズ ベルト",    "cat": "mens-fashion",   "hits": 4},
    # レディースファッション
    {"theme": "着回せるレディースワンピース比較",   "slug": "ladies-dress",             "keyword": "レディース ワンピース", "cat": "ladies-fashion", "hits": 4},
    {"theme": "冬のレディースコートの選び方",       "slug": "ladies-coat",              "keyword": "レディース コート", "cat": "ladies-fashion", "hits": 4},
    {"theme": "疲れにくいパンプスの選び方",         "slug": "pumps",                    "keyword": "パンプス",         "cat": "ladies-fashion", "hits": 4},
    # 小物系
    {"theme": "普段使いのネックレスの選び方",       "slug": "necklace",                 "keyword": "ネックレス",       "cat": "accessories",    "hits": 4},
    {"theme": "暖かいマフラー・ストールの選び方",   "slug": "scarf",                    "keyword": "マフラー",         "cat": "accessories",    "hits": 4},
    {"theme": "コーデが決まる帽子の選び方",         "slug": "hat",                      "keyword": "帽子",             "cat": "accessories",    "hits": 4},
    # アウトドア系
    {"theme": "季節で選ぶ寝袋・シュラフ比較",       "slug": "sleeping-bag",             "keyword": "寝袋",             "cat": "outdoor",        "hits": 4},
    {"theme": "キャンプ用LEDランタンの選び方",      "slug": "lantern",                  "keyword": "ランタン",         "cat": "outdoor",        "hits": 4},
    {"theme": "折りたたみアウトドアテーブル比較",   "slug": "outdoor-table",            "keyword": "アウトドアテーブル", "cat": "outdoor",       "hits": 4},
    # スイーツ・グルメ
    {"theme": "お取り寄せラーメンの人気比較",       "slug": "ramen",                    "keyword": "ラーメン お取り寄せ", "cat": "gourmet",      "hits": 4},
    {"theme": "お取り寄せ冷凍餃子の選び方",         "slug": "frozen-gyoza",             "keyword": "冷凍餃子",         "cat": "gourmet",        "hits": 4},
    {"theme": "手軽なドリップコーヒーの選び方",     "slug": "drip-coffee",              "keyword": "ドリップコーヒー", "cat": "gourmet",        "hits": 4},
    # メイクコスメ
    {"theme": "捨て色なしアイシャドウパレット比較", "slug": "eyeshadow-palette",        "keyword": "アイシャドウ",     "cat": "makeup",         "hits": 4},
    {"theme": "にじみにくいマスカラの選び方",       "slug": "mascara",                  "keyword": "マスカラ",         "cat": "makeup",         "hits": 4},
    {"theme": "崩れにくい化粧下地の選び方",         "slug": "makeup-primer",            "keyword": "化粧下地",         "cat": "makeup",         "hits": 4},
    # フィットネス
    {"theme": "初心者向け腹筋ローラーの選び方",     "slug": "ab-roller",                "keyword": "腹筋ローラー",     "cat": "fitness",        "hits": 4},
    {"theme": "自宅で使うトレーニングチューブ比較", "slug": "resistance-band",          "keyword": "トレーニングチューブ", "cat": "fitness",     "hits": 4},
    {"theme": "続けやすいヨガマットの選び方",       "slug": "yoga-mat",                 "keyword": "ヨガマット",       "cat": "fitness",        "hits": 4},
    # 防災グッズ
    {"theme": "手回し充電できる防災ラジオ比較",     "slug": "emergency-radio",          "keyword": "防災ラジオ",       "cat": "disaster",       "hits": 4},
    {"theme": "備えておく携帯・簡易トイレの選び方", "slug": "portable-toilet",          "keyword": "携帯トイレ",       "cat": "disaster",       "hits": 4},
    {"theme": "防災用LED懐中電灯の選び方",          "slug": "led-flashlight",           "keyword": "懐中電灯",         "cat": "disaster",       "hits": 4},
    # ペット用品
    {"theme": "省スペースなキャットタワー比較",     "slug": "cat-tower",                "keyword": "キャットタワー",   "cat": "pet",            "hits": 4},
    {"theme": "愛犬に合う首輪・ハーネスの選び方",   "slug": "dog-harness",              "keyword": "犬 ハーネス",      "cat": "pet",            "hits": 4},
    {"theme": "見守りペットカメラの選び方",         "slug": "pet-camera",               "keyword": "ペットカメラ",     "cat": "pet",            "hits": 4},
    # インテリア・収納
    {"theme": "遮光・断熱カーテンの選び方",         "slug": "blackout-curtain",         "keyword": "カーテン",         "cat": "interior",       "hits": 4},
    {"theme": "洗えるラグ・カーペットの選び方",     "slug": "washable-rug",             "keyword": "ラグ",             "cat": "interior",       "hits": 4},
    {"theme": "一人暮らし向けベッドフレーム比較",   "slug": "bed-frame",                "keyword": "ベッドフレーム",   "cat": "interior",       "hits": 4},
    # キッチン用品
    {"theme": "切れ味で選ぶ包丁の選び方",           "slug": "kitchen-knife",            "keyword": "包丁",             "cat": "kitchen",        "hits": 4},
    {"theme": "家族で使うホットプレート比較",       "slug": "hot-plate",                "keyword": "ホットプレート",   "cat": "kitchen",        "hits": 4},
    {"theme": "こんがり焼けるトースター比較",       "slug": "toaster",                  "keyword": "トースター",       "cat": "kitchen",        "hits": 4},
    # 季節家電
    {"theme": "一人暮らし向けこたつの選び方",       "slug": "kotatsu",                  "keyword": "こたつ",           "cat": "seasonal",       "hits": 4},
    {"theme": "梅雨対策の除湿機比較",               "slug": "dehumidifier",             "keyword": "除湿機",           "cat": "seasonal",       "hits": 4},
    {"theme": "足元を温めるヒーターの選び方",       "slug": "foot-heater",              "keyword": "ヒーター",         "cat": "seasonal",       "hits": 4},
]

# slug の重複は URL の衝突（＝記事の上書き）に直結するので、import 時に落とす。
_ALL_TOPICS = list(TOPICS) + list(TOPIC_POOL)
_SLUGS = [t["slug"] for t in _ALL_TOPICS if "slug" in t]
_DUPES = sorted({s for s in _SLUGS if _SLUGS.count(s) > 1})
assert not _DUPES, f"config.py: slug が重複しています: {_DUPES}"
_MISSING = [t["theme"] for t in _ALL_TOPICS if not t.get("slug")]
assert not _MISSING, f"config.py: slug が未設定のトピックがあります: {_MISSING}"

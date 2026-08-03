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
TOPICS = [
    # 美容系
    {"theme": "うるおいで選ぶ人気の美容液",         "keyword": "美容液",           "cat": "beauty",         "hits": 4},
    {"theme": "市販で買えるサロン級シャンプー",     "keyword": "シャンプー",       "cat": "beauty",         "hits": 4},
    # 日常系
    {"theme": "一人暮らし向けコーヒーメーカー比較", "keyword": "コーヒーメーカー", "cat": "daily",          "hits": 4},
    {"theme": "コスパ重視のワイヤレスイヤホンの選び方", "keyword": "ワイヤレスイヤホン", "cat": "daily",   "hits": 4},
    {"theme": "共働き家庭のロボット掃除機比較",     "keyword": "ロボット掃除機",   "cat": "daily",          "hits": 4},
    {"theme": "時短に効く電気ケトルの選び方",       "keyword": "電気ケトル",       "cat": "daily",          "hits": 4},
    # メンズファッション
    {"theme": "定番から選ぶメンズスニーカー",       "keyword": "メンズ スニーカー", "cat": "mens-fashion",  "hits": 4},
    {"theme": "大人のメンズ二つ折り財布",           "keyword": "メンズ 財布",      "cat": "mens-fashion",   "hits": 4},
    # レディースファッション
    {"theme": "通勤にも使えるレディースバッグ",     "keyword": "レディース バッグ", "cat": "ladies-fashion","hits": 4},
    {"theme": "歩きやすいレディーススニーカー",     "keyword": "レディース スニーカー", "cat": "ladies-fashion", "hits": 4},
    # 小物系
    {"theme": "毎日つけたい腕時計の選び方",         "keyword": "腕時計",           "cat": "accessories",    "hits": 4},
    {"theme": "コーデが締まるサングラスの選び方",   "keyword": "サングラス",       "cat": "accessories",    "hits": 4},
    # アウトドア系
    {"theme": "初心者向けソロキャンプ用テント",     "keyword": "テント",           "cat": "outdoor",        "hits": 4},
    # スイーツ・グルメ
    {"theme": "お取り寄せスイーツの人気比較",       "keyword": "スイーツ",         "cat": "gourmet",        "hits": 4},
    {"theme": "ご当地グルメ・お取り寄せの選び方",   "keyword": "お取り寄せグルメ", "cat": "gourmet",        "hits": 4},
    # メイクコスメ
    {"theme": "プチプラで選ぶファンデーション",     "keyword": "ファンデーション", "cat": "makeup",         "hits": 4},
    {"theme": "落ちにくいリップの選び方",           "keyword": "口紅",             "cat": "makeup",         "hits": 4},
    # フィットネス
    {"theme": "家トレ向けプロテインの選び方",       "keyword": "プロテイン",       "cat": "fitness",        "hits": 4},
    {"theme": "自宅で使えるダンベル比較",           "keyword": "ダンベル",         "cat": "fitness",        "hits": 4},
    # 防災グッズ
    {"theme": "備えておきたい防災セット比較",       "keyword": "防災セット",       "cat": "disaster",       "hits": 4},
    {"theme": "長期保存できる非常食の選び方",       "keyword": "非常食",           "cat": "disaster",       "hits": 4},
    # ペット用品
    {"theme": "毎日使うペット用品の選び方",         "keyword": "ペット用品",       "cat": "pet",            "hits": 4},
    # インテリア・収納
    {"theme": "部屋が片づく収納ラック比較",         "keyword": "収納 ラック",      "cat": "interior",       "hits": 4},
    # キッチン用品
    {"theme": "使いやすいフライパンの選び方",       "keyword": "フライパン",       "cat": "kitchen",        "hits": 4},
    # 季節家電
    {"theme": "乾燥対策の加湿器比較",               "keyword": "加湿器",           "cat": "seasonal",       "hits": 4},
    # ── 第2弾（カテゴリ拡充）──
    {"theme": "軽くて涼しいアウトドアチェア比較",   "keyword": "アウトドア チェア", "cat": "outdoor",       "hits": 4},
    {"theme": "保冷力で選ぶクーラーボックス",       "keyword": "クーラーボックス", "cat": "outdoor",        "hits": 4},
    {"theme": "掃除がラクな猫用トイレの選び方",     "keyword": "猫 トイレ",        "cat": "pet",            "hits": 4},
    {"theme": "愛犬が喜ぶドッグフードの選び方",     "keyword": "ドッグフード",     "cat": "pet",            "hits": 4},
    {"theme": "在宅ワークが捗るパソコンデスク比較", "keyword": "パソコンデスク",   "cat": "interior",       "hits": 4},
    {"theme": "時短調理の電気圧力鍋比較",           "keyword": "電気圧力鍋",       "cat": "kitchen",        "hits": 4},
    {"theme": "静音で選ぶ扇風機・サーキュレーター", "keyword": "扇風機",           "cat": "seasonal",       "hits": 4},
    {"theme": "冬の必需品 電気毛布の選び方",        "keyword": "電気毛布",         "cat": "seasonal",       "hits": 4},
    {"theme": "大容量モバイルバッテリー比較",       "keyword": "モバイルバッテリー", "cat": "daily",         "hits": 4},
    {"theme": "自宅で楽しむコーヒー豆の選び方",     "keyword": "コーヒー豆",       "cat": "gourmet",        "hits": 4},
    # 追加はここに1行ずつ（cat は CATEGORIES のキーから選ぶ）
]

# ── トピックプール（未公開の候補）──
# ここから毎日 DAILY_NEW_LIMIT 本ずつ「まだ記事が無いもの」を自動で追加生成する。
# 公開済みになったら通常の更新対象になる。枯渇したら良質キーワードを追記して補充する。
TOPIC_POOL = [
    # 美容系
    {"theme": "乾燥肌向け化粧水の選び方",           "keyword": "化粧水",           "cat": "beauty",         "hits": 4},
    {"theme": "紫外線対策の日焼け止め比較",         "keyword": "日焼け止め",       "cat": "beauty",         "hits": 4},
    {"theme": "毛穴ケアできるクレンジング比較",     "keyword": "クレンジング",     "cat": "beauty",         "hits": 4},
    # 日常系
    {"theme": "花粉・ハウスダスト対策の空気清浄機比較", "keyword": "空気清浄機",   "cat": "daily",          "hits": 4},
    {"theme": "速乾で選ぶヘアドライヤー比較",       "keyword": "ドライヤー",       "cat": "daily",          "hits": 4},
    {"theme": "コスパで選ぶ電動歯ブラシ比較",       "keyword": "電動歯ブラシ",     "cat": "daily",          "hits": 4},
    {"theme": "体組成計・体重計の選び方",           "keyword": "体重計",           "cat": "daily",          "hits": 4},
    # メンズファッション
    {"theme": "着回せるメンズTシャツの選び方",      "keyword": "メンズ Tシャツ",   "cat": "mens-fashion",   "hits": 4},
    {"theme": "通勤に使えるメンズリュック比較",     "keyword": "メンズ リュック",  "cat": "mens-fashion",   "hits": 4},
    {"theme": "本革メンズベルトの選び方",           "keyword": "メンズ ベルト",    "cat": "mens-fashion",   "hits": 4},
    # レディースファッション
    {"theme": "着回せるレディースワンピース比較",   "keyword": "レディース ワンピース", "cat": "ladies-fashion", "hits": 4},
    {"theme": "冬のレディースコートの選び方",       "keyword": "レディース コート", "cat": "ladies-fashion", "hits": 4},
    {"theme": "疲れにくいパンプスの選び方",         "keyword": "パンプス",         "cat": "ladies-fashion", "hits": 4},
    # 小物系
    {"theme": "普段使いのネックレスの選び方",       "keyword": "ネックレス",       "cat": "accessories",    "hits": 4},
    {"theme": "暖かいマフラー・ストールの選び方",   "keyword": "マフラー",         "cat": "accessories",    "hits": 4},
    {"theme": "コーデが決まる帽子の選び方",         "keyword": "帽子",             "cat": "accessories",    "hits": 4},
    # アウトドア系
    {"theme": "季節で選ぶ寝袋・シュラフ比較",       "keyword": "寝袋",             "cat": "outdoor",        "hits": 4},
    {"theme": "キャンプ用LEDランタンの選び方",      "keyword": "ランタン",         "cat": "outdoor",        "hits": 4},
    {"theme": "折りたたみアウトドアテーブル比較",   "keyword": "アウトドアテーブル", "cat": "outdoor",       "hits": 4},
    # スイーツ・グルメ
    {"theme": "お取り寄せラーメンの人気比較",       "keyword": "ラーメン お取り寄せ", "cat": "gourmet",      "hits": 4},
    {"theme": "お取り寄せ冷凍餃子の選び方",         "keyword": "冷凍餃子",         "cat": "gourmet",        "hits": 4},
    {"theme": "手軽なドリップコーヒーの選び方",     "keyword": "ドリップコーヒー", "cat": "gourmet",        "hits": 4},
    # メイクコスメ
    {"theme": "捨て色なしアイシャドウパレット比較", "keyword": "アイシャドウ",     "cat": "makeup",         "hits": 4},
    {"theme": "にじみにくいマスカラの選び方",       "keyword": "マスカラ",         "cat": "makeup",         "hits": 4},
    {"theme": "崩れにくい化粧下地の選び方",         "keyword": "化粧下地",         "cat": "makeup",         "hits": 4},
    # フィットネス
    {"theme": "初心者向け腹筋ローラーの選び方",     "keyword": "腹筋ローラー",     "cat": "fitness",        "hits": 4},
    {"theme": "自宅で使うトレーニングチューブ比較", "keyword": "トレーニングチューブ", "cat": "fitness",     "hits": 4},
    {"theme": "続けやすいヨガマットの選び方",       "keyword": "ヨガマット",       "cat": "fitness",        "hits": 4},
    # 防災グッズ
    {"theme": "手回し充電できる防災ラジオ比較",     "keyword": "防災ラジオ",       "cat": "disaster",       "hits": 4},
    {"theme": "備えておく携帯・簡易トイレの選び方", "keyword": "携帯トイレ",       "cat": "disaster",       "hits": 4},
    {"theme": "防災用LED懐中電灯の選び方",          "keyword": "懐中電灯",         "cat": "disaster",       "hits": 4},
    # ペット用品
    {"theme": "省スペースなキャットタワー比較",     "keyword": "キャットタワー",   "cat": "pet",            "hits": 4},
    {"theme": "愛犬に合う首輪・ハーネスの選び方",   "keyword": "犬 ハーネス",      "cat": "pet",            "hits": 4},
    {"theme": "見守りペットカメラの選び方",         "keyword": "ペットカメラ",     "cat": "pet",            "hits": 4},
    # インテリア・収納
    {"theme": "遮光・断熱カーテンの選び方",         "keyword": "カーテン",         "cat": "interior",       "hits": 4},
    {"theme": "洗えるラグ・カーペットの選び方",     "keyword": "ラグ",             "cat": "interior",       "hits": 4},
    {"theme": "一人暮らし向けベッドフレーム比較",   "keyword": "ベッドフレーム",   "cat": "interior",       "hits": 4},
    # キッチン用品
    {"theme": "切れ味で選ぶ包丁の選び方",           "keyword": "包丁",             "cat": "kitchen",        "hits": 4},
    {"theme": "家族で使うホットプレート比較",       "keyword": "ホットプレート",   "cat": "kitchen",        "hits": 4},
    {"theme": "こんがり焼けるトースター比較",       "keyword": "トースター",       "cat": "kitchen",        "hits": 4},
    # 季節家電
    {"theme": "一人暮らし向けこたつの選び方",       "keyword": "こたつ",           "cat": "seasonal",       "hits": 4},
    {"theme": "梅雨対策の除湿機比較",               "keyword": "除湿機",           "cat": "seasonal",       "hits": 4},
    {"theme": "足元を温めるヒーターの選び方",       "keyword": "ヒーター",         "cat": "seasonal",       "hits": 4},
]

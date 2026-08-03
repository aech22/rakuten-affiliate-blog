# scripts/config.py
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
    # 追加はここに1行ずつ（cat は CATEGORIES のキーから選ぶ）
]

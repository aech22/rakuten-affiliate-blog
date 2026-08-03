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
    # 追加はここに1行ずつ（cat は CATEGORIES のキーから選ぶ）
]

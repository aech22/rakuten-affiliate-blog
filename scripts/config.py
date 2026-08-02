# scripts/config.py
# 生成対象の一覧。1エントリ = 1記事。keyword は楽天商品検索APIに渡す検索語、
# category はサイト上のバッジ表示・分類に使う短い名前。hits は1記事あたりの比較商品数。
TOPICS = [
    {"theme": "一人暮らし向けコーヒーメーカー比較", "keyword": "コーヒーメーカー",   "category": "コーヒーメーカー", "hits": 4},
    {"theme": "コスパ重視のワイヤレスイヤホンの選び方", "keyword": "ワイヤレスイヤホン", "category": "イヤホン",       "hits": 4},
    {"theme": "共働き家庭のロボット掃除機比較",       "keyword": "ロボット掃除機",     "category": "掃除機",         "hits": 4},
    {"theme": "時短に効く電気ケトルの選び方",         "keyword": "電気ケトル",         "category": "キッチン家電",   "hits": 4},
    # 追加はここに1行ずつ（category は任意。無ければ keyword が使われる）
]

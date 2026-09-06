#!/usr/bin/env python3
"""scripts/quality_check.py の表現ゲートのテスト。`python3 scripts/test_quality_check.py`

このゲートが守っているのは「商材ではなく表現で切る」という判断軸。
軸を商材（販売資格の有無）に戻すと、販売しないこちらには何も掛からず、
最も表現リスクの高いプロテイン・サプリ・化粧品が素通りする。

「機械的に判定する」仕組みは端ケースを流してから完成と呼ぶ
（Knowledge/mistakes.md 2026-08-04 の教訓）。ここで流すのは次の3つ。
  ① 何も入っていない入力で誤検出しないか
  ② 日常語（収納が改善する等）で偽陽性を出さないか
  ③ 複数の法令に同時に当たる入力で全部report されるか
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from quality_check import expression_violations, check  # noqa: E402

failed = 0


def eq(name, got, want):
    global failed
    if got != want:
        failed += 1
        print(f"  FAIL {name}\n       got  {got!r}\n       want {want!r}")
    else:
        print(f"  PASS {name}")


# ① 空・無害
eq("空文字は違反なし", expression_violations(""), [])
eq("普通の講評は違反なし",
   expression_violations("軽くて持ち運びやすく、一人暮らしの部屋にも置きやすいサイズです。"), [])

# ② 日常語で偽陽性を出さない（ここが緩むと全記事が落ちて誰も直さなくなる）
eq("「改善」単体は拾わない", expression_violations("収納が改善するので部屋が片づきます。"), [])
eq("「回復」単体は拾わない", expression_violations("充電の回復が早いモデルです。"), [])
eq("「予防」単体は拾わない", expression_violations("結露の予防に役立ちます。"), [])

# 薬機法
eq("効能の主張を拾う", expression_violations("飲めば疲労回復に効きます。"), ["薬機法: 疲労回復"])
eq("症状の改善を拾う", expression_violations("肩こりの症状が改善します。"), ["薬機法: 症状が改善"])
eq("痩身の断定を拾う", expression_violations("これを使えば痩せます。"), ["薬機法: 痩せます"])
eq("育毛を拾う", expression_violations("育毛に良いとされています。"), ["薬機法: 育毛"])

# 健康増進法
eq("「飲むだけで」を拾う",
   expression_violations("飲むだけで体型が変わります。"), ["健康増進法: 飲むだけで"])

# 景表法（既存の挙動を維持していること）
eq("最安値を拾う", expression_violations("いま最安値で買えます。"), ["景表法: 最安値"])
eq("No.1を拾う", expression_violations("売上No.1の実績。"), ["景表法: No.1"])

# ③ 複数の法令に同時に当たる
eq("複数法令を全部返す",
   expression_violations("最安値で、飲むだけで痩せます。"),
   ["景表法: 最安値", "薬機法: 痩せます", "健康増進法: 飲むだけで"])


# 記事まるごとの検査（扱わない商材）
def article(title="テスト", name="ふつうの商品", prose="あ" * 500):
    return (
        "---\n"
        f"title: {title}\n"
        "date: 2026-09-06\n"
        "categorySlug: fitness\n"
        "gender: unisex\n"
        f"intro: {prose}\n"
        "outro: まとめ\n"
        "products:\n"
        f"  - name: {name}\n"
        "    image: https://example.com/a.jpg\n"
        "    url: https://hb.afl.rakuten.co.jp/x\n"
        "---\n本文\n"
    )


def has(errors, fragment):
    return any(fragment in e for e in errors)


eq("プロテイン記事は商材だけでは落ちない",
   has(check(article(title="家トレ向けプロテインの選び方")), "扱わない商材"), False)
eq("医薬品が商品名に混ざったら落ちる",
   has(check(article(name="第2類医薬品 かぜ薬")), "扱わない商材"), True)
# 医薬部外品は落とさない。薬用化粧水・薬用美容液の表示で、公開済み3本が誤検出で落ちた実績がある
eq("医薬部外品の化粧品は落とさない",
   has(check(article(name="薬用化粧水 医薬部外品 200ml")), "扱わない商材"), False)
eq("コンタクトレンズは落ちる",
   has(check(article(title="コンタクトレンズの選び方")), "扱わない商材"), True)
eq("効能表現を書いたプロテイン記事は落ちる",
   has(check(article(title="プロテイン", prose="疲労回復に効きます。" + "あ" * 500)), "薬機法"), True)

print(f"\n{'FAILED' if failed else 'OK'}: {failed} failure(s)")
sys.exit(1 if failed else 0)

# scripts/gen_pins.py
# 各記事から Pinterest 向けの縦長(2:3・1000x1500)ピン画像を生成する。
# 楽天の商品画像を白カードに載せ、下部にカテゴリ・タイトル・picknavi を重ねたブランドピン。
from __future__ import annotations
import io, os, sys
from pathlib import Path
import requests
import yaml
from PIL import Image, ImageDraw, ImageFont

W, H = 1000, 1500
BRAND  = (255, 107, 53)   # #ff6b35
BRAND2 = (255, 154, 90)   # #ff9a5a
WHITE  = (255, 255, 255)
INK    = (35, 48, 58)

ART_DIR = Path(__file__).resolve().parent.parent / "content" / "articles"

# Linux(Actions: fonts-noto-cjk) / macOS の両対応でフォントを探す
FONT_CANDIDATES = [
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/System/Library/Fonts/ヒラギノ角ゴシック W7.ttc",
    "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc",
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
    "/Library/Fonts/Arial Unicode.ttf",
]

def load_font(size: int) -> ImageFont.FreeTypeFont:
    for p in FONT_CANDIDATES:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()

def vgradient(w: int, h: int, c1, c2) -> Image.Image:
    img = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(img)
    for y in range(h):
        t = y / h
        col = tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))
        d.line([(0, y), (w, y)], fill=col)
    return img

def wrap(draw: ImageDraw.ImageDraw, text: str, font, max_w: int, max_lines: int) -> list:
    lines, cur = [], ""
    for ch in text:
        if draw.textlength(cur + ch, font=font) <= max_w:
            cur += ch
        else:
            lines.append(cur); cur = ch
            if len(lines) == max_lines:
                cur = ""
                break
    if cur:
        lines.append(cur)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
    return lines

def fetch_image(url: str) -> Image.Image | None:
    try:
        r = requests.get(url, timeout=20)
        if r.status_code != 200:
            return None
        return Image.open(io.BytesIO(r.content)).convert("RGB")
    except Exception:
        return None

def make_pin(image_url: str, title: str, category: str, out_path: Path) -> bool:
    canvas = vgradient(W, H, BRAND, BRAND2)
    draw = ImageDraw.Draw(canvas)

    # 上部: ブランド＋カテゴリ
    f_brand = load_font(46)
    draw.text((70, 70), "picknavi", font=f_brand, fill=WHITE)
    if category:
        f_cat = load_font(34)
        cw = draw.textlength(category, font=f_cat)
        draw.rounded_rectangle([70, 150, 70 + cw + 56, 210], radius=30, fill=(255, 255, 255, 60))
        draw.text((98, 160), category, font=f_cat, fill=BRAND)

    # 中央: 白カードに商品画像（contain）
    card = [60, 250, W - 60, 1010]
    draw.rounded_rectangle(card, radius=40, fill=WHITE)
    prod = fetch_image(image_url) if image_url else None
    if prod:
        box_w, box_h = (card[2] - card[0] - 80), (card[3] - card[1] - 80)
        prod.thumbnail((box_w, box_h), Image.LANCZOS)
        px = card[0] + ((card[2] - card[0]) - prod.width) // 2
        py = card[1] + ((card[3] - card[1]) - prod.height) // 2
        canvas.paste(prod, (px, py))

    # 下部: タイトル（白・太・折り返し）
    f_title = load_font(58)
    lines = wrap(draw, title, f_title, W - 140, 4)
    y = 1070
    for ln in lines:
        draw.text((70, y), ln, font=f_title, fill=WHITE)
        y += 76

    # 下端: 比較コピー
    f_sub = load_font(32)
    draw.text((70, H - 90), "写真・価格・レビューで比較", font=f_sub, fill=(255, 255, 255))

    out_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out_path, "JPEG", quality=85)
    return True

def mmdd(fm: dict) -> str:
    """公開日(date)を MMDD 文字列にする。ファイル名の先頭に付けて新着を見分けやすくする。"""
    d = fm.get("date")
    s = d.strftime("%Y-%m-%d") if hasattr(d, "strftime") else str(d)
    parts = s.split("-")
    return f"{parts[1]}{parts[2]}" if len(parts) >= 3 else "0000"

def main(out_dir: str) -> None:
    out = Path(out_dir)
    made = 0
    for p in sorted(ART_DIR.glob("*.md")):
        try:
            fm = yaml.safe_load(p.read_text(encoding="utf-8").split("---", 2)[1]) or {}
        except Exception:
            continue
        title = fm.get("title", p.stem)
        category = fm.get("category", "") or ""
        products = fm.get("products") or []
        image = (products[0] or {}).get("image", "") if products else ""
        name = f"{mmdd(fm)}_{p.stem}.jpg"
        try:
            make_pin(image, title, category, out / name)
            made += 1
            print(f"pin -> {name}")
        except Exception as e:
            print(f"[SKIP] {p.stem}: {type(e).__name__}: {e}")
    print(f"done: {made} pins -> {out}")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "social/pins")

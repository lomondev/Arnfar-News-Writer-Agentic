#!/usr/bin/env python3
"""Arnfar 4-card set — open-source Office alternatives (2026-10-14).

Liquid-glass on a story backdrop, Phetsarath OT Regular for Lao,
Noto Sans Regular for Latin. Regular weight only, hierarchy from size/colour.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Iterable, Sequence

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent
LAO_FONT = ROOT / "fonts" / "Phetsarath-Regular.ttf"
LAT_FONT = ROOT / "fonts" / "NotoLatin-Regular.ttf"
W, H = 1080, 1350
PAD_X = int(W * 0.10)          # FB collage crop-safe margin
PAD_Y = int(H * 0.055)

BLUE = (3, 148, 241)
GREEN = (21, 198, 122)
WHITE = (255, 255, 255)
INK2 = (200, 218, 235)
MUTED = (150, 170, 190)
RED = (255, 107, 107)

TEXT_SHADOW: int = 0      # 0 = off; 0-255 shadow strength
DARK_GLASS: float = 0.0   # 0 = classic white veil; e.g. 0.55 = smoked glass
SCRIM = (70, 0.55)       # (top alpha, gradient strength)

_cache: dict[tuple[str, int], ImageFont.FreeTypeFont] = {}


def font(kind: str, size: int) -> ImageFont.FreeTypeFont:
    key = (kind, size)
    if key not in _cache:
        path = LAO_FONT if kind == "lao" else LAT_FONT
        _cache[key] = ImageFont.truetype(str(path), size, layout_engine=ImageFont.Layout.RAQM)
    return _cache[key]


def is_lao(ch: str) -> bool:
    return "຀" <= ch <= "໿"


def runs(text: str) -> list[tuple[str, str]]:
    """Split into (kind, text) runs; spaces stick to the preceding run."""
    out: list[tuple[str, str]] = []
    for ch in text:
        kind = "lao" if is_lao(ch) else "lat"
        if ch == " " and out:
            kind = out[-1][0]
        if out and out[-1][0] == kind:
            out[-1] = (kind, out[-1][1] + ch)
        else:
            out.append((kind, ch))
    return out


def run_size(kind: str, size: int) -> int:
    # Phetsarath reads smaller than Noto at equal px; balance optically.
    return int(size * 1.08) if kind == "lao" else size


def text_width(text: str, size: int) -> int:
    return int(sum(font(k, run_size(k, size)).getlength(t) for k, t in runs(text)))


def draw_text(img: Image.Image, xy: tuple[int, int], text: str, size: int,
              fill: tuple[int, int, int] | None = WHITE, gradient: bool = False,
              anchor_center: bool = False) -> int:
    """Draw mixed-script text on a common baseline. Returns width."""
    x, y = xy
    total = text_width(text, size)
    if anchor_center:
        x -= total // 2
    asc = max(font(k, run_size(k, size)).getmetrics()[0] for k, _ in runs(text))
    baseline = y + asc
    if TEXT_SHADOW:
        pad = size
        sm = Image.new("L", (total + pad * 2, int(size * 2.2) + pad), 0)
        sd = ImageDraw.Draw(sm)
        cx = pad
        for k, t in runs(text):
            f = font(k, run_size(k, size))
            sd.text((cx, pad // 2 + asc), t, font=f, fill=TEXT_SHADOW, anchor="ls")
            cx += f.getlength(t)
        sm = sm.filter(ImageFilter.GaussianBlur(max(3, size // 9)))
        img.paste((2, 6, 20), (x - pad + 2, y - pad // 2 + max(2, size // 22)), sm)
    if gradient:
        mask = Image.new("L", img.size, 0)
        md = ImageDraw.Draw(mask)
        cx = x
        for k, t in runs(text):
            f = font(k, run_size(k, size))
            md.text((cx, baseline), t, font=f, fill=255, anchor="ls")
            cx += f.getlength(t)
        grad = gradient_img((total + 4, int(size * 1.8)), BLUE, GREEN, horizontal=True)
        layer = Image.new("RGB", img.size, BLUE)
        layer.paste(grad, (x, y - int(size * 0.3)))
        img.paste(layer, (0, 0), mask)
    else:
        d = ImageDraw.Draw(img)
        cx = x
        for k, t in runs(text):
            f = font(k, run_size(k, size))
            d.text((cx, baseline), t, font=f, fill=fill, anchor="ls")
            cx += f.getlength(t)
    return total


def gradient_img(size: tuple[int, int], c1: Sequence[int], c2: Sequence[int],
                 horizontal: bool = True) -> Image.Image:
    w, h = max(size[0], 1), max(size[1], 1)
    base = Image.linear_gradient("L").rotate(90 if horizontal else 0, expand=True)
    base = base.resize((w, h))
    if horizontal:
        base = base.transpose(Image.FLIP_LEFT_RIGHT)
    return Image.composite(Image.new("RGB", (w, h), tuple(c2)),
                           Image.new("RGB", (w, h), tuple(c1)), base)


def rounded_mask(size: tuple[int, int], r: int) -> Image.Image:
    m = Image.new("L", size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), r, fill=255)
    return m


def glass(img: Image.Image, box: tuple[int, int, int, int], r: int = 36,
          tint: int = 34, blur: int = 26) -> None:
    """Liquid-glass panel: backdrop blur + sat lift, white veil, specular sweep,
    inner depth shadow, gradient hairline rim."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    region = img.crop(box).filter(ImageFilter.GaussianBlur(blur))
    from PIL import ImageEnhance
    region = ImageEnhance.Color(region).enhance(1.35)
    region = ImageEnhance.Brightness(region).enhance(1.05)
    if DARK_GLASS:
        # smoked glass for vivid backdrops: keeps white text readable
        region = Image.blend(region, Image.new("RGB", (w, h), (10, 16, 40)), DARK_GLASS)
        region = Image.blend(region, Image.new("RGB", (w, h), WHITE), tint / 255 * 0.5)
    else:
        veil = Image.new("RGB", (w, h), WHITE)
        region = Image.blend(region, veil, tint / 255)
    # specular sweep top-left
    spec = Image.new("L", (w, h), 0)
    sd = ImageDraw.Draw(spec)
    sd.ellipse((-w * 0.35, -h * 0.9, w * 0.75, h * 0.42), fill=34)
    spec = spec.filter(ImageFilter.GaussianBlur(40))
    region.paste(WHITE, (0, 0), spec)
    # inner depth shadow at bottom
    sh = Image.new("L", (w, h), 0)
    ImageDraw.Draw(sh).rectangle((0, int(h * 0.78), w, h), fill=50)
    sh = sh.filter(ImageFilter.GaussianBlur(30))
    region.paste((5, 12, 30), (0, 0), sh)
    mask = rounded_mask((w, h), r)
    # drop shadow
    shadow = Image.new("L", img.size, 0)
    ImageDraw.Draw(shadow).rounded_rectangle((x0 + 6, y0 + 18, x1 + 6, y1 + 18), r, fill=110)
    shadow = shadow.filter(ImageFilter.GaussianBlur(28))
    img.paste((2, 8, 22), (0, 0), shadow)
    img.paste(region, (x0, y0), mask)
    # rim: gradient hairline + top highlight
    rim = Image.new("L", (w, h), 0)
    rd = ImageDraw.Draw(rim)
    rd.rounded_rectangle((0, 0, w - 1, h - 1), r, outline=255, width=2)
    grad = gradient_img((w, h), (120, 200, 255), (110, 235, 175), horizontal=True)
    rim_alpha = rim.point(lambda v: int(v * 0.55))
    img.paste(grad, (x0, y0), rim_alpha)
    hi = Image.new("L", (w, h), 0)
    ImageDraw.Draw(hi).rounded_rectangle((1, 1, w - 2, h - 2), r, outline=255, width=1)
    fade = Image.linear_gradient("L").resize((w, h)).transpose(Image.FLIP_TOP_BOTTOM)
    hi = Image.composite(hi, Image.new("L", (w, h), 0), fade.point(lambda v: 255 if v > 150 else 0))
    img.paste(WHITE, (x0, y0), hi.point(lambda v: int(v * 0.7)))


def pill(img: Image.Image, x: int, y: int, text: str, size: int = 26,
         highlight: bool = False, gradient_fill: bool = False) -> int:
    tw = text_width(text, size)
    pw, ph = tw + size * 1.4, int(size * 1.85)
    pw = int(pw)
    box = (x, y, x + pw, y + ph)
    if gradient_fill:
        g = gradient_img((pw, ph), BLUE, GREEN)
        img.paste(g, (x, y), rounded_mask((pw, ph), ph // 2))
        draw_text(img, (x + pw // 2, y + int(ph * 0.16)), text, size, WHITE, anchor_center=True)
    elif highlight:
        img.paste(WHITE, (x, y), rounded_mask((pw, ph), ph // 2))
        draw_text(img, (x + pw // 2, y + int(ph * 0.16)), text, size, (10, 30, 55), anchor_center=True)
    else:
        glass(img, box, r=ph // 2, tint=26, blur=14)
        draw_text(img, (x + pw // 2, y + int(ph * 0.16)), text, size, WHITE, anchor_center=True)
    return pw


def scrim(img: Image.Image) -> None:
    """Darken centre/lower area so text stays legible over the backdrop."""
    s = Image.linear_gradient("L").resize((W, H))  # 0 top -> 255 bottom
    s = s.point(lambda v: int(SCRIM[0] + v * SCRIM[1]))
    img.paste((4, 10, 26), (0, 0), s)


def chrome(img: Image.Image, tags: Iterable[str]) -> None:
    x = PAD_X
    y = PAD_Y
    for i, t in enumerate(tags):
        x += pill(img, x, y, t, 24, highlight=(i == 0)) + 12
    wm = "Arnfar"
    wx = W - PAD_X - text_width(wm, 40)
    if DARK_GLASS:
        glass(img, (wx - 80, y - 8, W - PAD_X + 18, y + 66), r=37, tint=20, blur=16)
    draw_text(img, (wx, y + 2), wm, 40, gradient=True)
    paste_logo(img, wx - 66, y, 58)


LOGO = ROOT / "arnfar-logo.png"


def paste_logo(img: Image.Image, x: int, y: int, size: int) -> None:
    logo = Image.open(LOGO).convert("RGBA")
    logo = logo.crop(logo.getchannel("A").getbbox())
    logo = logo.resize((size, size), Image.LANCZOS)
    img.paste(logo, (x, y), logo)


def footer(img: Image.Image, hashtags: Sequence[str]) -> None:
    band_h = 96
    by = H - PAD_Y - band_h
    # hashtag pills
    x = PAD_X
    hy = by - 70
    for t in hashtags:
        w = text_width(t, 22) + 30
        if x + w > W - PAD_X:
            break
        x += pill(img, x, hy, t, 22) + 10
    # ad band
    glass(img, (PAD_X, by, W - PAD_X, by + band_h), r=28, tint=30, blur=18)
    # real Arnfar logo (arnfar-icon/arnfar-logo.png)
    paste_logo(img, PAD_X + 18, by + (band_h - 68) // 2, 68)
    tx = PAD_X + 100
    w = draw_text(img, (tx, by + 16), "Arnfar", 30, gradient=True)
    draw_text(img, (tx + w + 10, by + 16), "ERP · ລະບົບບັນຊີ ແລະ ທຸລະກິດ", 28, WHITE)
    draw_text(img, (tx, by + 54), "arnfar.com", 22, INK2)


def check_mark(img: Image.Image, x: int, y: int, s: int, good: bool) -> None:
    box = (x, y, x + s, y + s)
    if good:
        g = gradient_img((s, s), BLUE, GREEN)
        img.paste(g, (x, y), rounded_mask((s, s), s // 2))
        d = ImageDraw.Draw(img)
        d.line([(x + s * .27, y + s * .52), (x + s * .44, y + s * .68), (x + s * .74, y + s * .34)],
               fill=WHITE, width=max(3, s // 9), joint="curve")
    else:
        img.paste((230, 80, 80), (x, y), rounded_mask((s, s), s // 2))
        d = ImageDraw.Draw(img)
        k = s * .3
        d.line([(x + k, y + k), (x + s - k, y + s - k)], fill=WHITE, width=max(3, s // 9))
        d.line([(x + s - k, y + k), (x + k, y + s - k)], fill=WHITE, width=max(3, s // 9))


def dot_badge(img: Image.Image, x: int, y: int, s: int, label: str) -> None:
    g = gradient_img((s, s), BLUE, GREEN)
    img.paste(g, (x, y), rounded_mask((s, s), s // 3))
    draw_text(img, (x + s // 2, y + int(s * 0.17)), label, int(s * 0.5), WHITE, anchor_center=True)


def base(bg: Image.Image, tags: Sequence[str]) -> Image.Image:
    img = bg.copy()
    scrim(img)
    chrome(img, tags)
    return img


# ------------------------------------------------------------------ cards

TAGS = ["OpenSource", "Office", "ເຄື່ອງມື"]
HASH = ["#lomon", "#arnfar", "#OpenSource", "#LibreOffice", "#ONLYOFFICE"]


def card1(bg: Image.Image) -> Image.Image:
    img = base(bg, TAGS)
    # evidence mockup: three app tiles (Docs / Sheets / Slides)
    top = 210
    glass(img, (PAD_X, top, W - PAD_X, top + 430), r=40, tint=22)
    draw_text(img, (PAD_X + 40, top + 32), "WordCraft · GridCraft · DeckCraft", 26, INK2)
    tile_w = (W - 2 * PAD_X - 80 - 40) // 3
    labels = [("Word", "87%", "ribbon"), ("Excel", "89%", "ribbon"), ("PowerPoint", "79%", "features")]
    for i, (name, pct, sub) in enumerate(labels):
        tx = PAD_X + 40 + i * (tile_w + 20)
        ty = top + 90
        glass(img, (tx, ty, tx + tile_w, ty + 300), r=28, tint=30, blur=16)
        d = ImageDraw.Draw(img)
        # mini icon
        ix, iy = tx + 24, ty + 26
        if i == 0:
            for k in range(5):
                d.rounded_rectangle((ix, iy + k * 16, ix + (110 if k % 2 == 0 else 80), iy + k * 16 + 7), 3,
                                    fill=(190, 225, 255))
        elif i == 1:
            for r_ in range(4):
                for c_ in range(4):
                    d.rectangle((ix + c_ * 28, iy + r_ * 20, ix + c_ * 28 + 24, iy + r_ * 20 + 16),
                                fill=(170, 240, 205) if (r_ + c_) % 3 else (90, 210, 150))
        else:
            d.rounded_rectangle((ix, iy, ix + 112, iy + 76), 8, outline=(190, 225, 255), width=3)
            for k, hh in enumerate([22, 38, 54]):
                d.rectangle((ix + 18 + k * 28, iy + 66 - hh, ix + 36 + k * 28, iy + 66), fill=(120, 220, 190))
        draw_text(img, (tx + 24, ty + 130), pct, 64, gradient=True)
        draw_text(img, (tx + 24, ty + 220), f"vs {name}", 24, WHITE)
        draw_text(img, (tx + 24, ty + 254), sub, 20, MUTED)
    draw_text(img, (PAD_X + 40, top + 398 - 6), "* ຕົວເລກທີ່ ArtCraft ລະບຸເອງ · v0.5.0", 20, MUTED)

    # headline band
    y = 720
    draw_text(img, (PAD_X, y), "ທາງເລືອກແທນ Office", 72, WHITE)
    draw_text(img, (PAD_X, y + 104), "Open Source ຟຣີ ມາແຮງ!", 64, gradient=True)
    bar_y = y + 210
    g = gradient_img((6, 84), BLUE, GREEN, horizontal=False)
    img.paste(g, (PAD_X, bar_y))
    draw_text(img, (PAD_X + 26, bar_y), "Word, Excel, PowerPoint ສະບັບ Open Source", 30, (130, 200, 255))
    draw_text(img, (PAD_X + 26, bar_y + 44), "LibreOffice · ONLYOFFICE · Euro-Office", 26, INK2)
    footer(img, HASH)
    return img


def card2(bg: Image.Image) -> Image.Image:
    img = base(bg, TAGS)
    y = 196
    draw_text(img, (PAD_X, y), "4 ເຄື່ອງມືທີ່ຄວນຮູ້ຈັກ", 60, WHITE)
    g = gradient_img((140, 8), BLUE, GREEN)
    img.paste(g, (PAD_X, y + 92), rounded_mask((140, 8), 4))
    items = [
        ("1", "LibreOffice 26.8", "ໃຊ້ offline, ບໍ່ມີ AI, ຮອງຮັບ 120+ ພາສາ", "26 ສິງຫາ 2026"),
        ("2", "ONLYOFFICE 10.0", "ໜ້າຕາຄ້າຍ Office, ແກ້ໄຂພ້ອມກັນເປັນທີມ", "10 ຕຸລາ 2026"),
        ("3", "Euro-Office 1.0", "Office ເທິງເວັບ ຈາກ Nextcloud ແລະ IONOS", "9 ມິຖຸນາ 2026"),
        ("4", "WordCraft · GridCraft · DeckCraft", "ຂຽນໃໝ່ດ້ວຍ Rust · ຍັງເປັນເວີຊັນທົດລອງ", "v0.5.0 · 7 ຕຸລາ 2026"),
    ]
    ry = y + 140
    rh = 158
    for num, name, desc, date in items:
        glass(img, (PAD_X, ry, W - PAD_X, ry + rh), r=30, tint=26, blur=18)
        dot_badge(img, PAD_X + 28, ry + 40, 70, num)
        tx = PAD_X + 124
        draw_text(img, (tx, ry + 22), name, 34, WHITE)
        draw_text(img, (tx, ry + 72), desc, 26, INK2)
        draw_text(img, (tx, ry + 112), date, 21, (120, 210, 175))
        ry += rh + 28
    footer(img, HASH)
    return img


def card3(bg: Image.Image) -> Image.Image:
    img = base(bg, TAGS)
    glass(img, (PAD_X, 200, W - PAD_X, 1010), r=44, tint=24)
    draw_text(img, (W // 2, 250), "GridCraft — ທາງເລືອກແທນ Excel", 34, INK2, anchor_center=True)
    draw_text(img, (W // 2, 318), "93%", 230, gradient=True, anchor_center=True)
    draw_text(img, (W // 2, 640), "ຂອງສູດຄຳນວນ (functions) ໃນ Excel", 40, WHITE, anchor_center=True)
    draw_text(img, (W // 2, 700), "ອີງຕາມຂໍ້ມູນທີ່ ArtCraft ລະບຸເອງ", 26, MUTED, anchor_center=True)
    chips = ["Excel ribbon 89%", "Word ribbon 87%", "PowerPoint 79%"]
    tw = sum(text_width(c, 24) + int(24 * 1.4) for c in chips) + 14 * (len(chips) - 1)
    x = (W - tw) // 2
    for c in chips:
        x += pill(img, x, 790, c, 24) + 14
    bx = (W - text_width("Apache-2.0 / MIT · ຟຣີ", 24) - 34) // 2
    pill(img, bx, 880, "Apache-2.0 / MIT · ຟຣີ", 24, gradient_fill=True)
    footer(img, HASH)
    return img


def card4(bg: Image.Image) -> Image.Image:
    img = base(bg, TAGS)
    y = 196
    draw_text(img, (PAD_X, y), "ກ່ອນປ່ຽນ ຕ້ອງຮູ້ຫຍັງແດ່?", 58, WHITE)
    g = gradient_img((140, 8), BLUE, GREEN)
    img.paste(g, (PAD_X, y + 92), rounded_mask((140, 8), 4))
    rows = [
        (False, "ArtCraft ຍັງເປັນເວີຊັນທົດລອງ", "ກຣາຟ ແລະ SmartArt ຫາຍ ເມື່ອບັນທຶກ DOCX ຄືນ"),
        (False, "ຍັງບໍ່ໄດ້ທົດສອບກັບເອກະສານທຸລະກິດຈິງ", "ຢ່າໃຊ້ກັບເອກະສານທີ່ຕ້ອງສົ່ງລູກຄ້າ"),
        (True, "ໃຊ້ໃນເຄື່ອງ ໝັ້ນຄົງ: LibreOffice", "ເອກະສານບໍ່ອອກນອກເຄື່ອງ"),
        (True, "ເຮັດວຽກເປັນທີມ: ONLYOFFICE", "ຫຼື Euro-Office ເທິງ server ຂອງຕົນເອງ"),
        (True, "ທົດລອງກັບພະແນກດຽວກ່ອນ", "ກວດຟອນລາວ ແລະ ຮູບແບບເອກະສານ"),
    ]
    ry = y + 140
    rh = 124
    for good, t1, t2 in rows:
        glass(img, (PAD_X, ry, W - PAD_X, ry + rh), r=28, tint=26, blur=18)
        check_mark(img, PAD_X + 28, ry + 34, 56, good)
        tx = PAD_X + 108
        draw_text(img, (tx, ry + 18), t1, 31, WHITE)
        draw_text(img, (tx, ry + 66), t2, 24, INK2 if good else (255, 190, 190))
        ry += rh + 20
    footer(img, HASH)
    return img


def load_bg(path: Path | None) -> Image.Image:
    if path and path.exists():
        src = Image.open(path).convert("RGB")
        sw, sh = src.size
        scale = max(W / sw, H / sh)
        src = src.resize((int(sw * scale + 0.5), int(sh * scale + 0.5)), Image.LANCZOS)
        l = (src.width - W) // 2
        t = (src.height - H) // 2
        return src.crop((l, t, l + W, t + H))
    # procedural fallback: navy + blue/green glows
    img = Image.new("RGB", (W, H), (6, 14, 34))
    glow = Image.new("L", (W, H), 0)
    ImageDraw.Draw(glow).ellipse((-300, -300, 600, 600), fill=160)
    img.paste(BLUE, (0, 0), glow.filter(ImageFilter.GaussianBlur(160)))
    glow = Image.new("L", (W, H), 0)
    ImageDraw.Draw(glow).ellipse((500, 800, 1400, 1700), fill=150)
    img.paste(GREEN, (0, 0), glow.filter(ImageFilter.GaussianBlur(170)))
    return img


def main() -> int:
    bg_path = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    out = ROOT / "out"
    out.mkdir(exist_ok=True)
    bg = load_bg(bg_path)
    for i, fn in enumerate([card1, card2, card3, card4], 1):
        p = out / f"arnfar-open-source-office-0{i}.png"
        fn(bg).save(p, optimize=True)
        print(p)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

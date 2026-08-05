#!/usr/bin/env python3
"""Arnfar-branded 1080x1080 FB square graphic for the MCP news report."""
import os
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

from pathlib import Path
REPO_DIR = Path(__file__).resolve().parent.parent
REPO = str(REPO_DIR)
sys.path.insert(0, str(REPO_DIR / "tools"))
from liquid_glass import glass_card
OUT = str(REPO_DIR / "output" / "arnfar-mcp-news.png")
W = H = 1080

BLUE = (3, 148, 241)
GREEN = (21, 198, 122)
INK = (233, 240, 247)
MUTE = (150, 167, 186)

# all card text renders in Arnfar Regular (user preference)
REG = os.path.join(REPO, "font/Arnfar Font Regular.ttf")
BOLD = REG
LOGO = os.path.join(REPO, "arnfar-icon/arnfar-nobg.png")


def font(path, size):
    return ImageFont.truetype(path, size)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def bg_gradient():
    """Diagonal dark blue->green with radial brand glows."""
    base = Image.new("RGB", (W, H))
    px = base.load()
    c0, c1 = (10, 20, 40), (7, 30, 30)
    for y in range(H):
        for x in range(0, W, 2):
            t = (x + y) / (W + H)
            col = lerp(c0, c1, t)
            px[x, y] = col
            if x + 1 < W:
                px[x + 1, y] = col
    # radial glows
    glow = Image.new("RGB", (W, H), (0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([-260, -300, 520, 480], fill=(BLUE[0] // 4, BLUE[1] // 4, BLUE[2] // 4))
    gd.ellipse([W - 520, H - 480, W + 260, H + 300],
               fill=(GREEN[0] // 5, GREEN[1] // 5, GREEN[2] // 5))
    glow = glow.filter(ImageFilter.GaussianBlur(170))
    return Image.blend(base, Image.composite(glow, base, Image.new("L", (W, H), 90)), 0.0) \
        if False else _screen(base, glow)


def _screen(a, b):
    pa, pb = a.load(), b.load()
    out = Image.new("RGB", (W, H))
    po = out.load()
    for y in range(H):
        for x in range(W):
            ra, rb = pa[x, y], pb[x, y]
            po[x, y] = tuple(255 - (255 - ra[i]) * (255 - rb[i]) // 255 for i in range(3))
    return out


def grad_h(w, h, c0=BLUE, c1=GREEN):
    g = Image.new("RGB", (w, h))
    p = g.load()
    for x in range(w):
        col = lerp(c0, c1, x / max(1, w - 1))
        for y in range(h):
            p[x, y] = col
    return g


def rrect_mask(w, h, r):
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], radius=r, fill=255)
    return m


def grad_pill(draw_img, x, y, w, h, r, c0=BLUE, c1=GREEN):
    tile = grad_h(w, h, c0, c1)
    draw_img.paste(tile, (x, y), rrect_mask(w, h, r))


def text_size(font_obj, s):
    b = font_obj.getbbox(s)
    return b[2] - b[0], b[3] - b[1], b[0], b[1]


def grad_text(img, xy, s, font_obj, c0=BLUE, c1=GREEN):
    w, h, ox, oy = text_size(font_obj, s)
    mask = Image.new("L", (w + 4, h + 4), 0)
    ImageDraw.Draw(mask).text((-ox + 2, -oy + 2), s, font=font_obj, fill=255)
    tile = grad_h(w + 4, h + 4, c0, c1)
    img.paste(tile, (xy[0], xy[1]), mask)


def main():
    img = bg_gradient()
    d = ImageDraw.Draw(img)

    M = 84  # margin

    # ---- top bar: logo + wordmark, category pill ----
    logo = Image.open(LOGO).convert("RGBA")
    lh = 66
    lw = int(logo.width * lh / logo.height)
    logo = logo.resize((lw, lh), Image.LANCZOS)
    img.paste(logo, (M, 70), logo)
    d.text((M + lw + 20, 78), "Arnfar", font=font(BOLD, 46), fill=INK)

    pill_f = font(BOLD, 30)
    ptxt = "ຂ່າວເຕັກໂນໂລຊີ"
    pw = text_size(pill_f, ptxt)[0]
    pad = 30
    pill_w, pill_h = pw + pad * 2, 58
    px0 = W - M - pill_w
    grad_pill(img, px0, 76, pill_w, pill_h, pill_h // 2)
    d.text((px0 + pad, 76 + 12), ptxt, font=pill_f, fill=(8, 18, 30))

    # ---- eyebrow ----
    d.text((M, 232), "MODEL CONTEXT PROTOCOL (MCP)", font=font(BOLD, 30),
           fill=GREEN)

    # ---- headline ----
    h1 = font(BOLD, 88)
    LH = 100
    d.text((M, 286), "ການແກ້ໄຂໃຫຍ່ທີ່ສຸດ", font=h1, fill=INK)
    d.text((M, 286 + LH), "ນັບແຕ່ MCP ເປີດໂຕ", font=h1, fill=INK)
    grad_text(img, (M, 286 + 2 * LH), "ປ່ຽນເປັນ Stateless", h1)

    # accent underline
    yU = 286 + 3 * LH + 8
    grad_pill(img, M, yU, 360, 12, 6)

    # ---- subhead ----
    d.text((M, yU + 44), "ໂປຣໂຕຄໍມາດຕະຖານເຊື່ອມຕໍ່ AI ກັບເຄື່ອງມື ແລະ ຂໍ້ມູນ",
           font=font(REG, 34), fill=MUTE)

    # ---- highlight chips ----
    yC = yU + 116
    chips = ["Stateless core", "MCP Apps + Tasks", "Auth ເຂັ້ມຂຶ້ນ"]
    cf = font(BOLD, 30)
    cx = M
    for c in chips:
        cw = text_size(cf, c)[0] + 50
        ch = 64
        glass_card(img, cx, yC, cw, ch, r=18)
        grad_pill(img, cx, yC, 8, ch, 4)
        d.text((cx + 28, yC + 16), c, font=cf, fill=INK)
        cx += cw + 22

    # ---- date strip ----
    yD = yC + 116
    grad_pill(img, M, yD, 14, 78, 7)
    d.text((M + 36, yD - 6), "ສະບັບ 2026-07-28", font=font(BOLD, 46), fill=INK)
    d.text((M + 36, yD + 48), "ປ່ອຍສະບັບສົມບູນ 28 ກໍລະກົດ 2026", font=font(REG, 30),
           fill=MUTE)

    # ---- footer ----
    grad_pill(img, M, H - 116, W - 2 * M, 6, 3)
    d.text((M, H - 92), "ແຫຼ່ງຂໍ້ມູນ: modelcontextprotocol.io",
           font=font(REG, 27), fill=MUTE)
    src = "Linux Foundation · Agentic AI Foundation"
    sw = text_size(font(REG, 27), src)[0]
    d.text((W - M - sw, H - 92), src, font=font(REG, 27), fill=MUTE)

    img.save(OUT)
    print("saved", OUT)


if __name__ == "__main__":
    main()

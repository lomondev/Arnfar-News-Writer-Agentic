#!/usr/bin/env python3
"""Arnfar dark 'AI coding' social card (blue->green), inspired by a reference layout."""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

from pathlib import Path
import sys
REPO_DIR = Path(__file__).resolve().parent.parent
REPO = str(REPO_DIR)
sys.path.insert(0, str(REPO_DIR / "tools"))
from liquid_glass import glass_card
OUT = str(REPO_DIR / "output" / "arnfar-ai-coding.png")
W = H = 1080

BLUE = (3, 148, 241)
GREEN = (21, 198, 122)
INK = (236, 242, 250)
MUTE = (150, 165, 186)
BG0 = (14, 16, 34)
BG1 = (9, 12, 26)

# all card text renders in Arnfar Regular (user preference)
REG = os.path.join(REPO, "font", "Arnfar Font Regular.ttf")
BOLD = REG


def font(p, s):
    return ImageFont.truetype(p, s)


def ts(f, s):
    b = f.getbbox(s)
    return b[2] - b[0], b[3] - b[1], b[0], b[1]


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def grad_h(w, h, c0=BLUE, c1=GREEN):
    w = max(1, w)
    ramp = np.linspace(0, 1, w)[:, None]
    arr = (np.array(c0)[None, :] * (1 - ramp) + np.array(c1)[None, :] * ramp)
    return Image.fromarray(arr.astype(np.uint8)[None].repeat(h, 0), "RGB")


def rrect_mask(w, h, r):
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], radius=r, fill=255)
    return m


def grad_pill(img, x, y, w, h, r, c0=BLUE, c1=GREEN):
    img.paste(grad_h(w, h, c0, c1), (x, y), rrect_mask(w, h, r))


def grad_text(img, xy, s, f, c0=BLUE, c1=GREEN):
    w, h, ox, oy = ts(f, s)
    mask = Image.new("L", (w + 6, h + 6), 0)
    ImageDraw.Draw(mask).text((-ox + 3, -oy + 3), s, font=f, fill=255)
    img.paste(grad_h(w + 6, h + 6, c0, c1), (xy[0], xy[1]), mask)


def orb(img, cx, cy, rad, color, strength=1.0):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    a = np.clip(1 - d / rad, 0, 1) ** 1.6 * strength
    layer = np.zeros((H, W, 4), np.float32)
    layer[..., 0] = color[0]
    layer[..., 1] = color[1]
    layer[..., 2] = color[2]
    layer[..., 3] = a * 255
    ov = Image.fromarray(layer.astype(np.uint8), "RGBA")
    base = img.convert("RGBA")
    base.alpha_composite(ov)
    return base.convert("RGB")


def star(d, cx, cy, r, color, ratio=0.32):
    pts = []
    import math
    for i in range(8):
        ang = math.pi / 2 + i * math.pi / 4
        rr = r if i % 2 == 0 else r * ratio
        pts.append((cx + rr * math.cos(ang), cy - rr * math.sin(ang)))
    d.polygon(pts, fill=color)


def main():
    # background gradient
    yy = np.linspace(0, 1, H)[:, None, None]
    base = (np.array(BG0)[None, None] * (1 - yy) + np.array(BG1)[None, None] * yy)
    base = np.clip(base, 0, 255).astype(np.uint8).repeat(W, axis=1)
    img = Image.fromarray(base, "RGB")

    # faint grid
    grid = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grid)
    for gx in range(0, W, 60):
        gd.line([(gx, 0), (gx, H)], fill=(255, 255, 255, 7), width=1)
    for gy in range(0, H, 60):
        gd.line([(0, gy), (W, gy)], fill=(255, 255, 255, 7), width=1)
    img = Image.alpha_composite(img.convert("RGBA"), grid).convert("RGB")

    # glowing orbs (blue top-left, green bottom-right)
    img = orb(img, 150, 150, 470, BLUE, 0.95)
    img = orb(img, 970, 980, 430, GREEN, 0.95)
    # small inner bright cores
    img = orb(img, 150, 150, 230, lerp(BLUE, (255, 255, 255), 0.25), 0.5)
    img = orb(img, 970, 980, 210, lerp(GREEN, (255, 255, 255), 0.2), 0.5)

    d = ImageDraw.Draw(img, "RGBA")
    M = 70

    # ---- top bar ----
    d.text((M, 86), "ARNFAR", font=font(BOLD, 46), fill=INK)
    pf = font(BOLD, 28)
    cat = "ຂ່າວເຕັກໂນໂລຊີ"
    pw = ts(pf, cat)[0]
    pill_w, pill_h = pw + 56, 60
    px0, py0 = W - M - pill_w, 84
    # liquid-glass pill + gradient border
    glass_card(img, px0, py0, pill_w, pill_h, r=pill_h // 2)
    img.paste(grad_h(pill_w, pill_h), (px0, py0), _ring(pill_w, pill_h, pill_h // 2, 3))
    d = ImageDraw.Draw(img, "RGBA")
    d.text((px0 + 28, py0 + 14), cat, font=pf, fill=INK)

    # ---- headline + underline ----
    hf = font(BOLD, 104)
    d.text((M, 248), "AI ຊ່ວຍຂຽນໂຄດ", font=hf, fill=INK)
    # gradient underline under the first portion
    uw = ts(hf, "AI ຊ່ວຍ")[0]
    grad_pill(img, M, 372, uw, 14, 7)
    d = ImageDraw.Draw(img, "RGBA")
    # ---- subhead ----
    d.text((M, 410), "ນັກຂຽນໂປຣແກຣມຍຸກໃໝ່ ປີ 2026", font=font(REG, 44), fill=MUTE)

    # ---- code editor window (liquid glass) ----
    wx, wy, ww, wh = M, 512, W - 2 * M, 372
    glass_card(img, wx, wy, ww, wh, r=26)
    d = ImageDraw.Draw(img, "RGBA")
    # title bar
    d.rounded_rectangle([wx, wy, wx + ww, wy + 64], radius=26, fill=(255, 255, 255, 14))
    d.rectangle([wx, wy + 40, wx + ww, wy + 64], fill=(0, 0, 0, 0))
    for i, col in enumerate([(255, 95, 87), (254, 188, 46), (40, 200, 64)]):
        d.ellipse([wx + 26 + i * 30, wy + 24, wx + 42 + i * 30, wy + 40], fill=col)
    d.text((wx + 140, wy + 18), "main.go", font=font(REG, 30), fill=(180, 192, 208))
    # separator
    d.line([(wx, wy + 64), (wx + ww, wy + 64)], fill=(255, 255, 255, 22), width=1)

    # code line bars
    GRAY = (120, 134, 154)
    LGRAY = (180, 190, 205)
    rows = [
        [(GREEN, 95), (BLUE, 175), (LGRAY, 120)],
        [(GRAY, 95), (BLUE, 235), (GREEN, 130)],
        [(LGRAY, 140), (BLUE, 150)],
        [(BLUE, 130), (GREEN, 165), (LGRAY, 90), (GRAY, 95)],
        [(GRAY, 95), (LGRAY, 215)],
    ]
    indent = [0, 0, 36, 0, 36]
    bx0, by = wx + 40, wy + 96
    rh, gap = 26, 30
    for r_i, row in enumerate(rows):
        x = bx0 + indent[r_i]
        for col, bw in row:
            d.rounded_rectangle([x, by, x + bw, by + rh], radius=rh // 2, fill=col)
            x += bw + 18
        by += rh + gap
    # cursor block
    d.rounded_rectangle([bx0, by, bx0 + 22, by + rh], radius=4, fill=GREEN)

    # sparkles
    star(d, wx + ww - 150, wy + 150, 34, lerp(BLUE, (255, 255, 255), 0.15))
    star(d, wx + ww - 215, wy + 205, 18, GREEN)

    # AI Agent pill (bottom-right inside window)
    af = font(BOLD, 30)
    atxt = "AI Agent"
    aw = ts(af, atxt)[0] + 92
    ah = 58
    ax, ay = wx + ww - aw - 28, wy + wh - ah - 26
    glass_card(img, ax, ay, aw, ah, r=ah // 2)
    img.paste(grad_h(aw, ah), (ax, ay), _ring(aw, ah, ah // 2, 2))
    d = ImageDraw.Draw(img, "RGBA")
    star(d, ax + 34, ay + ah // 2, 15, GREEN)
    d.text((ax + 56, ay + 13), atxt, font=af, fill=INK)

    # ---- hashtags ----
    d.text((M, 952), "#arnfar  #AICoding  #LaoDev", font=font(BOLD, 48), fill=INK)

    img.save(OUT)
    print("saved", OUT)


def _ring(w, h, r, width):
    """Return an L mask that is the rounded-rect border ring of given width."""
    outer = Image.new("L", (w, h), 0)
    ImageDraw.Draw(outer).rounded_rectangle([0, 0, w - 1, h - 1], radius=r, fill=255)
    inner = Image.new("L", (w, h), 0)
    ImageDraw.Draw(inner).rounded_rectangle(
        [width, width, w - 1 - width, h - 1 - width], radius=max(1, r - width), fill=255)
    from PIL import ImageChops
    return ImageChops.subtract(outer, inner)


if __name__ == "__main__":
    main()

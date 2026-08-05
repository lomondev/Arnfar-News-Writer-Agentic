#!/usr/bin/env python3
"""
arnfar_news_card.py — render modern, on-brand Arnfar news cards from a JSON spec.

Dark "glowing-orb" theme: a deep navy background with a soft blue glow (top-left)
and green glow (bottom-right), a faint grid, blue→green gradient accents, dark
glass cards, and bright legible text. Includes a `code` card kind that draws a
glassy code-editor (main.go) mockup for dev / AI-coding news.

Driven by a JSON spec describing one or more cards derived from a news story.
Each card renders to its own PNG. Facebook sizes by default (1080x1350 portrait;
"square" -> 1080x1080). Lao text is shaped via Pillow's raqm backend.

Usage:
    python3 arnfar_news_card.py spec.json
    python3 arnfar_news_card.py spec.json --outdir /path/to/out

See SKILL.md for the full spec guide.
"""
from __future__ import annotations
import os
import re
import math
import json
import hashlib
import argparse
import numpy as np
from PIL import (Image, ImageDraw, ImageFont, ImageFilter, ImageChops,
                 ImageEnhance)

# ---- brand constants ----
BLUE = (222, 28, 45)
GREEN = (243, 128, 32)
INK = (236, 242, 250)        # bright primary text on dark bg
MUTE = (150, 165, 186)       # secondary text
EYEBROW = (240, 96, 64)     # danger red-orange
GLASS = (17, 23, 44, 210)    # dark translucent card fill
BORDER = (255, 255, 255, 34)
BG0 = (14, 16, 34)
BG1 = (9, 12, 26)

# default branded hashtag footer (every card unless overridden via footer_tags)
DEFAULT_TAGS = "#arnfar   #ArnfarERP   #arnfar.com"

# code-window bar colors
GRAY = (120, 134, 154)
LGRAY = (172, 184, 200)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO = "/sessions/charming-keen-mayer/mnt/Arnfar-AI-Agentic"


def asset(*p):
    return os.path.join(REPO, *p)


BOLD_PATH = asset("font", "Arnfar Font Bold.ttf")
REG_PATH = asset("font", "Arnfar Font Regular.ttf")
LOGO_PATH = asset("arnfar-icon", "arnfar-nobg.png")

# Brand preference: render EVERY string (Latin headings, wordmark, numbers,
# badges — not just Lao) in Arnfar Regular. The Bold face reads too heavy for the
# Arnfar liquid-glass cards. Flip to False to restore Bold for Latin text.
ALL_REGULAR = True
if ALL_REGULAR:
    BOLD_PATH = REG_PATH

_FONT_CACHE: dict = {}


def font(path, size):
    key = (path, size)
    if key not in _FONT_CACHE:
        try:
            _FONT_CACHE[key] = ImageFont.truetype(path, size)
        except OSError:
            _FONT_CACHE[key] = ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
    return _FONT_CACHE[key]


# ---- Lao always renders in the Regular weight ----
# The Arnfar Bold face is too heavy for Lao script (tone marks and vowel
# clusters collide and read poorly), so any string containing Lao codepoints is
# drawn in Arnfar Regular regardless of the weight the caller asked for. This is
# enforced centrally — at font resolution, measurement, and the draw call — so
# every card kind gets it without each call site having to opt in. Latin-only
# strings (product names, commands) keep whatever weight was requested.
_LAO_RE = re.compile(r"[຀-໿]")


def _has_lao(s):
    return isinstance(s, str) and _LAO_RE.search(s) is not None


def _lao_swap(f):
    """Given a loaded font, return the Regular-weight equivalent at the same
    size if it is the Bold face; otherwise return it unchanged."""
    if getattr(f, "path", "") == BOLD_PATH:
        return font(REG_PATH, int(getattr(f, "size", 0) or 0))
    return f


# Route every ImageDraw.text() through a Lao check so mixed and pure-Lao lines
# are shaped in Regular no matter which helper drew them.
_orig_draw_text = ImageDraw.ImageDraw.text


def _lao_aware_text(self, xy, text="", *args, font=None, **kw):
    if font is not None and _has_lao(text):
        font = _lao_swap(font)
    return _orig_draw_text(self, xy, text, *args, font=font, **kw)


ImageDraw.ImageDraw.text = _lao_aware_text


def tsize(f, s):
    # measure with the weight that will actually be drawn (Regular for Lao)
    if _has_lao(s):
        f = _lao_swap(f)
    b = f.getbbox(s)
    return b[2] - b[0], b[3] - b[1], b[0], b[1]


def fit_font(path, s, max_w, start, lo=24):
    if _has_lao(s) and path == BOLD_PATH:
        path = REG_PATH  # Lao is always Regular; fit + return the Regular face
    size = start
    while size > lo:
        if tsize(font(path, size), s)[0] <= max_w:
            return font(path, size)
        size -= 2
    return font(path, lo)


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


def ring_mask(w, h, r, width):
    outer = rrect_mask(w, h, r)
    inner = Image.new("L", (w, h), 0)
    ImageDraw.Draw(inner).rounded_rectangle(
        [width, width, w - 1 - width, h - 1 - width],
        radius=max(1, r - width), fill=255)
    return ImageChops.subtract(outer, inner)


def grad_pill(img, x, y, w, h, r, c0=BLUE, c1=GREEN):
    img.paste(grad_h(w, h, c0, c1), (x, y), rrect_mask(w, h, r))


def grad_border(img, x, y, w, h, r, width=2, c0=BLUE, c1=GREEN, alpha=255):
    mask = ring_mask(w, h, r, width)
    if alpha < 255:
        mask = mask.point(lambda v: int(v * alpha / 255))
    img.paste(grad_h(w, h, c0, c1), (x, y), mask)


def grad_text(img, xy, s, f, c0=BLUE, c1=GREEN):
    w, h, ox, oy = tsize(f, s)
    mask = Image.new("L", (w + 6, h + 6), 0)
    ImageDraw.Draw(mask).text((-ox + 3, -oy + 3), s, font=f, fill=255)
    img.paste(grad_h(w + 6, h + 6, c0, c1), (xy[0], xy[1]), mask)


def _edge_refract(arr, band=22, strength=12.0):
    """Approximate liquid-glass edge lensing: pixels inside an edge band sample
    the backdrop pulled toward the panel center, so orbs/gradients 'bend' at
    the rim like light through thick curved glass. arr is HxWx3 uint8."""
    h, w = arr.shape[:2]
    if h < band * 3 or w < band * 3:
        return arr
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = np.minimum(np.minimum(xx, w - 1 - xx), np.minimum(yy, h - 1 - yy))
    t = np.clip(1.0 - d / band, 0.0, 1.0) ** 2          # 1 at rim -> 0 inside
    cx, cy = (w - 1) / 2.0, (h - 1) / 2.0
    nx, ny = cx - xx, cy - yy
    norm = np.sqrt(nx * nx + ny * ny) + 1e-6
    sx = np.clip(xx + strength * t * nx / norm, 0, w - 1).astype(np.int32)
    sy = np.clip(yy + strength * t * ny / norm, 0, h - 1).astype(np.int32)
    return arr[sy, sx]


def glass_card(img, x, y, w, h, r=22, dark=True):
    """Liquid-glass panel (Apple 'Liquid Glass' style): a deep frosted blur of
    the backdrop with saturation lift so brand orbs glow through, edge
    refraction that bends the background at the rim, a curved top-left
    specular sweep + hot spot, an inner bottom depth shadow, a directional
    specular rim, and the brand blue->green hairline border."""
    x, y, w, h = int(x), int(y), int(w), int(h)

    # 1. Soft drop shadow underneath the card
    shadow = Image.new("RGBA", (w + 48, h + 48), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle(
        [24, 24, 24 + w - 1, 24 + h - 1], radius=r, fill=(0, 0, 0, 110))
    shadow = shadow.filter(ImageFilter.GaussianBlur(18))
    img.paste(shadow, (x - 24, y - 16), shadow)

    # 2. Frosted backdrop: heavy blur + saturation/brightness lift (vivid,
    #    "liquid" glass rather than flat smoke), then edge refraction.
    reg = img.crop((x, y, x + w, y + h)).filter(ImageFilter.GaussianBlur(32))
    reg = ImageEnhance.Color(reg).enhance(1.45)
    reg = ImageEnhance.Brightness(reg).enhance(1.06)
    reg = Image.fromarray(_edge_refract(np.asarray(reg.convert("RGB"))))
    if dark:
        reg = Image.blend(reg, Image.new("RGB", (w, h), (10, 16, 32)), 0.66)
        tint_a = 12
        gloss_max = 42
    else:
        reg = Image.blend(reg, Image.new("RGB", (w, h), (255, 255, 255)), 0.20)
        tint_a = 30
        gloss_max = 95
    mask = rrect_mask(w, h, r)
    img.paste(reg, (x, y), mask)
    # NB: paste an RGB fill with an alpha-scaled mask — pasting an RGBA tint
    # with an explicit mask drops its alpha and floods the panel solid white.
    img.paste(Image.new("RGB", (w, h), (255, 255, 255)), (x, y),
              mask.point(lambda v: v * tint_a // 255))

    # 3. Curved specular sweep from the top-left (radial falloff, not a flat
    #    band) + a small bright hot spot near the corner — the "wet" look.
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    dist = np.sqrt((xx / w) ** 2 + (yy / h * 1.6) ** 2)
    sweep = np.clip(1.0 - dist / 0.85, 0.0, 1.0) ** 2 * gloss_max
    hot = np.exp(-(((xx - w * 0.16) / (w * 0.16)) ** 2
                   + ((yy - h * 0.10) / (h * 0.10)) ** 2)) * 46
    galpha = np.clip(sweep + hot, 0, 255).astype(np.uint8)
    gmask = ImageChops.multiply(Image.fromarray(galpha, "L"), mask)
    img.paste(Image.new("RGB", (w, h), (255, 255, 255)), (x, y), gmask)

    # 4. Inner bottom depth shadow (glass thickness)
    ib = max(6, int(h * 0.10))
    ialpha = np.zeros((h, w), np.float32)
    ialpha[h - ib:, :] = np.linspace(0, 46, ib)[:, None]
    imask = ImageChops.multiply(
        Image.fromarray(ialpha.astype(np.uint8), "L"), mask)
    img.paste(Image.new("RGB", (w, h), (2, 6, 16)), (x, y), imask)

    # 5. Directional specular rim: bright top-left arc, soft elsewhere
    spec = ring_mask(w, h, r, 2)
    rim = np.clip(1.0 - (xx / w + yy / h) / 1.1, 0.18, 1.0) * 120
    rmask = ImageChops.multiply(spec, Image.fromarray(
        rim.astype(np.uint8), "L"))
    img.paste(Image.new("RGB", (w, h), (255, 255, 255)), (x, y), rmask)

    # 6. Brand hairline gradient border (subtle transparency)
    grad_border(img, x, y, w, h, r, 1, alpha=90)


def star(d, cx, cy, r, color, ratio=0.32):
    pts = []
    for i in range(8):
        ang = math.pi / 2 + i * math.pi / 4
        rr = r if i % 2 == 0 else r * ratio
        pts.append((cx + rr * math.cos(ang), cy - rr * math.sin(ang)))
    d.polygon(pts, fill=color)


# ---------- dark glowing-orb background ----------
# background variants — each card gets a distinct on-brand backdrop.
# (grid_style, [orbs]) where each orb is (cx_frac, cy_frac, rad_frac, color, strength)
_BG_VARIANTS = [
    ("lines", [(0.14, 0.12, 0.44, BLUE, 0.95), (0.90, 0.90, 0.42, GREEN, 0.95),
               (0.14, 0.12, 0.22, "blue_w", 0.5), (0.90, 0.90, 0.20, "green_w", 0.5)]),
    ("dots",  [(0.88, 0.14, 0.46, GREEN, 0.9), (0.12, 0.92, 0.44, BLUE, 0.9),
               (0.88, 0.14, 0.22, "green_w", 0.5), (0.12, 0.92, 0.20, "blue_w", 0.5)]),
    ("diag",  [(0.50, 0.06, 0.52, BLUE, 0.85), (0.50, 0.98, 0.50, GREEN, 0.85),
               (0.50, 0.50, 0.30, "blue_w", 0.28)]),
    ("none",  [(0.10, 0.50, 0.40, BLUE, 0.9), (0.95, 0.55, 0.42, GREEN, 0.9),
               (0.52, 0.10, 0.26, "green_w", 0.35)]),
    ("dots",  [(0.16, 0.10, 0.40, GREEN, 0.92), (0.86, 0.94, 0.44, BLUE, 0.92),
               (0.50, 0.50, 0.30, "green_w", 0.25)]),
]


_MOTIF_ALIASES = {"software": "code", "tools": "gear", "tool": "gear",
                  "network": "ai", "neural": "ai", "brain": "ai", "ml": "ai",
                  "security": "shield", "lock": "shield", "launch": "rocket",
                  "cpu": "chip", "data": "chart", "analytics": "chart",
                  "computer": "aicoding", "laptop": "aicoding", "coding": "aicoding",
                  "devcode": "aicoding", "ai-coding": "aicoding", "aicode": "aicoding"}


def _draw_motif(layer, name, cx, cy, S, col, rng):
    """Draw a large faint thematic line-art motif (robot / ai / code / chip /
    gear / cloud / chart / rocket / shield / globe) centred at (cx, cy)."""
    md = ImageDraw.Draw(layer)
    name = _MOTIF_ALIASES.get(name, name)
    a = 82
    c = (col[0], col[1], col[2], a)
    cs = (col[0], col[1], col[2], min(255, a + 44))
    cf = (col[0], col[1], col[2], 52)
    w = max(4, int(S * 0.058))

    if name == "robot":
        md.line([(cx, cy - S * 1.16), (cx, cy - S * 0.86)], fill=c, width=w)
        md.ellipse([cx - S * 0.09, cy - S * 1.30, cx + S * 0.09, cy - S * 1.12], outline=cs, width=w)
        md.rounded_rectangle([cx - S, cy - S * 0.85, cx + S, cy + S * 0.78],
                             radius=int(S * 0.22), outline=c, width=w)
        for ex in (-0.42, 0.42):
            md.ellipse([cx + ex * S - S * 0.17, cy - S * 0.22, cx + ex * S + S * 0.17, cy + S * 0.12],
                       outline=cs, width=w)
            md.ellipse([cx + ex * S - S * 0.055, cy - S * 0.10, cx + ex * S + S * 0.055, cy + S * 0.0], fill=cs)
        for gx in range(4):
            x0 = cx - S * 0.52 + gx * S * 0.33
            md.rounded_rectangle([x0, cy + S * 0.34, x0 + S * 0.22, cy + S * 0.52], radius=3,
                                 outline=c, width=max(2, w - 2))
        md.rounded_rectangle([cx - S * 1.2, cy - S * 0.2, cx - S * 0.98, cy + S * 0.2], radius=6, outline=c, width=w)
        md.rounded_rectangle([cx + S * 0.98, cy - S * 0.2, cx + S * 1.2, cy + S * 0.2], radius=6, outline=c, width=w)
    elif name == "ai":
        cols = []
        for lxf, n in [(-0.92, 3), (0.0, 4), (0.92, 3)]:
            cps = [(cx + lxf * S, cy + (i - (n - 1) / 2) * S * 0.56) for i in range(n)]
            cols.append(cps)
        for li in range(len(cols) - 1):
            for p in cols[li]:
                for q in cols[li + 1]:
                    md.line([p, q], fill=(col[0], col[1], col[2], 30), width=2)
        for cps in cols:
            for p in cps:
                r = S * 0.13
                md.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], outline=cs, width=w)
                md.ellipse([p[0] - r * 0.4, p[1] - r * 0.4, p[0] + r * 0.4, p[1] + r * 0.4], fill=cs)
    elif name == "code":
        md.rounded_rectangle([cx - S, cy - S * 0.82, cx + S, cy + S * 0.82], radius=int(S * 0.1), outline=c, width=w)
        md.line([(cx - S, cy - S * 0.52), (cx + S, cy - S * 0.52)], fill=c, width=max(2, w - 2))
        for dx in (-0.86, -0.72, -0.58):
            md.ellipse([cx + dx * S, cy - S * 0.73, cx + dx * S + S * 0.07, cy - S * 0.66], outline=cs, width=2)
        yy = cy - S * 0.34
        while yy < cy + S * 0.66:
            x0 = cx - S * 0.82 + float(rng.choice([0.0, 0.12, 0.24])) * S
            wln = float(rng.uniform(0.5, 1.5)) * S
            md.rounded_rectangle([x0, yy, min(cx + S * 0.82, x0 + wln), yy + S * 0.07], radius=4, fill=cf)
            yy += S * 0.205
    elif name == "chip":
        md.rounded_rectangle([cx - S * 0.7, cy - S * 0.7, cx + S * 0.7, cy + S * 0.7], radius=int(S * 0.08), outline=c, width=w)
        md.rounded_rectangle([cx - S * 0.42, cy - S * 0.42, cx + S * 0.42, cy + S * 0.42], radius=int(S * 0.06), outline=cs, width=max(2, w - 1))
        for i in range(5):
            t = -0.5 + i * 0.25
            md.line([(cx + t * S, cy - S * 0.7), (cx + t * S, cy - S * 0.92)], fill=c, width=w)
            md.line([(cx + t * S, cy + S * 0.7), (cx + t * S, cy + S * 0.92)], fill=c, width=w)
            md.line([(cx - S * 0.7, cy + t * S), (cx - S * 0.92, cy + t * S)], fill=c, width=w)
            md.line([(cx + S * 0.7, cy + t * S), (cx + S * 0.92, cy + t * S)], fill=c, width=w)
        md.ellipse([cx - S * 0.08, cy - S * 0.08, cx + S * 0.08, cy + S * 0.08], fill=cs)
    elif name == "gear":
        for gx, gy, gs in [(cx - S * 0.3, cy - S * 0.2, S * 0.66), (cx + S * 0.5, cy + S * 0.42, S * 0.42)]:
            for k in range(10):
                ang = 2 * math.pi * k / 10
                md.line([(gx + math.cos(ang) * gs, gy + math.sin(ang) * gs),
                         (gx + math.cos(ang) * gs * 1.24, gy + math.sin(ang) * gs * 1.24)], fill=c, width=w + 2)
            md.ellipse([gx - gs, gy - gs, gx + gs, gy + gs], outline=cs, width=w)
            md.ellipse([gx - gs * 0.36, gy - gs * 0.36, gx + gs * 0.36, gy + gs * 0.36], outline=cs, width=w)
    elif name == "cloud":
        md.ellipse([cx - S, cy - S * 0.1, cx - S * 0.18, cy + S * 0.62], outline=c, width=w)
        md.ellipse([cx - S * 0.52, cy - S * 0.52, cx + S * 0.42, cy + S * 0.5], outline=c, width=w)
        md.ellipse([cx + S * 0.1, cy - S * 0.2, cx + S, cy + S * 0.62], outline=c, width=w)
        md.line([(cx - S * 0.7, cy + S * 0.56), (cx + S * 0.7, cy + S * 0.56)], fill=c, width=w)
        md.line([(cx, cy + S * 0.72), (cx, cy + S * 1.06)], fill=cs, width=w)
    elif name == "chart":
        md.line([(cx - S, cy + S * 0.8), (cx - S, cy - S * 0.8)], fill=c, width=w)
        md.line([(cx - S, cy + S * 0.8), (cx + S, cy + S * 0.8)], fill=c, width=w)
        for i, h in enumerate([0.4, 0.72, 0.55, 0.98]):
            bx = cx - S * 0.66 + i * S * 0.46
            md.rounded_rectangle([bx, cy + S * 0.8 - h * S, bx + S * 0.28, cy + S * 0.8], radius=4, outline=cs, width=w)
    elif name == "rocket":
        md.rounded_rectangle([cx - S * 0.3, cy - S * 0.5, cx + S * 0.3, cy + S * 0.6], radius=int(S * 0.3), outline=c, width=w)
        md.polygon([(cx - S * 0.3, cy - S * 0.38), (cx, cy - S), (cx + S * 0.3, cy - S * 0.38)], outline=cs, width=w)
        md.ellipse([cx - S * 0.14, cy - S * 0.18, cx + S * 0.14, cy + S * 0.1], outline=cs, width=w)
        md.polygon([(cx - S * 0.3, cy + S * 0.2), (cx - S * 0.6, cy + S * 0.62), (cx - S * 0.3, cy + S * 0.56)], outline=c, width=w)
        md.polygon([(cx + S * 0.3, cy + S * 0.2), (cx + S * 0.6, cy + S * 0.62), (cx + S * 0.3, cy + S * 0.56)], outline=c, width=w)
        md.line([(cx, cy + S * 0.6), (cx, cy + S * 0.98)], fill=cs, width=w)
    elif name == "shield":
        md.line([(cx - S * 0.8, cy - S * 0.68), (cx, cy - S * 0.92), (cx + S * 0.8, cy - S * 0.68),
                 (cx + S * 0.8, cy + S * 0.12), (cx, cy + S), (cx - S * 0.8, cy + S * 0.12),
                 (cx - S * 0.8, cy - S * 0.68)], fill=c, width=w, joint="curve")
        md.line([(cx - S * 0.3, cy + S * 0.02), (cx - S * 0.05, cy + S * 0.3), (cx + S * 0.42, cy - S * 0.3)],
                fill=cs, width=w + 1, joint="curve")
    elif name == "globe":
        md.ellipse([cx - S, cy - S, cx + S, cy + S], outline=c, width=w)
        md.line([(cx - S, cy), (cx + S, cy)], fill=c, width=max(2, w - 2))
        md.ellipse([cx - S * 0.45, cy - S, cx + S * 0.45, cy + S], outline=c, width=max(2, w - 2))
        for yf in (-0.5, 0.5):
            md.line([(cx - S * 0.87, cy + yf * S), (cx + S * 0.87, cy + yf * S)], fill=c, width=max(2, w - 2))
    elif name == "aicoding":
        # laptop screen with code + an AI sparkle (computer / AI coding)
        sx0, sy0, sx1, sy1 = cx - S, cy - S * 0.80, cx + S, cy + S * 0.16
        md.rounded_rectangle([sx0, sy0, sx1, sy1], radius=int(S * 0.07), outline=c, width=w)
        # code lines on screen
        yy = sy0 + S * 0.16
        pal = [cf, (col[0], col[1], col[2], 64)]
        while yy < sy1 - S * 0.12:
            ind = float(rng.choice([0.0, 0.14, 0.26])) * S
            x0 = sx0 + S * 0.14 + ind
            wln = float(rng.uniform(0.4, 1.3)) * S
            md.rounded_rectangle([x0, yy, min(sx1 - S * 0.14, x0 + wln), yy + S * 0.05],
                                 radius=3, fill=pal[int(rng.integers(0, 2))])
            yy += S * 0.135
        # prompt caret
        md.rounded_rectangle([sx0 + S * 0.14, yy, sx0 + S * 0.22, yy + S * 0.05], radius=3, fill=cs)
        # laptop base / keyboard deck
        md.polygon([(sx0, sy1), (sx1, sy1), (cx + S * 1.28, cy + S * 0.5),
                    (cx - S * 1.28, cy + S * 0.5)], outline=c, width=w)
        md.line([(cx - S * 0.16, cy + S * 0.33), (cx + S * 0.16, cy + S * 0.33)], fill=c, width=w)
        # AI sparkles (top-right of screen)
        star(md, sx1 - S * 0.18, sy0 + S * 0.20, S * 0.15, cs)
        star(md, sx1 - S * 0.36, sy0 + S * 0.38, S * 0.08, c)


def _bg_decor(img, seed, variant, motif=None):
    """Cinematic, multi-layer TECH backdrop with depth, behind the glass.

    Layers back→front: (1) far perspective grid (atmospheric perspective),
    (2) volumetric light rays from the scene's light source, (3) a mid-ground
    circuit-trace network with nodes (tech motif), (4) accent rings + sparkles,
    (5) large out-of-focus bokeh discs framing the foreground (depth of field).
    Elements are biased to the side rails / top / bottom, leaving the centre as
    negative space for headline and cards."""
    W, H = img.size
    rng = np.random.default_rng(seed * 131 + 9)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    lights = [(0.14, 0.12), (0.86, 0.16), (0.50, 0.06), (0.10, 0.50), (0.16, 0.10)]
    lx, ly = lights[variant % len(lights)]
    lx, ly = lx * W, ly * H

    def near_center(x, y):
        return 0.30 * W < x < 0.70 * W and 0.24 * H < y < 0.78 * H

    # (1) FAR — perspective grid converging to a vanishing point (low-contrast)
    far = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    fd = ImageDraw.Draw(far)
    vpx, vpy = W * 0.5, H * 0.34
    for i in range(1, 13):
        t = i / 12
        y = vpy + (H - vpy) * t ** 1.7
        fd.line([(0, y), (W, y)], fill=(120, 150, 205, int(6 + 11 * t)), width=1)
    for k in range(-7, 8):
        fd.line([(vpx, vpy), (vpx + k * W * 0.155, H)], fill=(120, 150, 205, 7), width=1)
    ov.alpha_composite(far.filter(ImageFilter.GaussianBlur(1.1)))

    # (2) VOLUMETRIC light rays fanning from the light source
    rays = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    rd = ImageDraw.Draw(rays)
    base_ang = math.atan2(H * 0.5 - ly, W * 0.5 - lx)
    rcol = lerp(BLUE, (255, 255, 255), 0.5)
    for k in range(-3, 4):
        a = base_ang + k * 0.16
        spread = 0.05
        far_len = max(W, H) * 1.4
        p1 = (lx + far_len * math.cos(a - spread), ly + far_len * math.sin(a - spread))
        p2 = (lx + far_len * math.cos(a + spread), ly + far_len * math.sin(a + spread))
        rd.polygon([(lx, ly), p1, p2], fill=(rcol[0], rcol[1], rcol[2], 14))
    ov.alpha_composite(rays.filter(ImageFilter.GaussianBlur(34)))

    # (3) MID — circuit-trace network on the side rails (perspective scaling: the
    # lower a node, the larger/brighter it is)
    mid = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    md = ImageDraw.Draw(mid)
    nodes = []
    for _ in range(16):
        side = rng.random() < 0.5
        x = rng.uniform(0.02, 0.20) * W if side else rng.uniform(0.80, 0.98) * W
        y = rng.uniform(0.06, 0.96) * H
        if near_center(x, y):
            continue
        depth = y / H
        nodes.append((x, y, 3 + depth * 5, int(50 + depth * 70)))
    ncol = lerp(BLUE, GREEN, 0.4)
    for (x, y, r, a) in nodes:
        for (x2, y2, r2, a2) in nodes:
            if x2 <= x:
                continue
            d = math.hypot(x2 - x, y2 - y)
            if d < W * 0.26 and rng.random() < 0.5:
                bend = (x2, y)  # right-angle (manhattan) trace = circuit look
                ta = int(min(a, a2) * 0.5)
                md.line([(x, y), bend, (x2, y2)], fill=(ncol[0], ncol[1], ncol[2], ta), width=2)
                md.ellipse([bend[0] - 4, bend[1] - 4, bend[0] + 4, bend[1] + 4],
                           fill=(ncol[0], ncol[1], ncol[2], ta + 20))
    for (x, y, r, a) in nodes:
        md.ellipse([x - r, y - r, x + r, y + r], fill=(ncol[0], ncol[1], ncol[2], a))
        md.ellipse([x - r - 5, y - r - 5, x + r + 5, y + r + 5],
                   outline=(ncol[0], ncol[1], ncol[2], a // 3), width=2)
    ov.alpha_composite(mid.filter(ImageFilter.GaussianBlur(0.5)))

    # (3b) thematic motif — a large faint scene element (robot/ai/code/chip/...)
    if motif:
        mcx, mcy, S = W * 0.75, H * 0.30, W * 0.185
        mcol = lerp(BLUE, GREEN, 0.5 if (seed % 2) else 0.2)
        add_glow(img, int(mcx), int(mcy), int(S * 2.8), mcol, 0.17)
        mlayer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        _draw_motif(mlayer, str(motif).lower(), mcx, mcy, S, mcol,
                    np.random.default_rng(seed * 211 + 3))
        ov.alpha_composite(mlayer.filter(ImageFilter.GaussianBlur(0.6)))

    # (4) accent rings near the light corner + sparkles (kept light)
    acc = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ad = ImageDraw.Draw(acc)
    rc = BLUE if rng.random() < 0.5 else GREEN
    for i, r in enumerate(range(120, 360, 64)):
        ad.ellipse([lx - r, ly - r, lx + r, ly + r],
                   outline=(rc[0], rc[1], rc[2], max(9, 34 - i * 7)), width=2)
    for _ in range(8):
        sx, sy = rng.uniform(0, 1) * W, rng.uniform(0, 0.94) * H
        if near_center(sx, sy) and rng.random() < 0.7:
            continue
        star(ad, sx, sy, rng.uniform(5, 12), (255, 255, 255, int(rng.integers(45, 120))))
    ov.alpha_composite(acc)

    # (5) FOREGROUND bokeh — big out-of-focus discs hugging the edges (DOF frame)
    bok = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(bok)
    spots = [(-0.04, 0.10), (1.03, 0.30), (0.04, 0.93), (0.97, 0.88), (0.5, 1.04)]
    for fxf, fyf in spots:
        bx, by = fxf * W, fyf * H
        br = rng.uniform(0.10, 0.20) * W
        bc = GREEN if rng.random() < 0.5 else BLUE
        bd.ellipse([bx - br, by - br, bx + br, by + br], fill=(bc[0], bc[1], bc[2], 46))
        bd.ellipse([bx - br, by - br, bx + br, by + br], outline=(bc[0], bc[1], bc[2], 70), width=6)
    ov.alpha_composite(bok.filter(ImageFilter.GaussianBlur(26)))

    img.paste(ov, (0, 0), ov)


def background(W, H, seed=0, motif=None):
    variant = (max(0, seed - 1)) % len(_BG_VARIANTS)
    grid_style, orbs = _BG_VARIANTS[variant]

    yy = np.linspace(0, 1, H)[:, None, None]
    base = (np.array(BG0)[None, None] * (1 - yy) + np.array(BG1)[None, None] * yy)
    img = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8).repeat(W, 1), "RGB")

    grid = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grid)
    if grid_style == "lines":
        for gx in range(0, W, 60):
            gd.line([(gx, 0), (gx, H)], fill=(255, 255, 255, 7), width=1)
        for gy in range(0, H, 60):
            gd.line([(0, gy), (W, gy)], fill=(255, 255, 255, 7), width=1)
    elif grid_style == "dots":
        for gx in range(30, W, 56):
            for gy in range(30, H, 56):
                gd.ellipse([gx, gy, gx + 2, gy + 2], fill=(255, 255, 255, 16))
    elif grid_style == "diag":
        for off in range(-H, W, 70):
            gd.line([(off, 0), (off + H, H)], fill=(255, 255, 255, 6), width=1)
    img = Image.alpha_composite(img.convert("RGBA"), grid).convert("RGB")

    yg, xg = np.mgrid[0:H, 0:W].astype(np.float32)

    def orb(im, cx, cy, rad, color, strength):
        if color == "blue_w":
            color = lerp(BLUE, (255, 255, 255), 0.25)
        elif color == "green_w":
            color = lerp(GREEN, (255, 255, 255), 0.2)
        dist = np.sqrt((xg - cx) ** 2 + (yg - cy) ** 2)
        a = np.clip(1 - dist / rad, 0, 1) ** 1.6 * strength
        layer = np.zeros((H, W, 4), np.float32)
        layer[..., :3] = color
        layer[..., 3] = a * 255
        b = im.convert("RGBA")
        b.alpha_composite(Image.fromarray(layer.astype(np.uint8), "RGBA"))
        return b.convert("RGB")

    for (cxf, cyf, radf, color, strength) in orbs:
        img = orb(img, cxf * W, cyf * H, radf * W, color, strength)
    _bg_decor(img, seed, variant, motif)
    return img


def top_bar(img, d, M, brand, category, tags=None):
    W = img.width
    # top-left: a 3-pill tag row (first highlighted) — else a single category pill
    if tags:
        pf = font(BOLD_PATH, 26)
        px, ph = M, 56
        for i, t in enumerate(tags[:3]):
            pw = tsize(pf, t)[0] + 44
            if i == 0:
                d.rounded_rectangle([px, 74, px + pw, 74 + ph], radius=ph // 2,
                                    fill=(240, 245, 252))
                d.text((px + 22, 74 + 13), t, font=pf, fill=(20, 28, 46))
            else:
                d.rounded_rectangle([px, 74, px + pw, 74 + ph], radius=ph // 2,
                                    fill=(34, 42, 64, 235))
                d.text((px + 22, 74 + 13), t, font=pf, fill=INK)
            px += pw + 14
    elif category:
        pf = font(BOLD_PATH, 28)
        pw = tsize(pf, category)[0]
        pill_w, pill_h, pad = pw + 56, 60, 28
        d.rounded_rectangle([M, 72, M + pill_w, 72 + pill_h],
                            radius=pill_h // 2, fill=(255, 255, 255, 16))
        grad_border(img, M, 72, pill_w, pill_h, pill_h // 2, 3)
        d.text((M + pad, 72 + 15), category, font=pf, fill=INK)
    # logo + wordmark — top-right
    bf = font(BOLD_PATH, 44)
    bw = tsize(bf, brand)[0]
    if os.path.exists(LOGO_PATH):
        logo = Image.open(LOGO_PATH).convert("RGBA")
        lh = 64
        lw = max(1, int(logo.width * lh / logo.height))
        logo = logo.resize((lw, lh), Image.LANCZOS)
        gx = W - M - (lw + 18 + bw)
        img.paste(logo, (gx, 70), logo)
        d.text((gx + lw + 18, 78), brand, font=bf, fill=INK)
    else:
        d.text((W - M - bw, 78), brand, font=bf, fill=INK)


def footer(img, d, M, tags):
    """Branded hashtag sign-off, centered, on every card."""
    H, W = img.height, img.width
    grad_pill(img, M, H - 112, W - 2 * M, 6, 3)
    if not tags:
        return
    tf = fit_font(BOLD_PATH, tags, W - 2 * M, start=38, lo=24)
    tw = tsize(tf, tags)[0]
    d.text(((W - tw) // 2, H - 86), tags, font=tf, fill=INK)


def draw_marker(d, cx, cy, mark, r=20):
    if mark == "check":
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GREEN)
        d.line([(cx - r * 0.45, cy + r * 0.02), (cx - r * 0.10, cy + r * 0.42),
                (cx + r * 0.50, cy - r * 0.42)], fill=(10, 22, 30), width=4,
               joint="curve")
    elif mark == "cross":
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(232, 92, 92))
        o = r * 0.42
        d.line([(cx - o, cy - o), (cx + o, cy + o)], fill=(255, 255, 255), width=4)
        d.line([(cx - o, cy + o), (cx + o, cy - o)], fill=(255, 255, 255), width=4)
    else:
        d.ellipse([cx - r * 0.55, cy - r * 0.55, cx + r * 0.55, cy + r * 0.55], fill=BLUE)


def wrap(text, f, max_w):
    words = text.split(" ")
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if tsize(f, trial)[0] <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# ---------- code-editor mockup ----------
def draw_code_window(img, d, wx, wy, ww, wh, seed, file="main.go", badge="AI Agent"):
    glass_card(img, wx, wy, ww, wh, r=26, dark=True)
    # title bar tint + traffic lights + filename
    d.rounded_rectangle([wx, wy, wx + ww, wy + 64], radius=26, fill=(255, 255, 255, 14))
    d.rectangle([wx, wy + 40, wx + ww, wy + 64], fill=(0, 0, 0, 0))
    for i, col in enumerate([(255, 95, 87), (254, 188, 46), (40, 200, 64)]):
        d.ellipse([wx + 26 + i * 30, wy + 24, wx + 42 + i * 30, wy + 40], fill=col)
    d.text((wx + 140, wy + 18), file, font=font(REG_PATH, 30), fill=(180, 192, 208))
    d.line([(wx, wy + 64), (wx + ww, wy + 64)], fill=(255, 255, 255, 22), width=1)

    rng = np.random.default_rng(int(hashlib.md5(str(seed).encode()).hexdigest(), 16)
                                % (2 ** 32))
    palette = [GREEN, BLUE, GRAY, LGRAY, BLUE, GREEN]
    bx0, by = wx + 40, wy + 96
    rh, gap = 26, 30
    avail_w = ww - 110
    n_rows = max(3, (wh - 96 - rh) // (rh + gap))
    for _ in range(int(n_rows)):
        indent = int(rng.choice([0, 0, 36, 54]))
        x = bx0 + indent
        budget = avail_w - indent
        segs = int(rng.integers(2, 5))
        for _s in range(segs):
            if budget < 90:
                break
            bw = int(rng.integers(80, max(110, min(260, budget))))
            col = palette[int(rng.integers(0, len(palette)))]
            d.rounded_rectangle([x, by, x + bw, by + rh], radius=rh // 2, fill=col)
            x += bw + 18
            budget -= bw + 18
        by += rh + gap
    # cursor
    d.rounded_rectangle([bx0, by, bx0 + 22, by + rh], radius=4, fill=GREEN)

    # sparkles
    star(d, wx + ww - 150, wy + 140, 32, lerp(BLUE, (255, 255, 255), 0.15))
    star(d, wx + ww - 212, wy + 192, 17, GREEN)

    # badge pill
    if badge:
        af = font(BOLD_PATH, 30)
        aw = tsize(af, badge)[0] + 92
        ah = 58
        ax, ay = wx + ww - aw - 28, wy + wh - ah - 26
        d.rounded_rectangle([ax, ay, ax + aw, ay + ah], radius=ah // 2,
                            fill=(10, 22, 30, 205))
        grad_border(img, ax, ay, aw, ah, ah // 2, 2)
        star(d, ax + 34, ay + ah // 2, 15, GREEN)
        d.text((ax + 56, ay + 13), badge, font=af, fill=INK)


# ---------- showcase helpers (chart + solar-system illustration) ----------
def _rot_text(s, f, fill, angle):
    w, h, ox, oy = tsize(f, s)
    im = Image.new("RGBA", (w + 6, h + 6), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((-ox + 3, -oy + 3), s, font=f, fill=fill)
    return im.rotate(angle, expand=True, resample=Image.BICUBIC)


def _starfield(img, seed, n=170):
    rng = np.random.default_rng(seed * 7 + 11)
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    dr = ImageDraw.Draw(layer)
    for _ in range(n):
        x = rng.integers(0, img.width)
        y = rng.integers(0, int(img.height * 0.72))
        r = rng.choice([1, 1, 1, 2])
        a = int(rng.integers(35, 190))
        dr.ellipse([x, y, x + r, y + r], fill=(255, 255, 255, a))
    img.paste(layer, (0, 0), layer)


def add_glow(img, cx, cy, rad, color, strength):
    yg, xg = np.mgrid[0:img.height, 0:img.width].astype(np.float32)
    a = np.clip(1 - np.sqrt((xg - cx) ** 2 + (yg - cy) ** 2) / rad, 0, 1) ** 1.8
    a = np.clip(a * strength, 0, 1)
    img.paste(Image.new("RGB", img.size, tuple(color)), (0, 0),
              Image.fromarray((a * 255).astype(np.uint8), "L"))


_SPHERE = {
    "sun":   ((255, 238, 162), (231, 116, 18)),
    "earth": ((118, 200, 236), (12, 70, 150)),
    "moon":  ((226, 229, 238), (118, 126, 142)),
}


def make_sphere(size, kind, seed=0):
    size = int(size)
    r = size / 2.0
    yy, xx = np.mgrid[0:size, 0:size].astype(np.float32)
    dx = (xx - r) / r
    dy = (yy - r) / r
    d2 = dx * dx + dy * dy
    dist = np.sqrt(d2)
    light, dark = _SPHERE.get(kind, ((118, 200, 236), (12, 70, 150)))
    arr = np.zeros((size, size, 4), np.float32)
    if kind == "sun":
        t = np.clip(dist, 0, 1) ** 1.3
        for i in range(3):
            arr[..., i] = light[i] + (dark[i] - light[i]) * t
    else:
        nz = np.sqrt(np.clip(1.0 - d2, 0, 1))
        lx, ly = -0.45, -0.55
        lz = math.sqrt(max(0.0, 1 - lx * lx - ly * ly))
        lam = np.clip(dx * lx + dy * ly + nz * lz, 0, 1)
        shade = 0.20 + 0.92 * lam
        for i in range(3):
            arr[..., i] = np.clip(dark[i] + (light[i] - dark[i]) * shade, 0, 255)
        spec = np.clip(lam, 0, 1) ** 12
        for i in range(3):
            arr[..., i] = np.clip(arr[..., i] + spec * 110, 0, 255)
        rng = np.random.default_rng(seed * 13 + hash(kind) % 1000)
        yyy, xxx = np.mgrid[0:size, 0:size]
        if kind == "earth":
            for _ in range(7):
                bx, by = rng.uniform(0.2, 0.8) * size, rng.uniform(0.2, 0.8) * size
                br = rng.uniform(0.07, 0.17) * size
                m = (((xxx - bx) ** 2 + (yyy - by) ** 2) <= br * br) & (dist <= 0.95)
                tone = (0.35 + 0.9 * lam)
                for i in range(3):
                    arr[..., i] = np.where(m, np.clip(GREEN[i] * tone, 0, 255), arr[..., i])
        elif kind == "moon":
            for _ in range(10):
                bx, by = rng.uniform(0.18, 0.82) * size, rng.uniform(0.18, 0.82) * size
                br = rng.uniform(0.03, 0.09) * size
                m = (((xxx - bx) ** 2 + (yyy - by) ** 2) <= br * br) & (dist <= 0.93)
                arr[..., :3] = np.where(m[..., None], arr[..., :3] * 0.78, arr[..., :3])
    feather = 2.5 / r
    arr[..., 3] = np.clip((1.0 - dist) / feather, 0, 1) * 255
    return Image.fromarray(arr.astype(np.uint8), "RGBA")


def paste_sphere(img, cx, cy, r, kind, seed=0):
    if kind == "sun":
        add_glow(img, cx, cy, r * 2.7, (250, 150, 44), 0.85)
    sp = make_sphere(r * 2, kind, seed)
    img.paste(sp, (int(cx - r), int(cy - r)), sp)


def _center_label(img, d, cx, cy, text, fsize):
    f = font(BOLD_PATH, fsize)
    w, h, ox, oy = tsize(f, text)
    x, y = cx - w / 2 - ox, cy - h / 2 - oy
    d.text((x + 2, y + 2), text, font=f, fill=(0, 0, 0, 150))
    d.text((x, y), text, font=f, fill=INK)


def _digit_globe(d, cx, cy, r, seed):
    rng = np.random.default_rng(seed * 17 + 5)
    f = font(REG_PATH, 18)
    step = 21
    for gy in range(int(cy - r), int(cy + r), step):
        for gx in range(int(cx - r), int(cx + r), step):
            if (gx - cx) ** 2 + (gy - cy) ** 2 > r * r:
                continue
            ch = rng.choice(["5", "6"])
            if rng.random() < 0.22:
                col = (52, 178, 116, int(rng.integers(40, 130)))
            else:
                col = (214, 96, 46, int(rng.integers(35, 135)))
            d.text((gx, gy), ch, font=f, fill=col)


def _bottom_gradient(img, top):
    W, H = img.width, img.height
    band = H - top
    t = np.linspace(0, 1, band)[:, None]
    c0, c1 = np.array((14, 18, 40)), np.array((38, 64, 150))
    rgb = (c0 * (1 - t) + c1 * t)
    arr = np.zeros((band, W, 4), np.uint8)
    arr[..., :3] = rgb[:, None, :].astype(np.uint8)
    arr[..., 3] = (np.clip(np.linspace(0, 1, band) ** 1.2, 0, 1) * 240)[:, None].astype(np.uint8)
    layer = Image.fromarray(arr, "RGBA")
    img.paste(layer, (0, top), layer)


def _draw_bar_chart(img, d, x, y, w, h, chart, seed):
    title = chart.get("title", "")
    bars = chart.get("bars", [])
    legend = chart.get("legend", [])
    unit = chart.get("unit", "%")
    pad_l, pad_r, pad_t, pad_b = 66, 22, 124, 98
    if title:
        d.text((x + 28, y + 20), title, font=font(BOLD_PATH, 28), fill=INK)
    if legend:
        lf = font(BOLD_PATH, 21)
        lx = x + 28
        ly = y + 62
        for i, lg in enumerate(legend):
            lw = tsize(lf, lg)[0] + 32
            lh = 38
            if i == 0:
                d.rounded_rectangle([lx, ly, lx + lw, ly + lh],
                                    radius=lh // 2, fill=(238, 244, 252))
                d.text((lx + 16, ly + 8), lg, font=lf, fill=(20, 28, 46))
            else:
                d.rounded_rectangle([lx, ly, lx + lw, ly + lh],
                                    radius=lh // 2, fill=(255, 255, 255, 34))
                d.text((lx + 16, ly + 8), lg, font=lf, fill=INK)
            lx += lw + 12
    px0, px1 = x + pad_l, x + w - pad_r
    py0, py1 = y + pad_t, y + h - pad_b
    maxv = float(chart.get("max", 100))
    tf = font(REG_PATH, 22)
    for tick in (0, 25, 50, 75):
        ty = py1 - (tick / maxv) * (py1 - py0)
        d.line([(px0, ty), (px1, ty)], fill=(255, 255, 255, 24), width=1)
        lab = f"{tick}%"
        lw, lh = tsize(tf, lab)[:2]
        d.text((px0 - 12 - lw, ty - lh // 2 - 4), lab, font=tf, fill=MUTE)
    sc = _rot_text("Score", font(REG_PATH, 22), MUTE, 90)
    img.paste(sc, (int(x + 6), int((py0 + py1) // 2 - sc.height // 2)), sc)
    n = max(1, len(bars))
    slot = (px1 - px0) / n
    bw = slot * 0.52
    vf = font(BOLD_PATH, 26)
    lblf = font(REG_PATH, 21)
    for i, bar in enumerate(bars):
        val = float(bar.get("value", 0))
        bx = px0 + slot * i + (slot - bw) / 2
        bh = (val / maxv) * (py1 - py0)
        by = py1 - bh
        color = bar.get("color")
        if not color:
            color = ("grad" if bar.get("highlight")
                     else "dark" if bar.get("muted") else "light")
        if color == "grad":
            grad_pill(img, int(bx), int(by), int(bw), max(2, int(bh)), 10)
        elif color == "dark":
            d.rounded_rectangle([bx, by, bx + bw, by + bh], radius=10, fill=(64, 72, 92))
        else:
            d.rounded_rectangle([bx, by, bx + bw, by + bh], radius=10, fill=(232, 239, 248))
        vs = bar.get("value_label", f"{val:g}{unit}")
        vw = tsize(vf, vs)[0]
        d.text((bx + bw / 2 - vw / 2, by - 34), vs, font=vf, fill=INK)
        lab = bar.get("label", "")
        if lab:
            ti = _rot_text(lab, lblf, MUTE, 20)
            img.paste(ti, (int(bx + bw / 2 - ti.width * 0.34), int(py1 + 14)), ti)


# ---------- feature-card helpers (mockups, icons, chips, badges) ----------
def _particles(img, seed, n=70):
    rng = np.random.default_rng(seed * 5 + 3)
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    dr = ImageDraw.Draw(layer)
    for _ in range(n):
        x = int(rng.integers(0, img.width))
        y = int(rng.integers(0, img.height))
        r = int(rng.choice([2, 3, 4, 6]))
        base = BLUE if rng.random() < 0.5 else GREEN
        col = lerp(base, (255, 255, 255), 0.3)
        a = int(rng.integers(26, 110))
        dr.ellipse([x, y, x + r, y + r], fill=(col[0], col[1], col[2], a))
    layer = layer.filter(ImageFilter.GaussianBlur(0.6))
    img.paste(layer, (0, 0), layer)


def _grad_circle(img, cx, cy, r):
    em = Image.new("L", (r * 2, r * 2), 0)
    ImageDraw.Draw(em).ellipse([0, 0, r * 2 - 1, r * 2 - 1], fill=255)
    img.paste(grad_h(r * 2, r * 2), (int(cx - r), int(cy - r)), em)


def _icon(d, x, y, s, name, color=INK):
    cx, cy = x + s / 2, y + s / 2
    lw = max(2, int(s * 0.11))
    if name == "play":
        d.polygon([(x + s * 0.32, y + s * 0.22), (x + s * 0.32, y + s * 0.78),
                   (x + s * 0.80, y + s * 0.5)], fill=color)
    elif name == "bolt":
        d.polygon([(x + s * 0.56, y + s * 0.06), (x + s * 0.24, y + s * 0.56),
                   (x + s * 0.47, y + s * 0.56), (x + s * 0.42, y + s * 0.94),
                   (x + s * 0.78, y + s * 0.42), (x + s * 0.53, y + s * 0.42)], fill=color)
    elif name == "code":
        d.line([(x + s * 0.36, y + s * 0.26), (x + s * 0.16, y + s * 0.5),
                (x + s * 0.36, y + s * 0.74)], fill=color, width=lw, joint="curve")
        d.line([(x + s * 0.64, y + s * 0.26), (x + s * 0.84, y + s * 0.5),
                (x + s * 0.64, y + s * 0.74)], fill=color, width=lw, joint="curve")
        d.line([(x + s * 0.57, y + s * 0.20), (x + s * 0.43, y + s * 0.80)],
               fill=color, width=lw)
    elif name == "check":
        d.line([(x + s * 0.20, y + s * 0.52), (x + s * 0.42, y + s * 0.74),
                (x + s * 0.82, y + s * 0.26)], fill=color, width=lw + 1, joint="curve")
    elif name == "globe":
        d.ellipse([x + s * 0.12, y + s * 0.12, x + s * 0.88, y + s * 0.88],
                  outline=color, width=lw)
        d.line([(x + s * 0.12, cy), (x + s * 0.88, cy)], fill=color, width=max(1, lw - 1))
        d.ellipse([x + s * 0.34, y + s * 0.12, x + s * 0.66, y + s * 0.88],
                  outline=color, width=max(1, lw - 1))
    elif name == "lock":
        d.rounded_rectangle([x + s * 0.24, y + s * 0.46, x + s * 0.76, y + s * 0.86],
                            radius=int(s * 0.08), fill=color)
        d.arc([x + s * 0.30, y + s * 0.14, x + s * 0.70, y + s * 0.64], 180, 360,
              fill=color, width=lw)
    elif name == "layers":
        d.polygon([(cx, y + s * 0.16), (x + s * 0.84, y + s * 0.38), (cx, y + s * 0.60),
                   (x + s * 0.16, y + s * 0.38)], outline=color, width=lw)
        d.line([(x + s * 0.16, y + s * 0.54), (cx, y + s * 0.76),
                (x + s * 0.84, y + s * 0.54)], fill=color, width=lw, joint="curve")
    elif name == "chart":
        for i, hh in enumerate([0.30, 0.55, 0.42]):
            bx = x + s * (0.22 + i * 0.22)
            d.rectangle([bx, y + s * (0.80 - hh), bx + s * 0.13, y + s * 0.80], fill=color)
    elif name in ("spark", "sparkle", "star"):
        star(d, cx, cy, s * 0.42, color)
    elif name == "doc":
        d.rounded_rectangle([x + s * 0.26, y + s * 0.14, x + s * 0.74, y + s * 0.86],
                            radius=int(s * 0.06), outline=color, width=lw)
        for i in range(3):
            yy = y + s * (0.34 + i * 0.16)
            d.line([(x + s * 0.36, yy), (x + s * 0.64, yy)], fill=color, width=max(1, lw - 1))
    elif name == "clock":
        d.ellipse([x + s * 0.14, y + s * 0.14, x + s * 0.86, y + s * 0.86],
                  outline=color, width=lw)
        d.line([(cx, cy), (cx, y + s * 0.30)], fill=color, width=lw)
        d.line([(cx, cy), (x + s * 0.68, cy)], fill=color, width=lw)
    elif name == "video":
        d.rounded_rectangle([x + s * 0.14, y + s * 0.26, x + s * 0.64, y + s * 0.74],
                            radius=int(s * 0.08), outline=color, width=lw)
        d.polygon([(x + s * 0.70, y + s * 0.34), (x + s * 0.70, y + s * 0.66),
                   (x + s * 0.88, y + s * 0.5)], fill=color)
    else:
        d.ellipse([cx - s * 0.16, cy - s * 0.16, cx + s * 0.16, cy + s * 0.16], fill=color)


def _float_badge(img, d, x, y, text, align="left"):
    f = font(BOLD_PATH, 26)
    w = tsize(f, text)[0] + 74
    h = 56
    if align == "right":
        x = x - w
    glass_card(img, x, y, w, h, r=h // 2)
    grad_pill(img, int(x + 22), int(y + h // 2 - 7), 14, 14, 7)
    d.text((x + 48, y + 13), text, font=f, fill=INK)
    return w, h


def _feature_chips(img, d, M, y, feats, max_w, cols=2):
    gap = 20
    cw = (max_w - gap * (cols - 1)) // cols
    ch = 100
    tf = font(REG_PATH, 27)
    rows = (len(feats) + cols - 1) // cols
    for i, ft in enumerate(feats):
        r, c = divmod(i, cols)
        cx = M + c * (cw + gap)
        cy = y + r * (ch + gap)
        glass_card(img, cx, cy, cw, ch, r=18)
        ib = 58
        _grad_circle_box = (cx + 20, cy + ch // 2 - ib // 2)
        grad_pill(img, _grad_circle_box[0], _grad_circle_box[1], ib, ib, 16)
        _icon(d, _grad_circle_box[0] + 13, _grad_circle_box[1] + 13, 32,
              ft.get("icon", "spark") if isinstance(ft, dict) else "spark",
              (10, 22, 30))
        text = ft["text"] if isinstance(ft, dict) else str(ft)
        lines = wrap(text, tf, cw - 110)[:2]
        ty = cy + ch // 2 - (len(lines) * int(tf.size * 1.22)) // 2
        for ln in lines:
            d.text((cx + 96, ty), ln, font=tf, fill=INK)
            ty += int(tf.size * 1.22)
    return y + rows * (ch + gap)


def _content_video(img, d, x, y, w, h, mk, seed):
    tl_h = 72
    ph = h - tl_h - 14
    poster = grad_h(w, ph, lerp(BLUE, (10, 14, 30), 0.45), lerp(GREEN, (10, 14, 30), 0.45))
    poster = Image.blend(poster.convert("RGB"), Image.new("RGB", (w, ph), (9, 13, 28)), 0.42)
    img.paste(poster, (x, y), rrect_mask(w, ph, 18))
    grad_border(img, x, y, w, ph, 18, 1)
    pcx, pcy, pr = x + w // 2, y + int(ph * 0.42), 56
    _grad_circle(img, pcx, pcy, pr)
    d.polygon([(pcx - pr * 0.26, pcy - pr * 0.40), (pcx - pr * 0.26, pcy + pr * 0.40),
               (pcx + pr * 0.46, pcy)], fill=(8, 18, 28))
    # filmstrip thumbnails along the bottom of the poster
    n, gap = 5, 14
    tww = (w - (n + 1) * gap) // n
    thh, thy = 60, y + ph - 76
    for i in range(n):
        tx = x + gap + i * (tww + gap)
        col = lerp(BLUE, GREEN, i / (n - 1))
        d.rounded_rectangle([tx, thy, tx + tww, thy + thh], radius=10,
                            fill=(col[0], col[1], col[2], 95))
    # "duration" chip top-left of poster
    cf = font(BOLD_PATH, 22)
    ctxt = mk.get("tag", "1080p")
    cw = tsize(cf, ctxt)[0] + 28
    d.rounded_rectangle([x + 16, y + 16, x + 16 + cw, y + 16 + 36], radius=10,
                        fill=(10, 22, 30, 200))
    d.text((x + 30, y + 22), ctxt, font=cf, fill=INK)
    # timeline
    ty = y + ph + 28
    d.rounded_rectangle([x, ty, x + w, ty + 8], radius=4, fill=(255, 255, 255, 46))
    fillw = int(w * 0.42)
    grad_pill(img, x, ty, fillw, 8, 4)
    d.ellipse([x + fillw - 11, ty - 7, x + fillw + 11, ty + 15], fill=(255, 255, 255))
    d.text((x, ty + 22), mk.get("time", "0:06 / 0:15"), font=font(REG_PATH, 24),
           fill=(172, 186, 202))


def _content_browser(img, d, x, y, w, h, mk, seed):
    hero_w, hero_h = int(w * 0.46), int(h * 0.52)
    hero = Image.blend(grad_h(hero_w, hero_h).convert("RGB"),
                       Image.new("RGB", (hero_w, hero_h), (12, 16, 34)), 0.4)
    img.paste(hero, (x, y), rrect_mask(hero_w, hero_h, 16))
    grad_border(img, x, y, hero_w, hero_h, 16, 1)
    _icon(d, x + hero_w // 2 - 26, y + hero_h // 2 - 26, 52,
          mk.get("icon", "play"), (255, 255, 255))
    tx = x + hero_w + 28
    lw = w - hero_w - 28
    for i, frac in enumerate([1.0, 0.86, 0.62]):
        yy = y + 8 + i * 50
        d.rounded_rectangle([tx, yy, tx + int(lw * frac), yy + 22], radius=10,
                            fill=(255, 255, 255, 78 if i == 0 else 40))
    for i in range(2):
        bx = tx + i * 150
        d.rounded_rectangle([bx, y + 180, bx + 132, y + 180 + 44], radius=22,
                            fill=(255, 255, 255, 30))
        grad_pill(img, bx + 16, y + 194, 16, 16, 8)
    cardsy = y + hero_h + 22
    n, gap = 3, 18
    cw = (w - (n - 1) * gap) // n
    chh = max(70, h - hero_h - 22)
    icons = mk.get("card_icons", ["bolt", "layers", "globe"])
    for i in range(n):
        cxx = x + i * (cw + gap)
        glass_card(img, cxx, cardsy, cw, chh, r=14)
        grad_pill(img, cxx + 16, cardsy + 16, 40, 40, 12)
        _icon(d, cxx + 16 + 8, cardsy + 16 + 8, 24, icons[i % len(icons)], (10, 22, 30))
        for k, frac in enumerate([0.8, 0.55]):
            yy = cardsy + 72 + k * 22
            d.rounded_rectangle([cxx + 16, yy, cxx + 16 + int((cw - 32) * frac), yy + 12],
                                radius=6, fill=(255, 255, 255, 46 if k == 0 else 26))


def _content_dashboard(img, d, x, y, w, h, mk, seed):
    rng = np.random.default_rng(seed * 9 + 4)
    tiles = mk.get("tiles", [{"value": "98%", "label": "uptime"},
                             {"value": "12k", "label": "users"},
                             {"value": "4.8", "label": "rating"}])[:3]
    n = len(tiles)
    gap = 18
    tw = (w - gap * (n - 1)) // n
    th = int(h * 0.34)
    for i, t in enumerate(tiles):
        tx = x + i * (tw + gap)
        glass_card(img, tx, y, tw, th, r=16)
        grad_text(img, (tx + 20, y + 18), str(t.get("value", "")), font(BOLD_PATH, 52))
        d.text((tx + 22, y + 84), str(t.get("label", "")), font=font(REG_PATH, 24),
               fill=MUTE)
    by = y + th + 20
    bh = h - th - 20
    # bar panel (left)
    bw = int(w * 0.54)
    glass_card(img, x, by, bw, bh, r=16)
    nb = 6
    g = 16
    barw = (bw - g * (nb + 1)) // nb
    base = by + bh - 24
    for i in range(nb):
        v = float(rng.uniform(0.3, 1.0))
        bx = x + g + i * (barw + g)
        bhh = int((bh - 60) * v)
        grad_pill(img, bx, base - bhh, barw, bhh, 8)
    # sparkline panel (right)
    sx = x + bw + 18
    sw = w - bw - 18
    glass_card(img, sx, by, sw, bh, r=16)
    pts = []
    nn = 7
    for i in range(nn):
        px = sx + 24 + i * (sw - 48) / (nn - 1)
        py = by + 30 + (bh - 70) * float(rng.uniform(0, 1))
        pts.append((px, py))
    d.line(pts, fill=GREEN, width=4, joint="curve")
    for p in pts:
        d.ellipse([p[0] - 5, p[1] - 5, p[0] + 5, p[1] + 5], fill=INK)


def _content_leaderboard(img, d, x, y, w, h, mk, seed):
    """Ranked comparison rows (logo chip + name + value); a `highlight` row is the
    brand-teal 'winner / self' row. Mirrors the Oxlo.ai pricing-comparison look."""
    rows = mk.get("rows", [])
    yy = y
    if mk.get("label"):
        d.text((x + 6, yy), mk["label"], font=font(BOLD_PATH, 26), fill=MUTE)
        yy += 48
    n = max(1, len(rows))
    gap = 16
    rh = min(116, max(70, (y + h - yy - gap * (n - 1)) // n))
    nf = font(BOLD_PATH, 38)
    vf = font(BOLD_PATH, 38)
    for r in rows:
        name = r.get("name", "") if isinstance(r, dict) else str(r)
        val = r.get("value", "") if isinstance(r, dict) else ""
        hl = r.get("highlight") if isinstance(r, dict) else False
        if hl:
            glass_card(img, x, yy, w, rh, r=16)
            grad_border(img, x, yy, w, rh, 16, 2)
            ncol = vcol = lerp(GREEN, (255, 255, 255), 0.25)
        else:
            d.rounded_rectangle([x, yy, x + w, yy + rh], radius=16, fill=(18, 24, 42, 235))
            d.rounded_rectangle([x, yy, x + w, yy + rh], radius=16, outline=(255, 255, 255, 26), width=1)
            ncol = vcol = INK
        ls = rh - 30
        lsx, lsy = x + 20, yy + (rh - ls) // 2
        grad_pill(img, lsx, lsy, ls, ls, 14)
        _icon(d, int(lsx + ls * 0.24), int(lsy + ls * 0.24), int(ls * 0.52),
              r.get("icon", "spark") if isinstance(r, dict) else "spark", (10, 22, 30))
        d.text((lsx + ls + 26, yy + rh // 2 - nf.size // 2), name, font=nf, fill=ncol)
        if val:
            vw = tsize(vf, val)[0]
            d.text((x + w - 24 - vw, yy + rh // 2 - vf.size // 2), val, font=vf, fill=vcol)
        yy += rh + gap


def _draw_mockup(img, d, x, y, w, h, mk, seed):
    kind = mk.get("type", "browser")
    if kind == "leaderboard":
        glass_card(img, x, y, w, h, r=26)
        _content_leaderboard(img, d, x + 26, y + 24, w - 52, h - 48, mk, seed)
        return
    glass_card(img, x, y, w, h, r=26)
    bar_h = 58
    d.rounded_rectangle([x, y, x + w, y + bar_h], radius=26, fill=(255, 255, 255, 14))
    d.rectangle([x, y + bar_h - 26, x + w, y + bar_h], fill=(0, 0, 0, 0))
    for i, col in enumerate([(255, 95, 87), (254, 188, 46), (40, 200, 64)]):
        d.ellipse([x + 24 + i * 28, y + bar_h // 2 - 7, x + 24 + i * 28 + 14,
                   y + bar_h // 2 + 7], fill=col)
    url = mk.get("url")
    if url:
        uf = font(REG_PATH, 24)
        uw = tsize(uf, url)[0]
        pw = min(w - 260, uw + 90)
        px = x + (w - pw) // 2
        ph = 38
        d.rounded_rectangle([px, y + bar_h // 2 - ph // 2, px + pw, y + bar_h // 2 + ph // 2],
                            radius=ph // 2, fill=(255, 255, 255, 24))
        _icon(d, px + 16, y + bar_h // 2 - 10, 20, "lock", (150, 165, 186))
        d.text((px + 46, y + bar_h // 2 - 13), url, font=uf, fill=(192, 204, 220))
    elif mk.get("title"):
        d.text((x + 120, y + bar_h // 2 - 15), mk["title"], font=font(REG_PATH, 26),
               fill=(182, 194, 210))
    d.line([(x, y + bar_h), (x + w, y + bar_h)], fill=(255, 255, 255, 22), width=1)
    cx0, cy0 = x + 28, y + bar_h + 26
    cw, ch = w - 56, h - bar_h - 52
    if kind == "video":
        _content_video(img, d, cx0, cy0, cw, ch, mk, seed)
    elif kind == "dashboard":
        _content_dashboard(img, d, cx0, cy0, cw, ch, mk, seed)
    else:
        _content_browser(img, d, cx0, cy0, cw, ch, mk, seed)


# ---------- card renderers ----------
def _headline_block(img, d, M, card, y):
    """Shared: eyebrow + headline + gradient underline + subhead. Returns new y."""
    W = img.width
    colw = W - 2 * M
    if card.get("eyebrow"):
        d.text((M, y), card["eyebrow"], font=font(BOLD_PATH, 30), fill=EYEBROW)
        y += 56
    hl = card.get("headline", [])
    hf = fit_font(BOLD_PATH, max(hl, key=len), colw, start=96) if hl else None
    lh = int((hf.size if hf else 88) * 1.42)
    first_w = tsize(hf, hl[0])[0] if hl else 0
    for line in hl:
        d.text((M, y), line, font=hf, fill=INK)
        y += lh
    if card.get("accent"):
        af = fit_font(BOLD_PATH, card["accent"], colw, start=hf.size if hf else 88)
        grad_text(img, (M, y), card["accent"], af)
        y += int(af.size * 1.42)
    y += 6
    grad_pill(img, M, y, card.get("underline_w", min(first_w or 360, 420)), 14, 7)
    y += 50
    if card.get("subhead"):
        sf = fit_font(REG_PATH, card["subhead"], colw, start=40, lo=24)
        d.text((M, y), card["subhead"], font=sf, fill=MUTE)
        y += int(sf.size * 1.5) + 24
    if card.get("url"):
        uf = font(REG_PATH, 32)
        _icon(d, M, y + 2, 26, "globe", lerp(BLUE, (255, 255, 255), 0.55))
        d.text((M + 40, y), card["url"], font=uf, fill=lerp(BLUE, (255, 255, 255), 0.6))
        y += int(uf.size * 1.5) + 8
    return y


def render_hero(img, d, M, card):
    W = img.width
    _particles(img, card.get("_seed", 1), n=56)
    add_glow(img, int(W * 0.82), int(img.height * 0.30), int(W * 0.5), GREEN, 0.26)
    y = _headline_block(img, d, M, card, int(img.height * 0.18))
    chips = card.get("chips", [])
    if chips:
        cf = font(BOLD_PATH, 30)
        cx = M
        for c in chips:
            cw = tsize(cf, c)[0] + 50
            ch = 64
            if cx + cw > W - M:
                cx = M
                y += ch + 18
            glass_card(img, cx, y, cw, ch, r=18)
            grad_pill(img, cx + 14, y + 18, 8, ch - 36, 4)
            d.text((cx + 34, y + 16), c, font=cf, fill=INK)
            cx += cw + 20
        y += 64 + 40
    st = card.get("stat")
    if st:
        vf = font(BOLD_PATH, 88)
        grad_text(img, (M, y), st["value"], vf)
        vw = tsize(vf, st["value"])[0]
        d.text((M + vw + 24, y + 30), st.get("label", ""),
               font=font(REG_PATH, 32), fill=MUTE)
        y += 120
    if card.get("date"):
        grad_pill(img, M, y, 14, 78, 7)
        d.text((M + 36, y - 6), card["date"], font=font(BOLD_PATH, 46), fill=INK)
        if card.get("date_sub"):
            d.text((M + 36, y + 48), card["date_sub"],
                   font=font(REG_PATH, 30), fill=MUTE)


def render_code(img, d, M, card):
    W, H = img.width, img.height
    _particles(img, card.get("_seed", 1), n=50)
    add_glow(img, int(W * 0.84), int(H * 0.28), int(W * 0.5), GREEN, 0.24)
    y = _headline_block(img, d, M, card, int(H * 0.15))
    # reserve bottom for hashtags/footer
    bottom = H - 150
    wy = y + 8
    wh = max(360, min(560, bottom - wy))
    draw_code_window(img, d, M, wy, W - 2 * M, wh, seed=card.get("_seed", 1),
                     file=card.get("file", "main.go"),
                     badge=card.get("badge", "AI Agent"))


def _marker_chip(img, d, x, cy, mark, i):
    """A glass, gradient-bordered marker box for a points item (modern look)."""
    s = 56
    y = cy - s // 2
    if mark == "num":
        grad_pill(img, x, y, s, s, 16)
        nb = font(BOLD_PATH, 30)
        nw = tsize(nb, str(i))[0]
        d.text((x + s // 2 - nw // 2, y + 11), str(i), font=nb, fill=(10, 22, 30))
    else:
        glass_card(img, x, y, s, s, r=16)
        grad_border(img, x, y, s, s, 16, 2)
        draw_marker(d, x + s // 2, cy, mark, r=17)


def render_points(img, d, M, card):
    W, H = img.width, img.height
    seed = card.get("_seed", 1)
    _particles(img, seed, n=52)
    add_glow(img, int(W * 0.86), int(H * 0.82), int(W * 0.5), GREEN, 0.22)
    y = int(H * 0.16)
    if card.get("eyebrow"):
        d.text((M, y), card["eyebrow"], font=font(BOLD_PATH, 30), fill=EYEBROW)
        y += 54
    title = card.get("title", "")
    if title:
        tf = fit_font(BOLD_PATH, title, W - 2 * M, start=72)
        d.text((M, y), title, font=tf, fill=INK)
        y += int(tf.size * 1.2)
        grad_pill(img, M, y, 300, 12, 6)
        y += 84
    colw = W - 2 * M
    rf = font(REG_PATH, 34)
    pad = 28
    for i, it in enumerate(card.get("items", []), 1):
        text = it["text"] if isinstance(it, dict) else str(it)
        mark = it.get("mark", "dot") if isinstance(it, dict) else "dot"
        lines = wrap(text, rf, colw - 140)
        rh = max(92, pad * 2 + len(lines) * int(rf.size * 1.35) - int(rf.size * 0.35))
        glass_card(img, M, y, colw, rh, r=18)
        grad_pill(img, M + 18, y + 16, 7, rh - 32, 4)
        _marker_chip(img, d, M + 40, y + rh // 2, mark, i)
        ty = y + (rh - len(lines) * int(rf.size * 1.35) + int(rf.size * 0.35)) // 2
        for ln in lines:
            d.text((M + 122, ty), ln, font=rf, fill=INK)
            ty += int(rf.size * 1.35)
        y += rh + 40


def render_stat(img, d, M, card):
    W, H = img.width, img.height
    seed = card.get("_seed", 1)
    _particles(img, seed, n=60)
    add_glow(img, int(W * 0.5), int(H * 0.40), int(W * 0.62), BLUE, 0.20)
    add_glow(img, int(W * 0.80), int(H * 0.74), int(W * 0.42), GREEN, 0.16)
    colw = W - 2 * M

    vf = fit_font(BOLD_PATH, card["value"], colw - 96, start=300, lo=96)
    vw, vh, ox, oy = tsize(vf, card["value"])
    lf = fit_font(BOLD_PATH, card["label"], colw - 130, start=50, lo=30) if card.get("label") else None
    nf = fit_font(REG_PATH, card["note"], colw - 130, start=34, lo=22) if card.get("note") else None
    chips = card.get("chips", [])

    content_h = vh + 28
    if lf:
        content_h += int(lf.size * 1.4) + 30
    if nf:
        content_h += int(nf.size * 1.5)
    panel_h = content_h + 96
    panel_y = (H - panel_h) // 2 + (10 if chips else 0)
    glass_card(img, M, panel_y, colw, panel_h, r=30)

    # floating badges above the panel
    by = panel_y - 70
    bx = M + colw - 8
    for b in card.get("badges", []):
        _, bh = _float_badge(img, d, bx, by, b, align="right")
        by -= bh + 14

    cy = panel_y + 56
    grad_text(img, ((W - vw) // 2 - ox, cy), card["value"], vf)
    y = cy + vh + 26
    if lf:
        lw = tsize(lf, card["label"])[0]
        d.text(((W - lw) // 2, y), card["label"], font=lf, fill=INK)
        y += int(lf.size * 1.4)
        grad_pill(img, (W - 200) // 2, y, 200, 10, 5)
        y += 30
    if nf:
        nw = tsize(nf, card["note"])[0]
        d.text(((W - nw) // 2, y), card["note"], font=nf, fill=MUTE)

    # optional sub-metric chips row below the panel
    if chips:
        cf = font(BOLD_PATH, 28)
        widths = [tsize(cf, c)[0] + 76 for c in chips]
        total = sum(widths) + 20 * (len(chips) - 1)
        cx = (W - total) // 2
        cyy = panel_y + panel_h + 26
        for c, cw in zip(chips, widths):
            glass_card(img, cx, cyy, cw, 64, r=18)
            grad_pill(img, cx + 20, cyy + 26, 14, 14, 7)
            d.text((cx + 46, cyy + 16), c, font=cf, fill=INK)
            cx += cw + 20


def render_showcase(img, d, M, card):
    """Apple-style showcase: benchmark bar chart + Sol/Terra/Luna solar-system
    illustration + bold bottom headline. Reproduces the premium release-card look
    for model/benchmark news. Full-bleed (no source footer)."""
    W, H = img.width, img.height
    seed = card.get("_seed", 1)
    _starfield(img, seed)
    _particles(img, seed, n=46)
    colw = W - 2 * M

    # --- benchmark chart panel (top-left) ---
    ch_x, ch_y = M, 168
    ch_w, ch_h = int(colw * 0.62), 372
    if card.get("chart"):
        glass_card(img, ch_x, ch_y, ch_w, ch_h, r=22)
        _draw_bar_chart(img, d, ch_x, ch_y, ch_w, ch_h, card["chart"], seed)
        # --- decorative digit globe (top-right gap) ---
        gcx = (ch_x + ch_w + (W - M)) // 2
        _digit_globe(d, gcx, ch_y + 150, 168, seed)
        # floating stat badges under the globe
        by = ch_y + 300
        for b in card.get("badges", []):
            _, bh = _float_badge(img, d, gcx + 150, by, b, align="right")
            by += bh + 14

    # --- solar-system band (middle) ---
    bcy = card.get("band_cy", 690)
    bodies = card.get("bodies", ["Sol", "Terra", "Luna"])
    sol_cx, sol_r = M + 78, 146
    terra_cx, terra_r = int(W * 0.52), 96
    luna_cx, luna_r = int(W * 0.83), 60
    for pcx in (terra_cx, luna_cx):
        rx = pcx - sol_cx
        ry = rx * 0.30
        d.ellipse([sol_cx - rx, bcy - ry, sol_cx + rx, bcy + ry],
                  outline=(255, 255, 255, 42), width=2)
    paste_sphere(img, sol_cx, bcy, sol_r, "sun", seed)
    paste_sphere(img, terra_cx, bcy, terra_r, "earth", seed)
    paste_sphere(img, luna_cx, bcy, luna_r, "moon", seed)
    _center_label(img, d, sol_cx, bcy, bodies[0], 60)
    _center_label(img, d, terra_cx, bcy, bodies[1], 46)
    _center_label(img, d, luna_cx, bcy, bodies[2], 34)

    # optional caption under each body (e.g. price / role)
    subs = card.get("body_subs")
    if subs:
        sf = font(REG_PATH, 26)
        for (pcx, pr), txt in zip(
                [(sol_cx, sol_r), (terra_cx, terra_r), (luna_cx, luna_r)], subs):
            sw = tsize(sf, txt)[0]
            d.text((pcx - sw // 2, bcy + pr + 14), txt, font=sf, fill=lerp(BLUE, (255, 255, 255), 0.5))

    if card.get("date"):
        df = fit_font(REG_PATH, card["date"], colw, start=30, lo=22)
        dw = tsize(df, card["date"])[0]
        dy = bcy + sol_r + (52 if subs else 18)
        d.text(((W - dw) // 2, dy), card["date"], font=df, fill=MUTE)

    # --- bold bottom headline block ---
    band_top = int(H * 0.66)
    _bottom_gradient(img, band_top)
    y = band_top + 34
    hl = card.get("headline", [])
    hf = fit_font(BOLD_PATH, max(hl, key=len), colw, start=118, lo=52) if hl else None
    lh = int((hf.size if hf else 90) * 1.1)
    for line in hl:
        d.text((M + 3, y + 3), line, font=hf, fill=(0, 0, 0, 130))
        d.text((M, y), line, font=hf, fill=INK)
        y += lh
    y += 12
    sub = card.get("subhead")
    if sub:
        if isinstance(sub, str):
            sub = [sub]
        sf = fit_font(REG_PATH, max(sub, key=len), colw - 34, start=46, lo=28)
        sub_h = len(sub) * int(sf.size * 1.42)
        grad_pill(img, M, y + 6, 12, max(10, sub_h - 12), 6)
        sc = lerp(BLUE, (255, 255, 255), 0.6)
        for ln in sub:
            d.text((M + 36, y), ln, font=sf, fill=sc)
            y += int(sf.size * 1.42)


def render_feature(img, d, M, card):
    """Modern, detailed product/tool hero: headline + a glassy mockup (browser /
    video / dashboard) with floating stat badges and a row of feature chips with
    icons, over particles + glow. Use as the hero for product/tool/how-to posts."""
    W, H = img.width, img.height
    seed = card.get("_seed", 1)
    _particles(img, seed)
    add_glow(img, int(W * 0.82), int(H * 0.30), int(W * 0.5), GREEN, 0.30)

    colw = W - 2 * M
    y = _headline_block(img, d, M, card, int(H * 0.135))

    feats = card.get("features", [])
    chip_rows = (len(feats) + 1) // 2
    chips_h = chip_rows * (100 + 20) if feats else 0
    footer_top = H - 150

    # --- mockup window ---
    mk = card.get("mockup")
    if mk:
        mock_y = y + 6
        mock_h = footer_top - mock_y - chips_h - (30 if feats else 0)
        mock_h = max(320, min(540, mock_h))
        _draw_mockup(img, d, M, mock_y, colw, mock_h, mk, seed)
        # floating stat badges, stacked at the mockup's top-right
        bx = M + colw - 24
        by = mock_y - 28
        for b in card.get("badges", []):
            bw, bh = _float_badge(img, d, bx, by, b, align="right")
            by += bh + 14
        chips_y = mock_y + mock_h + 30
    else:
        chips_y = y + 10

    # --- feature chips ---
    if feats:
        _feature_chips(img, d, M, chips_y, feats, colw, cols=2)


def render_stack(img, d, M, card):
    """'Tools / tech stack' card — a list of tools each with an icon badge, a
    bold name, and a one-line role. Use for 'what it's built on / tools to use'."""
    W, H = img.width, img.height
    seed = card.get("_seed", 1)
    _particles(img, seed, n=50)
    add_glow(img, int(W * 0.84), int(H * 0.20), int(W * 0.5), GREEN, 0.22)
    colw = W - 2 * M
    y = int(H * 0.16)
    if card.get("eyebrow"):
        d.text((M, y), card["eyebrow"], font=font(BOLD_PATH, 30), fill=EYEBROW)
        y += 54
    if card.get("title"):
        tf = fit_font(BOLD_PATH, card["title"], colw, start=72)
        d.text((M, y), card["title"], font=tf, fill=INK)
        y += int(tf.size * 1.2)
        grad_pill(img, M, y, 300, 12, 6)
        y += 52

    tools = card.get("tools", [])
    footer_top = H - 150
    gap = 20
    rh = min(150, max(110, (footer_top - y - gap * (len(tools) - 1)) // max(1, len(tools))))
    nf = font(BOLD_PATH, 42)
    rf = font(REG_PATH, 31)
    role_col = (206, 217, 232)  # brighter than MUTE for readability
    for t in tools:
        name = t.get("name", "") if isinstance(t, dict) else str(t)
        role = t.get("role", "") if isinstance(t, dict) else ""
        icon = t.get("icon", "spark") if isinstance(t, dict) else "spark"
        glass_card(img, M, y, colw, rh, r=20)
        grad_pill(img, M + 22, y + 22, 8, rh - 44, 4)
        ib = 72
        ibx, iby = M + 46, y + rh // 2 - ib // 2
        grad_pill(img, ibx, iby, ib, ib, 18)
        _icon(d, ibx + 18, iby + 18, 36, icon, (10, 22, 30))
        tx = ibx + ib + 30
        if role:
            rlines = wrap(role, rf, colw - (tx - M) - 28)[:2]
            block_h = nf.size + 10 + len(rlines) * int(rf.size * 1.28)
            ty = y + (rh - block_h) // 2
            d.text((tx, ty), name, font=nf, fill=INK)
            ty += nf.size + 10
            for ln in rlines:
                d.text((tx, ty), ln, font=rf, fill=role_col)
                ty += int(rf.size * 1.28)
        else:
            d.text((tx, y + rh // 2 - nf.size // 2), name, font=nf, fill=INK)
        y += rh + gap


SIZES = {"portrait": (1080, 1350), "square": (1080, 1080),
         "landscape": (1200, 630), "story": (1080, 1920)}
RENDERERS = {"hero": render_hero, "code": render_code,
             "points": render_points, "stat": render_stat,
             "showcase": render_showcase, "feature": render_feature,
             "stack": render_stack}


def render_card(card, top, idx):
    size = card.get("size", top.get("size", "portrait"))
    W, H = SIZES.get(size, SIZES["portrait"]) if isinstance(size, str) else size
    M = round(W * 0.078)
    card = dict(card, _seed=idx + 1)
    img = background(W, H, seed=idx + 1,
                     motif=card.get("motif", top.get("motif")))
    d = ImageDraw.Draw(img, "RGBA")
    top_bar(img, d, M,
            card.get("brand", top.get("brand", "Arnfar")),
            card.get("category", top.get("category", "")),
            tags=card.get("tags", top.get("tags")))
    RENDERERS.get(card.get("kind", "hero"), render_hero)(img, d, M, card)
    if card.get("kind") != "showcase":
        footer(img, d, M,
               card.get("footer_tags", top.get("footer_tags", DEFAULT_TAGS)))
    return img


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("--outdir", default=None)
    args = ap.parse_args()
    spec = json.load(open(args.spec, encoding="utf-8"))
    outdir = args.outdir or spec.get("outdir") or os.getcwd()
    os.makedirs(outdir, exist_ok=True)
    prefix = spec.get("prefix", "arnfar-news")
    cards = spec.get("cards", [])
    for i, card in enumerate(cards, 1):
        img = render_card(card, spec, i)
        suffix = f"-{i:02d}" if len(cards) > 1 else ""
        p = os.path.join(outdir, f"{prefix}{suffix}.png")
        img.save(p)
        print("saved", p)


if __name__ == "__main__":
    main()

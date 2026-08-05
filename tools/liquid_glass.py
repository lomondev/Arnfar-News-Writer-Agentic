#!/usr/bin/env python3
"""liquid_glass.py — shared Arnfar liquid-glass panel renderer (Pillow+numpy).

Apple 'Liquid Glass'-style panel: deep frosted blur of the backdrop with a
saturation lift so the brand orbs glow through, edge refraction that bends the
background at the rim, a curved top-left specular sweep + hot spot, an inner
bottom depth shadow, a directional specular rim, and a brand blue->green
hairline border.

Usage:
    from liquid_glass import glass_card
    glass_card(img, x, y, w, h, r=22)                  # dark panel
    glass_card(img, x, y, w, h, r=22, dark=False)      # light panel

The same implementation lives inline in
skills/breaking-news-report/scripts/arnfar_news_card.py (the skill script is
intentionally self-contained); keep the two in sync when tuning the look.
"""
from __future__ import annotations

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter

BLUE = (3, 148, 241)
GREEN = (21, 198, 122)


def _rrect_mask(w, h, r):
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], radius=r,
                                        fill=255)
    return m


def _ring_mask(w, h, r, width):
    outer = _rrect_mask(w, h, r)
    inner = Image.new("L", (w, h), 0)
    ImageDraw.Draw(inner).rounded_rectangle(
        [width, width, w - 1 - width, h - 1 - width],
        radius=max(1, r - width), fill=255)
    return ImageChops.subtract(outer, inner)


def _grad_h(w, h, c0=BLUE, c1=GREEN):
    ramp = np.linspace(0, 1, max(1, w))[:, None]
    arr = np.array(c0)[None, :] * (1 - ramp) + np.array(c1)[None, :] * ramp
    return Image.fromarray(arr.astype(np.uint8)[None].repeat(h, 0), "RGB")


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


def glass_card(img, x, y, w, h, r=22, dark=True, border=(BLUE, GREEN)):
    """Draw a liquid-glass panel onto `img` (RGB) at (x, y) sized (w, h)."""
    x, y, w, h = int(x), int(y), int(w), int(h)

    # 1. Soft drop shadow underneath the card
    shadow = Image.new("RGBA", (w + 48, h + 48), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle(
        [24, 24, 24 + w - 1, 24 + h - 1], radius=r, fill=(0, 0, 0, 110))
    shadow = shadow.filter(ImageFilter.GaussianBlur(18))
    img.paste(shadow, (x - 24, y - 16), shadow)

    # 2. Frosted backdrop: heavy blur + saturation/brightness lift, then
    #    edge refraction.
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
    mask = _rrect_mask(w, h, r)
    img.paste(reg, (x, y), mask)
    # NB: paste an RGB fill with an alpha-scaled mask — pasting an RGBA tint
    # with an explicit mask drops its alpha and floods the panel solid white.
    img.paste(Image.new("RGB", (w, h), (255, 255, 255)), (x, y),
              mask.point(lambda v: v * tint_a // 255))

    # 3. Curved specular sweep from the top-left + corner hot spot
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
    spec = _ring_mask(w, h, r, 2)
    rim = np.clip(1.0 - (xx / w + yy / h) / 1.1, 0.18, 1.0) * 120
    rmask = ImageChops.multiply(spec, Image.fromarray(
        rim.astype(np.uint8), "L"))
    img.paste(Image.new("RGB", (w, h), (255, 255, 255)), (x, y), rmask)

    # 6. Brand hairline gradient border
    bmask = _ring_mask(w, h, r, 1).point(lambda v: v * 90 // 255)
    img.paste(_grad_h(w, h, border[0], border[1]), (x, y), bmask)

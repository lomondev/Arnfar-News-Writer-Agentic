#!/usr/bin/env python3
"""Arnfar single-image news post (house format, approved 2026-10-18/19).

One FB-size image (1080x1350) per story, used on Facebook, Instagram and TikTok:
topic pill + glass Arnfar badge, headline (max 2 lines), real related photo in a
glass frame, one short explanation line, credit line, "read more" cue, and the
Arnfar ERP ad band at the bottom of the safe area. Background: AI-generated,
text-free, cover-fitted (spec "background"); falls back to a blurred photo.

usage: render_single.py <spec.json>
spec keys:
  out         output stem, e.g. "out/arnfar-<slug>" (-> <stem>-<platform>.png)
  photo       related photo / screenshot
  background  optional topic background image
  tag         short topic pill text
  title       headline; "\n" forces the line break; max 2 lines
  desc        one short line (max 2 lines)
  credit      "ຮູບ: <source> · ຂໍ້ມູນ: <source>"
  accent      optional "brand" (default) or "warn"
  platforms   optional list, default ["facebook"]
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

import render as R

R.DARK_GLASS = 0.45
R.TEXT_SHADOW = 140
WARN = ((255, 90, 80), (255, 176, 32))
BRAND = (R.BLUE, R.GREEN)

# size + safe area (left, top, right, bottom)
PLATFORMS = {
    "facebook": ((1080, 1350), (108, 60, 108, 74)),
    "instagram": ((1080, 1350), (108, 60, 108, 74)),
    "tiktok": ((1080, 1920), (90, 170, 150, 470)),
}


def set_accent(spec: dict, brand: bool = False) -> None:
    R.BLUE, R.GREEN = BRAND if (brand or spec.get("accent") != "warn") else WARN


def wrap(text: str, size: int, max_w: int, max_lines: int) -> list[str]:
    lines: list[str] = []
    for para in text.split("\n"):
        cur = ""
        for w in para.split(" "):
            trial = f"{cur} {w}".strip()
            if R.text_width(trial, size) <= max_w or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    if len(lines) > max_lines or any(R.text_width(l, size) > max_w for l in lines):
        raise SystemExit(f"text too long for {max_lines} lines at {size}px: {text!r}")
    return [l.replace(" ", " ") for l in lines]


def fit_title(text: str, max_w: int) -> tuple[list[str], int]:
    for size in (76, 70, 64, 58, 52):
        try:
            return wrap(text, size, max_w, 2), size
        except SystemExit:
            continue
    raise SystemExit(f"title too long: {text!r}")


def cover(im: Image.Image, W: int, H: int) -> Image.Image:
    s = max(W / im.width, H / im.height)
    im = im.resize((int(im.width * s) + 1, int(im.height * s) + 1), Image.LANCZOS)
    x, y = (im.width - W) // 2, (im.height - H) // 2
    return im.crop((x, y, x + W, y + H))


def backdrop(spec: dict, photo: Image.Image, W: int, H: int) -> Image.Image:
    if spec.get("background"):
        bg = cover(Image.open(spec["background"]).convert("RGB"), W, H)
        return ImageEnhance.Brightness(bg).enhance(0.9)
    bg = cover(photo, W, H).filter(ImageFilter.GaussianBlur(38))
    bg = ImageEnhance.Brightness(bg).enhance(0.35)
    tint = R.gradient_img((W, H), (4, 14, 40), (2, 30, 30), horizontal=False)
    return Image.blend(bg, tint, 0.55)


def logo_disc(img: Image.Image, x: int, y: int, size: int) -> None:
    """Logo on a crisp white disc just inside the logo ring."""
    d = Image.new("L", (size * 4, size * 4), 0)
    inset = int(size * 4 * 0.07)
    ImageDraw.Draw(d).ellipse((inset, inset, size * 4 - inset, size * 4 - inset), fill=255)
    d = d.resize((size, size), Image.LANCZOS)
    img.paste((255, 255, 255), (x, y), d)
    R.paste_logo(img, x, y, size)


def ink_center_y(text: str, size: int) -> tuple[int, int]:
    """(ascent-to-ink-top, ink height) for vertically centring by glyph ink."""
    tops, bots = [], []
    for k, t in R.runs(text):
        f = R.font(k, R.run_size(k, size))
        b = f.getbbox(t, anchor="ls")
        tops.append(b[1]); bots.append(b[3])
    return min(tops), max(bots) - min(tops)


def badge(img: Image.Image, right: int, y: int) -> int:
    wm, ws, ls = "Arnfar", 46, 62
    tw = R.text_width(wm, ws)
    h = 84
    w = 14 + ls + 16 + tw + 30
    x = right - w
    R.glass(img, (x, y, right, y + h), r=h // 2, tint=46, blur=22)
    logo_disc(img, x + 12, y + (h - ls) // 2, ls)
    top, ih = ink_center_y(wm, ws)
    asc = max(R.font(k, R.run_size(k, ws)).getmetrics()[0] for k, _ in R.runs(wm))
    ty = y + (h - ih) // 2 - (asc + top)
    R.draw_text(img, (x + 12 + ls + 16, ty), wm, ws, R.WHITE)
    return y + h


def footer(img: Image.Image, left: int, right: int, bottom: int) -> int:
    band_h = 96
    by = bottom - band_h
    R.glass(img, (left, by, right, bottom), r=34, tint=30, blur=18)
    logo_disc(img, left + 16, by + (band_h - 68) // 2, 68)
    tx = left + 16 + 68 + 16
    max_w = right - 22 - tx
    l1a, l1b = "Arnfar", "ERP · ບັນຊີ · ສາງສິນຄ້າ · HR · Payroll"
    l2 = "ເຊື່ອມທຸກລະບົບເຂົ້າເປັນບັນຊີດຽວ · arnfar.com · ໂທ 020 9999 6967"
    s1, s2 = 32, 24
    while R.text_width(f"{l1a} {l1b}", s1) > max_w and s1 > 20:
        s1 -= 1
    while R.text_width(l2, s2) > max_w and s2 > 16:
        s2 -= 1
    w = R.draw_text(img, (tx, by + 12), l1a, s1, gradient=True)
    R.draw_text(img, (tx + w + 10, by + 12), l1b, s1, R.WHITE)
    R.draw_text(img, (tx, by + 54), l2, s2, R.INK2)
    return by


def framed_photo(img, photo, box) -> tuple[int, int]:
    x0, y0, x1, y1 = box
    bw, bh = x1 - x0, y1 - y0
    pad = 14
    s = min((bw - 2 * pad) / photo.width, (bh - 2 * pad) / photo.height)
    pw, ph = int(photo.width * s), int(photo.height * s)
    p = photo.resize((pw, ph), Image.LANCZOS)
    px, py = x0 + (bw - pw) // 2, y0 + (bh - ph) // 2
    R.glass(img, (px - pad, py - pad, px + pw + pad, py + ph + pad), r=34, tint=30, blur=18)
    img.paste(p, (px, py), R.rounded_mask((pw, ph), 22))
    return py - pad, py + ph + pad


def render_one(spec: dict, platform: str) -> Path:
    (W, H), (sl, st, sr, sb) = PLATFORMS[platform]
    R.W, R.H = W, H
    left, right, top, bottom = sl, W - sr, st, H - sb
    photo = Image.open(spec["photo"]).convert("RGB")
    img = backdrop(spec, photo, W, H)

    # top bar
    set_accent(spec)
    ph = int(30 * 1.85)
    R.pill(img, left, top + (84 - ph) // 2, spec["tag"], 30, gradient_fill=True)
    set_accent(spec, brand=True)
    y = badge(img, right, top)

    # headline
    set_accent(spec)
    lines, size = fit_title(spec["title"], right - left)
    ty = y + 34
    lh = int(size * 1.45)
    for i, ln in enumerate(lines):
        last = i == len(lines) - 1
        R.draw_text(img, (W // 2, ty + i * lh), ln, size,
                    R.WHITE, gradient=last, anchor_center=True)
    title_bottom = ty + len(lines) * lh + 10

    # footer + cue + credit + desc (bottom-up)
    set_accent(spec, brand=True)
    fy = footer(img, left, right, bottom)
    cue = "ອ່ານລາຍລະອຽດຕໍ່ໃນແຄັບຊັນ"
    cs = 28
    cw = R.text_width(cue, cs) + int(cs * 1.4)
    cy = fy - 26 - int(cs * 1.85)
    R.pill(img, (W - cw) // 2, cy, cue, cs)
    crs = 22
    cry = cy - 22 - int(crs * 1.5)
    R.draw_text(img, (W // 2, cry), spec["credit"], crs, R.INK2, anchor_center=True)
    dlines = wrap(spec["desc"], 34, right - left, 2)
    dy = cry - 18 - len(dlines) * 52
    for i, ln in enumerate(dlines):
        R.draw_text(img, (W // 2, dy + i * 52), ln, 34, R.WHITE, anchor_center=True)

    # centre photo between headline and description
    framed_photo(img, photo, (left - 32, title_bottom + 24, right + 32, dy - 24))

    out = Path(f"{spec['out']}-{platform}.png")
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, optimize=True)
    return out


if __name__ == "__main__":
    spec = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    for p in spec.get("platforms", ["facebook"]):
        print(render_one(spec, p))

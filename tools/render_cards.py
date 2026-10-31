#!/usr/bin/env python3
"""Arnfar liquid-glass news cards — always a 4-card set, Phetsarath OT font.

Usage:  python3 render_cards.py spec.json --outdir output

Rules baked in (from the Arnfar card conventions):
- 1080x1350 portrait (4:5), safe zone x=10% y=5.5%, line-height 1.42.
- Exactly 4 cards per set (hero / stat / points / action). A spec with any
  other count is rejected — fix the spec, not the renderer.
- Font: Phetsarath OT Regular for ALL text. Never Bold. If the Phetsarath file
  has no Latin glyphs (the Google Fonts build is Lao-only), each run of
  uncovered characters falls back to Noto Sans Regular, glyph by glyph.
- Brand gradient blue #0394F1 -> green #15C67A, dark navy liquid glass.
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional, Sequence

from fontTools.ttLib import TTFont
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageFont

W, H = 1080, 1350
SAFE_X = int(W * 0.10)
SAFE_Y = int(H * 0.055)
LINE_H = 1.42
CARD_COUNT = 4

BLUE = (3, 148, 241)
GREEN = (21, 198, 122)
NAVY = (6, 14, 30)
INK = (240, 246, 255)
INK_SOFT = (178, 196, 222)

RGB = tuple[int, int, int]

# Category styles. Accents (badges, underlines, highlight pills, accent text,
# glass rims, motif strokes) follow the style; the Arnfar wordmark and the ad
# band always stay on the brand blue->green so every set reads as Arnfar.
STYLES: dict[str, dict[str, Any]] = {
    "default": {
        "base": NAVY,
        "glows": [((-320, -300, 620, 560), (3, 110, 200)), ((520, 820, 1460, 1680), (12, 150, 95)), ((640, -160, 1180, 300), (20, 40, 110))],
        "accent": (BLUE, GREEN),
        "accent_text": ((60, 175, 255), (40, 225, 150)),
        "rim": ((120, 200, 255), (110, 235, 180)),
        "motif": ((120, 200, 255), (110, 235, 180)),
        "particles": (200, 230, 255),
        "ink_soft": INK_SOFT,
        "overlay": "grid",
    },
    # Breach / ransomware / hacking news: black terminal, red-alert glow, amber edge, red code rain.
    "hacker": {
        "base": (7, 5, 9),
        "glows": [((-420, -380, 520, 420), (110, 6, 20)), ((600, 960, 1480, 1700), (120, 48, 0)), ((760, -220, 1260, 240), (55, 4, 14))],
        "accent": ((235, 38, 52), (255, 160, 32)),
        "accent_text": ((255, 74, 84), (255, 184, 64)),
        "rim": ((255, 110, 110), (255, 190, 90)),
        "motif": ((255, 80, 90), (255, 176, 60)),
        "particles": (255, 140, 120),
        "ink_soft": (214, 186, 186),
        "overlay": "code",
        "code_color": (255, 70, 70),
    },
    # Hacker variants — same red/amber palette, different backdrop art.
    "hacker_grid": {"base": (6, 4, 10), "glows": [((-300, 560, 1380, 1160), (140, 14, 30)), ((-420, -380, 520, 420), (60, 4, 16)), ((640, 900, 1480, 1700), (110, 44, 0))],
                    "overlay": "grid3d"},
    "hacker_circuit": {"base": (8, 4, 6), "glows": [((-420, -380, 520, 420), (100, 6, 18)), ((600, 960, 1480, 1700), (120, 46, 0)), ((300, 300, 1200, 1000), (40, 4, 10))],
                       "overlay": "circuit"},
    "hacker_netmap": {"base": (5, 4, 8), "glows": [((-420, -380, 520, 420), (90, 6, 18)), ((600, 960, 1480, 1700), (110, 44, 0)), ((200, 200, 1000, 800), (45, 6, 14))],
                      "overlay": "netmap"},
    # Same story, classic terminal-green look.
    "matrix": {
        "base": (3, 8, 6),
        "glows": [((-420, -380, 520, 420), (0, 80, 38)), ((600, 960, 1480, 1700), (0, 100, 58)), ((760, -220, 1260, 240), (0, 38, 24))],
        "accent": ((0, 200, 90), (150, 255, 120)),
        "accent_text": ((40, 230, 120), (170, 255, 140)),
        "rim": ((90, 240, 150), (170, 255, 150)),
        "motif": ((60, 230, 130), (160, 255, 140)),
        "particles": (140, 255, 170),
        "ink_soft": (176, 214, 190),
        "overlay": "code",
        "code_color": (40, 255, 120),
    },
}
# Video / creator-tool news: default navy palette + editing-suite backdrop art.
STYLES["video"] = {**STYLES["default"], "overlay": "video"}
STYLES["diagram"] = {**STYLES["default"], "overlay": "diagram"}
# Education news: chalkboard green base, warm lamp-amber glow, gold + mint accents.
STYLES["education"] = {
    "base": (8, 30, 26),
    "glows": [((-320, -300, 620, 560), (14, 92, 70)), ((520, 820, 1460, 1680), (150, 92, 10)), ((640, -160, 1180, 300), (90, 70, 10))],
    "accent": ((255, 190, 60), (60, 210, 150)),
    "accent_text": ((255, 202, 90), (90, 230, 170)),
    "rim": ((255, 215, 140), (140, 235, 190)),
    "motif": ((255, 200, 90), (120, 230, 180)),
    "particles": (255, 230, 170),
    "ink_soft": (214, 226, 210),
    "overlay": "education",
}
for _k in ("hacker_grid", "hacker_circuit", "hacker_netmap"):
    STYLES[_k] = {**{k: v for k, v in STYLES["hacker"].items() if k not in ("glows", "base", "overlay")}, **STYLES[_k]}
STYLE: dict[str, Any] = STYLES["default"]
BRAND_TEXT: tuple[RGB, RGB] = ((60, 175, 255), (40, 225, 150))
MONO = next((m for m in ("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", "/Library/Fonts/Courier New.ttf",
                          "/System/Library/Fonts/Menlo.ttc", "C:/Windows/Fonts/consola.ttf") if Path(m).exists()),
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf")


def set_style(name: str) -> None:
    global STYLE
    if name not in STYLES:
        sys.exit(f"unknown style {name!r} (use {sorted(STYLES)})")
    STYLE = STYLES[name]

_HERE = Path(__file__).resolve().parent
# works both standalone (./fonts) and inside the repo (tools/fonts, or <repo>/font)
FONT_DIR = next((d for d in (_HERE / "fonts", _HERE.parent / "fonts", _HERE.parent / "font") if (d / "Phetsarath-Regular.ttf").exists() or (d / "Phetsarath_OT.ttf").exists()), _HERE / "fonts")
# First existing file wins. A real "Phetsarath OT" (with Latin) makes the
# fallback unused.
PHETSARATH_CANDIDATES = [
    FONT_DIR / "Phetsarath_OT.ttf",
    FONT_DIR / "Phetsarath OT.ttf",
    FONT_DIR / "Phetsarath-Regular.ttf",
]
FALLBACK_FONT = FONT_DIR / "NotoSans.ttf"
LATIN_SCALE = 0.92  # Noto Sans reads slightly larger than Phetsarath at equal size


def _first_existing(paths: Sequence[Path]) -> Path:
    for p in paths:
        if p.exists():
            return p
    sys.exit("Phetsarath OT font not found. Put Phetsarath_OT.ttf (or Phetsarath-Regular.ttf) in " + str(FONT_DIR))


PRIMARY_PATH = _first_existing(PHETSARATH_CANDIDATES)
PRIMARY_CMAP: set[int] = set(TTFont(str(PRIMARY_PATH)).getBestCmap())
if "Bold" in PRIMARY_PATH.name:
    sys.exit("Refusing Bold face — Regular only")


class MixFont:
    """Phetsarath for every glyph it has; Noto Sans Regular for the rest."""

    def __init__(self, size: int) -> None:
        self.size = size
        self.primary = ImageFont.truetype(str(PRIMARY_PATH), size, layout_engine=ImageFont.Layout.RAQM)
        self.fallback: ImageFont.FreeTypeFont | None = None
        if FALLBACK_FONT.exists():
            fb = ImageFont.truetype(str(FALLBACK_FONT), int(size * LATIN_SCALE), layout_engine=ImageFont.Layout.RAQM)
            try:
                fb.set_variation_by_name("Regular")
            except (OSError, ValueError):
                pass
            self.fallback = fb
        self.ascent, self.descent = self.primary.getmetrics()

    def runs(self, s: str) -> list[tuple[str, ImageFont.FreeTypeFont]]:
        out: list[tuple[str, ImageFont.FreeTypeFont]] = []
        for ch in s:
            use_primary = ord(ch) in PRIMARY_CMAP or self.fallback is None
            # spaces/combining marks stay with the current run
            if out and (ch == " " or 0x0E31 <= ord(ch) <= 0x0ECD and ord(ch) in PRIMARY_CMAP and out[-1][1] is self.primary):
                f = out[-1][1]
            else:
                f = self.primary if use_primary else self.fallback  # type: ignore[assignment]
            if out and out[-1][1] is f:
                out[-1] = (out[-1][0] + ch, f)
            else:
                out.append((ch, f))
        return out

    def length(self, s: str) -> int:
        return int(sum(f.getlength(t) for t, f in self.runs(s)))

    def height(self) -> int:
        return self.ascent + self.descent

    def draw(self, d: ImageDraw.ImageDraw, xy: tuple[int, int], s: str, fill: Any) -> None:
        x, y = xy
        base = y + self.ascent
        for t, f in self.runs(s):
            d.text((x, base), t, font=f, fill=fill, anchor="ls")
            x += f.getlength(t)


_cache: dict[int, MixFont] = {}


def font(size: int) -> MixFont:
    if size not in _cache:
        _cache[size] = MixFont(size)
    return _cache[size]


# ---------------------------------------------------------------- drawing helpers


def lerp(a: tuple[int, int, int], b: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    return (int(a[0] + (b[0] - a[0]) * t), int(a[1] + (b[1] - a[1]) * t), int(a[2] + (b[2] - a[2]) * t))


def h_gradient(w: int, h: int, c1: RGB | None = None, c2: RGB | None = None) -> Image.Image:
    if c1 is None or c2 is None:
        c1, c2 = STYLE["accent"]
    row = Image.new("RGB", (max(1, w), 1))
    px = row.load()
    for x in range(max(1, w)):
        px[x, 0] = lerp(c1, c2, x / max(1, w - 1))
    return row.resize((max(1, w), max(1, h)))


def rrect_mask(size: tuple[int, int], radius: int) -> Image.Image:
    m = Image.new("L", size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), radius, fill=255)
    return m


BG_IMAGE: Optional[Path] = None
BG_SHIFT_X: int = 0
BG_SCALE: float = 1.0


def photo_background(path: Path, kind: str) -> Image.Image:
    """Cover-crop an illustration to the card, then shade it so text stays legible.

    Hero/stat cards keep the picture bright on the right and fade the left
    (text column) to the style base; list cards (points/action) blur and dim the
    whole picture because glass rows cover most of the card.
    """
    src = Image.open(path).convert("RGB")
    sc = max(W / src.width, H / src.height)
    src = src.resize((round(src.width * sc), round(src.height * sc)), Image.LANCZOS)
    ox, oy = (src.width - W) // 2, (src.height - H) // 2
    img = src.crop((ox, oy, ox + W, oy + H))
    base = Image.new("RGB", (W, H), STYLE["base"])
    if kind not in ("points", "action") and (BG_SHIFT_X or BG_SCALE != 1.0):
        # shrink the scene and anchor it bottom-right (then nudge by BG_SHIFT_X)
        # so the subject clears the headline column without being cropped
        sw, sh = round(W * BG_SCALE), round(H * BG_SCALE)
        small = img.resize((sw, sh), Image.LANCZOS)
        # feather the top and left edges of the shrunk picture so no seam shows
        feather = Image.new("L", (sw, sh), 255)
        fd = ImageDraw.Draw(feather)
        fe = 140
        for k in range(fe):
            a = int(255 * (k / fe) ** 1.5)
            fd.line((0, k, sw, k), fill=a)
        lm = Image.new("L", (sw, sh), 255)
        ld2 = ImageDraw.Draw(lm)
        for k in range(fe):
            ld2.line((k, 0, k, sh), fill=int(255 * (k / fe) ** 1.5))
        feather = ImageChops.multiply(feather, lm)
        shifted = base.copy()
        shifted.paste(small, (W - sw + BG_SHIFT_X, H - sh), feather)
        img = shifted
    if kind in ("points", "action"):
        img = img.filter(ImageFilter.GaussianBlur(6))
        img = Image.blend(base, img, 0.42)
    else:
        img = ImageEnhance.Color(img).enhance(1.1)
        # horizontal fade: solid base behind the text column, picture on the right
        mask = Image.new("L", (W, 1))
        for x in range(W):
            t = x / (W - 1)
            mask.putpixel((x, 0), int(255 * min(1.0, max(0.0, (t - 0.18) / 0.5)) ** 1.3))
        mask = mask.resize((W, H))
        # and keep the bottom (chips, hashtags, ad band) calm
        vfade = Image.new("L", (1, H))
        for y in range(H):
            u = y / (H - 1)
            bottom = max(0.0, (u - 0.55) / 0.45) * 0.75
            top = max(0.0, (0.12 - u) / 0.12) * 0.55  # calm strip behind tags + wordmark
            vfade.putpixel((0, y), int(255 * (1 - max(bottom, top))))
        mask = ImageChops.multiply(mask, vfade.resize((W, H)))
        img = Image.composite(img, Image.blend(base, img, 0.22), mask)
    glow = Image.new("RGB", (W, H), (0, 0, 0))
    g = ImageDraw.Draw(glow)
    for box, col in STYLE["glows"]:
        g.ellipse(box, fill=tuple(int(c * 0.45) for c in col))
    return ImageChops.add(img, glow.filter(ImageFilter.GaussianBlur(170)))


def background(seed: int, kind: str = "") -> Image.Image:
    if BG_IMAGE is not None:
        return photo_background(BG_IMAGE, kind)
    img = Image.new("RGB", (W, H), STYLE["base"])
    glow = Image.new("RGB", (W, H), (0, 0, 0))
    g = ImageDraw.Draw(glow)
    for box, col in STYLE["glows"]:
        g.ellipse(box, fill=col)
    img = ImageChops.add(img, glow.filter(ImageFilter.GaussianBlur(170)))
    d = ImageDraw.Draw(img, "RGBA")
    rnd = random.Random(seed)
    if STYLE["overlay"] == "code":
        # faint code rain on its own layer, faded out behind the text column
        mono = ImageFont.truetype(MONO, 20)
        cc = STYLE["code_color"]
        rain = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        rd_ = ImageDraw.Draw(rain)
        for x in range(14, W, 36):
            if rnd.random() < 0.45:
                continue
            y0 = rnd.randint(-400, H // 2)
            length = rnd.randint(8, 30)
            for k in range(length):
                y = y0 + k * 26
                if not 0 <= y < H:
                    continue
                ch = rnd.choice("0123456789ABCDEF" if rnd.random() < 0.6 else "01")
                a = 60 if k == length - 1 else int(8 + 26 * (k / length))
                rd_.text((x, y), ch, font=mono, fill=(*cc, a))
        # keep the rain strong only at the left/right edges, near-invisible mid-card
        fade = Image.new("L", (W, 1))
        for x in range(W):
            t = x / (W - 1)
            edge = max(0.0, 1 - min(t, 1 - t) / 0.16)  # 1 at edges, 0 by 16% in
            right = max(0.0, (t - 0.62) / 0.38) * 0.7  # extra presence behind the motif
            fade.putpixel((x, 0), int(255 * min(1.0, 0.12 + edge + right)))
        fade = fade.resize((W, H))
        rain.putalpha(ImageChops.multiply(rain.getchannel("A"), fade))
        img.paste(rain, (0, 0), rain)
        # CRT scanlines
        for y in range(0, H, 4):
            d.line((0, y, W, y), fill=(0, 0, 0, 38), width=1)
        # vignette
        vg = Image.new("L", (W, H), 0)
        ImageDraw.Draw(vg).rectangle((0, 0, W, H), fill=120)
        ImageDraw.Draw(vg).ellipse((-200, -150, W + 200, H + 150), fill=0)
        img.paste(Image.new("RGB", (W, H), (0, 0, 0)), (0, 0), vg.filter(ImageFilter.GaussianBlur(120)))
        d = ImageDraw.Draw(img, "RGBA")
    elif STYLE["overlay"] == "grid3d":
        # synthwave-style perspective floor in the lower third + horizon glow line
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        hz = int(H * 0.70)
        c1, c2 = STYLE["accent"]
        ld.line((0, hz, W, hz), fill=(*c2, 150), width=2)
        vx = W // 2
        for i in range(-24, 25):
            x_bot = vx + i * 120
            ld.line((vx + i * 6, hz, x_bot, H), fill=(*c1, 110), width=2)
        y, gap = hz + 6, 6.0
        while y < H:
            ld.line((0, int(y), W, int(y)), fill=(*c1, int(70 + 90 * (y - hz) / (H - hz))), width=2)
            gap *= 1.28
            y += gap
        # faint upper grid of dots
        for gy in range(40, hz - 20, 44):
            for gx in range(20, W, 44):
                ld.point((gx, gy), fill=(*c2, 40))
        # fade the floor toward the edges so it frames, not fights, the text
        mask = Image.new("L", (W, H), 0)
        ImageDraw.Draw(mask).rectangle((0, hz - 4, W, H), fill=255)
        mask = mask.filter(ImageFilter.GaussianBlur(10))
        lay.putalpha(ImageChops.multiply(lay.getchannel("A"), ImageChops.add(mask, Image.new("L", (W, H), 80))))
        img.paste(lay, (0, 0), lay)
        hglow = Image.new("L", (W, H), 0)
        ImageDraw.Draw(hglow).ellipse((-200, hz - 60, W + 200, hz + 60), fill=90)
        img.paste(Image.new("RGB", (W, H), c1), (0, 0), hglow.filter(ImageFilter.GaussianBlur(40)))
        d = ImageDraw.Draw(img, "RGBA")
        for yy in range(0, H, 4):
            d.line((0, yy, W, yy), fill=(0, 0, 0, 30), width=1)
    elif STYLE["overlay"] == "circuit":
        # PCB traces: orthogonal paths with 45-degree jogs and via pads, brightest at the edges
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        c1, c2 = STYLE["accent"]
        step = 30
        for _ in range(70):
            x = rnd.randrange(0, W, step)
            y = rnd.randrange(0, H, step)
            col = c1 if rnd.random() < 0.6 else c2
            a = rnd.randint(40, 110)
            pts = [(x, y)]
            for _seg in range(rnd.randint(3, 7)):
                dirn = rnd.choice([(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)])
                ln = rnd.randint(2, 7) * step
                x += dirn[0] * ln
                y += dirn[1] * ln
                pts.append((x, y))
            ld.line(pts, fill=(*col, a), width=3, joint="curve")
            ex, ey = pts[-1]
            ld.ellipse((ex - 7, ey - 7, ex + 7, ey + 7), outline=(*col, a + 60), width=3)
            sx, sy = pts[0]
            ld.ellipse((sx - 4, sy - 4, sx + 4, sy + 4), fill=(*col, a + 40))
        # chip outline, upper right
        cx0, cy0 = W - 330, 170
        ld.rounded_rectangle((cx0, cy0, cx0 + 220, cy0 + 220), 18, outline=(*c2, 90), width=4)
        for k in range(6):
            o = 30 + k * 32
            for (x1, y1, x2, y2) in ((cx0 + o, cy0 - 30, cx0 + o, cy0), (cx0 + o, cy0 + 220, cx0 + o, cy0 + 250),
                                     (cx0 - 30, cy0 + o, cx0, cy0 + o), (cx0 + 220, cy0 + o, cx0 + 250, cy0 + o)):
                ld.line((x1, y1, x2, y2), fill=(*c2, 80), width=4)
        fade = Image.new("L", (W, 1))
        for xx in range(W):
            t = xx / (W - 1)
            fade.putpixel((xx, 0), int(255 * min(1.0, 0.18 + max(0.0, 1 - min(t, 1 - t) / 0.2) + max(0.0, (t - 0.6) / 0.4) * 0.6)))
        lay.putalpha(ImageChops.multiply(lay.getchannel("A"), fade.resize((W, H))))
        img.paste(lay, (0, 0), lay)
        d = ImageDraw.Draw(img, "RGBA")
    elif STYLE["overlay"] == "netmap":
        # live-attack map: dotted globe, glowing nodes, arcs between them
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        c1, c2 = STYLE["accent"]
        gcx, gcy, gr = W - 215, 395, 205
        for lat in range(-80, 81, 6):
            import math
            yy = gcy + gr * math.sin(math.radians(lat))
            rr = gr * math.cos(math.radians(lat))
            for lon in range(0, 360, 5):
                xx = gcx + rr * math.sin(math.radians(lon))
                front = math.cos(math.radians(lon))
                if front < 0:
                    continue
                if rnd.random() < 0.55:
                    ld.point((xx, yy), fill=(*c2, int(30 + 50 * front)))
        nodes = []
        # nodes stay in a right-hand zone below the wordmark/logo row
        zx0, zx1, zy0, zy1 = W - 360, W - 70, 190, 600
        for _ in range(12):
            nodes.append((rnd.uniform(zx0, zx1), rnd.uniform(zy0, zy1)))
        for i in range(9):
            (x1, y1), (x2, y2) = rnd.sample(nodes, 2)
            mx = (x1 + x2) / 2 + rnd.uniform(-40, 40)
            my = max(zy0 - 10, min(y1, y2) - rnd.uniform(30, 90))
            pts = [((1 - t) ** 2 * x1 + 2 * (1 - t) * t * mx + t * t * x2, (1 - t) ** 2 * y1 + 2 * (1 - t) * t * my + t * t * y2) for t in [k / 40 for k in range(41)]]
            ld.line(pts, fill=(*c1, 120), width=2)
        for (nx, ny) in nodes:
            ld.ellipse((nx - 14, ny - 14, nx + 14, ny + 14), outline=(*c1, 90), width=2)
            ld.ellipse((nx - 5, ny - 5, nx + 5, ny + 5), fill=(*c2, 220))
        glow = lay.filter(ImageFilter.GaussianBlur(6))
        img.paste(glow, (0, 0), glow)
        img.paste(lay, (0, 0), lay)
        d = ImageDraw.Draw(img, "RGBA")
        for yy in range(0, H, 4):
            d.line((0, yy, W, yy), fill=(0, 0, 0, 26), width=1)
    elif STYLE["overlay"] == "video":
        # editing-suite art in the upper-right: preview monitor + play button,
        # 3-track timeline with playhead, scissors at the cut, AI chat bubble,
        # plus a faint film strip down the right edge
        strip = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        sd = ImageDraw.Draw(strip)
        fx = W - 46
        sd.rectangle((fx, 0, fx + 30, H), fill=(255, 255, 255, 10))
        for yy in range(18, H, 44):
            sd.rounded_rectangle((fx + 7, yy, fx + 23, yy + 22), 4, fill=(255, 255, 255, 22))
        img.paste(strip, (0, 0), strip)
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        c1, c2 = STYLE["accent"]
        # preview monitor
        mx0, my0, mx1, my1 = W - 400, 190, W - 80, 390
        ld.rounded_rectangle((mx0, my0, mx1, my1), 22, outline=(*c1, 120), width=4, fill=(*c1, 18))
        ld.rounded_rectangle((mx0 + 14, my0 + 14, mx1 - 14, my1 - 40), 12, fill=(255, 255, 255, 10))
        pcx, pcy = (mx0 + mx1) // 2, (my0 + my1 - 26) // 2
        ld.ellipse((pcx - 46, pcy - 46, pcx + 46, pcy + 46), outline=(*c2, 150), width=4)
        ld.polygon([(pcx - 14, pcy - 24), (pcx - 14, pcy + 24), (pcx + 26, pcy)], fill=(*c2, 170))
        # scrub bar under the picture
        sy = my1 - 22
        ld.line((mx0 + 24, sy, mx1 - 24, sy), fill=(255, 255, 255, 40), width=4)
        ld.line((mx0 + 24, sy, mx0 + 24 + int((mx1 - mx0 - 48) * 0.42), sy), fill=(*c2, 170), width=4)
        ld.ellipse((mx0 + 24 + int((mx1 - mx0 - 48) * 0.42) - 7, sy - 7, mx0 + 24 + int((mx1 - mx0 - 48) * 0.42) + 7, sy + 7), fill=(*c2, 220))
        # 3-track timeline
        tx0, tx1 = W - 400, W - 80
        tracks = [(420, c1), (468, c2), (516, (180, 150, 255))]
        for ty, col in tracks:
            x = tx0
            while x < tx1 - 20:
                wdt = rnd.randint(40, 110)
                x2 = min(x + wdt, tx1)
                ld.rounded_rectangle((x, ty, x2 - 6, ty + 34), 7, fill=(*col, 70), outline=(*col, 140), width=2)
                x = x2
        # audio waveform on the bottom track
        wy = 516 + 17
        for xx in range(tx0 + 6, tx1 - 6, 6):
            amp = rnd.randint(3, 14)
            ld.line((xx, wy - amp, xx, wy + amp), fill=(255, 255, 255, 70), width=2)
        # playhead + scissors at the cut
        phx = tx0 + int((tx1 - tx0) * 0.58)
        ld.line((phx, 404, phx, 566), fill=(255, 255, 255, 170), width=3)
        ld.polygon([(phx - 9, 398), (phx + 9, 398), (phx, 410)], fill=(255, 255, 255, 200))
        sx, sy2 = phx, 600
        ld.ellipse((sx - 34, sy2 - 2, sx - 12, sy2 + 20), outline=(*c2, 170), width=4)
        ld.ellipse((sx + 12, sy2 - 2, sx + 34, sy2 + 20), outline=(*c2, 170), width=4)
        ld.line((sx - 16, sy2 + 2, sx + 6, sy2 - 36), fill=(*c2, 170), width=4)
        ld.line((sx + 16, sy2 + 2, sx - 6, sy2 - 36), fill=(*c2, 170), width=4)
        # AI chat bubble with sparkle, left of the monitor
        bx0, by0 = W - 520, 236
        ld.rounded_rectangle((bx0, by0, bx0 + 96, by0 + 64), 18, fill=(*c1, 60), outline=(*c1, 150), width=3)
        ld.polygon([(bx0 + 70, by0 + 62), (bx0 + 96, by0 + 84), (bx0 + 88, by0 + 58)], fill=(*c1, 60))
        scx, scy = bx0 + 48, by0 + 32
        ld.polygon([(scx, scy - 20), (scx + 6, scy - 6), (scx + 20, scy), (scx + 6, scy + 6), (scx, scy + 20), (scx - 6, scy + 6), (scx - 20, scy), (scx - 6, scy - 6)], fill=(255, 255, 255, 200))
        if kind in ("points", "action"):
            # list cards: titles sit where the art lives — drop it behind the glass rows, dimmer
            moved = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            moved.paste(lay, (0, 330))
            r, g_, b, a = moved.split()
            lay = Image.merge("RGBA", (r, g_, b, a.point(lambda v: int(v * 0.6))))
        glow = lay.filter(ImageFilter.GaussianBlur(5))
        img.paste(glow, (0, 0), glow)
        img.paste(lay, (0, 0), lay)
        d = ImageDraw.Draw(img, "RGBA")
    elif STYLE["overlay"] == "education":
        # classroom art, upper-right: chalkboard with a formula + bar chart,
        # graduation cap above it, open book below with a lightbulb rising out,
        # an AI sparkle bubble and a pencil; faint ruled-notebook lines on the card
        ruled = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        rd2 = ImageDraw.Draw(ruled)
        for yy in range(60, H, 46):
            rd2.line((0, yy, W, yy), fill=(255, 255, 255, 9), width=1)
        rd2.line((40, 0, 40, H), fill=(255, 120, 140, 16), width=2)
        img.paste(ruled, (0, 0), ruled)
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        c1, c2 = STYLE["accent"]
        c3 = (255, 200, 90)
        # chalkboard
        bx0, by0, bx1, by1 = W - 380, 250, W - 92, 430
        ld.rounded_rectangle((bx0 - 10, by0 - 10, bx1 + 10, by1 + 10), 16, fill=(*c1, 40), outline=(*c1, 160), width=4)
        ld.rounded_rectangle((bx0, by0, bx1, by1), 10, fill=(10, 40, 40, 120))
        mono = ImageFont.truetype(MONO, 30)
        ld.text((bx0 + 20, by0 + 18), "y = ax + b", font=mono, fill=(255, 255, 255, 170))
        for k, hgt in enumerate((40, 70, 55, 95)):
            x = bx0 + 24 + k * 34
            ld.rectangle((x, by1 - 20 - hgt, x + 22, by1 - 20), fill=(*(c2 if k % 2 else c1), 150))
        ld.line((bx0 + 20, by1 - 20, bx0 + 170, by1 - 20), fill=(255, 255, 255, 120), width=2)
        # small atom on the board
        ax, ay = bx1 - 64, by1 - 66
        ld.ellipse((ax - 34, ay - 13, ax + 34, ay + 13), outline=(*c2, 170), width=3)
        ld.ellipse((ax - 13, ay - 34, ax + 13, ay + 34), outline=(*c2, 170), width=3)
        ld.ellipse((ax - 6, ay - 6, ax + 6, ay + 6), fill=(255, 255, 255, 210))
        # graduation cap above the board
        gx, gy = W - 236, 196
        ld.polygon([(gx, gy - 34), (gx + 86, gy), (gx, gy + 34), (gx - 86, gy)], fill=(*c1, 90), outline=(*c1, 200))
        ld.line([(gx, gy - 34), (gx + 86, gy), (gx, gy + 34), (gx - 86, gy), (gx, gy - 34)], fill=(*c1, 200), width=3)
        ld.rectangle((gx - 46, gy + 14, gx + 46, gy + 40), fill=(*c1, 70))
        ld.line((gx + 64, gy + 8, gx + 64, gy + 50), fill=(*c3, 210), width=3)
        ld.ellipse((gx + 58, gy + 48, gx + 70, gy + 60), fill=(*c3, 230))
        # open book under the board
        ox, oy = W - 236, 520
        for s in (-1, 1):
            pts = [(ox, oy), (ox + s * 120, oy - 22), (ox + s * 120, oy + 56), (ox, oy + 78)]
            ld.polygon(pts, fill=(255, 255, 255, 40), outline=(*c2, 190))
            ld.line(pts + [pts[0]], fill=(*c2, 190), width=3)
            for k in range(3):
                yy = oy + 10 + k * 16
                ld.line((ox + s * 18, yy + 2, ox + s * 100, yy - 14), fill=(255, 255, 255, 90), width=3)
        # lightbulb rising from the book
        lx, ly = ox, 470
        ld.ellipse((lx - 26, ly - 30, lx + 26, ly + 22), fill=(*c3, 120), outline=(*c3, 230), width=3)
        ld.rectangle((lx - 12, ly + 20, lx + 12, ly + 34), fill=(*c3, 170))
        for ang in (-60, -30, 0, 30, 60):
            import math
            r0, r1 = 40, 56
            ca, sa = math.sin(math.radians(ang)), -math.cos(math.radians(ang))
            ld.line((lx + ca * r0, ly - 4 + sa * r0, lx + ca * r1, ly - 4 + sa * r1), fill=(*c3, 200), width=3)
        # AI sparkle bubble left of the board
        sbx, sby = W - 520, 176
        ld.rounded_rectangle((sbx, sby, sbx + 96, sby + 64), 18, fill=(*c1, 60), outline=(*c1, 150), width=3)
        ld.polygon([(sbx + 70, sby + 62), (sbx + 96, sby + 84), (sbx + 88, sby + 58)], fill=(*c1, 60))
        scx, scy = sbx + 48, sby + 32
        ld.polygon([(scx, scy - 20), (scx + 6, scy - 6), (scx + 20, scy), (scx + 6, scy + 6), (scx, scy + 20), (scx - 6, scy + 6), (scx - 20, scy), (scx - 6, scy - 6)], fill=(255, 255, 255, 200))
        # pencil leaning on the book
        px0, py0 = W - 92, 470
        ld.line((px0, py0, px0 - 70, py0 + 110), fill=(*c3, 200), width=12)
        ld.polygon([(px0 - 76, py0 + 104), (px0 - 64, py0 + 116), (px0 - 82, py0 + 128)], fill=(255, 230, 200, 220))
        if kind in ("points", "action"):
            moved = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            moved.paste(lay, (0, 330))
            r, g_, b, a = moved.split()
            lay = Image.merge("RGBA", (r, g_, b, a.point(lambda v: int(v * 0.6))))
        glow = lay.filter(ImageFilter.GaussianBlur(5))
        img.paste(glow, (0, 0), glow)
        img.paste(lay, (0, 0), lay)
        d = ImageDraw.Draw(img, "RGBA")
    elif STYLE["overlay"] == "diagram":
        # whiteboard dot grid over the whole card, then a small flowchart in the
        # upper-right: start pill -> box -> decision diamond -> two boxes,
        # orthogonal arrows, a database cylinder, an AI sparkle bubble and a cursor
        grid = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        gd = ImageDraw.Draw(grid)
        for gy in range(20, H, 32):
            for gx in range(20, W, 32):
                gd.ellipse((gx - 1, gy - 1, gx + 1, gy + 1), fill=(255, 255, 255, 26))
        img.paste(grid, (0, 0), grid)
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        c1, c2 = STYLE["accent"]
        c3 = (180, 150, 255)

        def arrow(pts: list[tuple[int, int]], col: tuple[int, int, int]) -> None:
            ld.line(pts, fill=(*col, 170), width=4, joint="curve")
            (ax, ay), (bx, by) = pts[-2], pts[-1]
            if bx == ax:
                s = 1 if by > ay else -1
                ld.polygon([(bx - 10, by - 14 * s), (bx + 10, by - 14 * s), (bx, by)], fill=(*col, 210))
            else:
                s = 1 if bx > ax else -1
                ld.polygon([(bx - 14 * s, by - 10), (bx - 14 * s, by + 10), (bx, by)], fill=(*col, 210))

        cx = W - 250  # flow spine
        # start pill
        ld.rounded_rectangle((cx - 70, 184, cx + 70, 226), 21, fill=(*c2, 60), outline=(*c2, 170), width=3)
        arrow([(cx, 226), (cx, 262)], (255, 255, 255))
        # process box with text lines
        ld.rounded_rectangle((cx - 95, 262, cx + 95, 330), 12, fill=(*c1, 50), outline=(*c1, 170), width=3)
        for k, ln in enumerate((120, 90)):
            ld.rounded_rectangle((cx - 60, 282 + k * 18, cx - 60 + ln, 290 + k * 18), 4, fill=(255, 255, 255, 90))
        arrow([(cx, 330), (cx, 366)], (255, 255, 255))
        # decision diamond
        ld.polygon([(cx, 366), (cx + 62, 420), (cx, 474), (cx - 62, 420)], fill=(*c3, 55), outline=(*c3, 190))
        ld.line([(cx, 366), (cx + 62, 420), (cx, 474), (cx - 62, 420), (cx, 366)], fill=(*c3, 190), width=3)
        # branches: "yes" straight down, "no" out to the right — nothing to the left,
        # where the headline sits
        lx, rx = cx, cx + 135
        arrow([(cx, 474), (lx, 520)], c2)
        arrow([(cx + 62, 420), (rx, 420), (rx, 520)], c1)
        ld.rounded_rectangle((lx - 56, 520, lx + 56, 578), 12, fill=(*c2, 50), outline=(*c2, 170), width=3)
        ld.rounded_rectangle((rx - 50, 520, rx + 50, 578), 12, fill=(*c1, 50), outline=(*c1, 170), width=3)
        for bx_ in (lx, rx):
            ld.rounded_rectangle((bx_ - 32, 542, bx_ + 24, 550), 4, fill=(255, 255, 255, 90))
        # database cylinder, dashed link from the right box
        dbx, dby = rx, 640
        ld.rectangle((dbx - 36, dby, dbx + 36, dby + 54), fill=(*c1, 40))
        ld.line((dbx - 36, dby, dbx - 36, dby + 54), fill=(*c1, 160), width=3)
        ld.line((dbx + 36, dby, dbx + 36, dby + 54), fill=(*c1, 160), width=3)
        ld.ellipse((dbx - 36, dby - 12, dbx + 36, dby + 12), fill=(*c1, 70), outline=(*c1, 170), width=3)
        ld.arc((dbx - 36, dby + 42, dbx + 36, dby + 66), 0, 180, fill=(*c1, 160), width=3)
        for yy in range(580, 626, 12):
            ld.line((dbx, yy, dbx, yy + 6), fill=(*c1, 150), width=3)
        # AI sparkle bubble, left of the start pill
        bx0, by0 = cx - 250, 196
        ld.rounded_rectangle((bx0, by0, bx0 + 96, by0 + 64), 18, fill=(*c1, 60), outline=(*c1, 150), width=3)
        ld.polygon([(bx0 + 70, by0 + 62), (bx0 + 96, by0 + 84), (bx0 + 88, by0 + 58)], fill=(*c1, 60))
        scx, scy = bx0 + 48, by0 + 32
        ld.polygon([(scx, scy - 20), (scx + 6, scy - 6), (scx + 20, scy), (scx + 6, scy + 6), (scx, scy + 20), (scx - 6, scy + 6), (scx - 20, scy), (scx - 6, scy - 6)], fill=(255, 255, 255, 200))
        # pointer cursor dragging the right box
        px, py = rx + 26, 566
        ld.polygon([(px, py), (px, py + 40), (px + 11, py + 30), (px + 19, py + 46), (px + 26, py + 43), (px + 18, py + 27), (px + 31, py + 27)],
                   fill=(255, 255, 255, 230), outline=(20, 20, 30, 255))
        if kind in ("points", "action"):
            moved = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            moved.paste(lay, (0, 330))
            r, g_, b, a = moved.split()
            lay = Image.merge("RGBA", (r, g_, b, a.point(lambda v: int(v * 0.6))))
        glow = lay.filter(ImageFilter.GaussianBlur(5))
        img.paste(glow, (0, 0), glow)
        img.paste(lay, (0, 0), lay)
        d = ImageDraw.Draw(img, "RGBA")
    else:
        for i in range(-H, W, 90):
            d.line((i, 0, i + H, H), fill=(255, 255, 255, 6), width=1)
    pc = STYLE["particles"]
    for _ in range(70):
        x, y = rnd.randint(0, W), rnd.randint(0, H)
        r = rnd.choice([1, 1, 2, 2, 3])
        d.ellipse((x - r, y - r, x + r, y + r), fill=(*pc, rnd.randint(30, 100)))
    return img


def glass(img: Image.Image, box: tuple[int, int, int, int], radius: int = 36, tint: int = 22) -> None:
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    region = img.crop(box).filter(ImageFilter.GaussianBlur(28))
    region = ImageEnhance.Brightness(ImageEnhance.Color(region).enhance(1.35)).enhance(1.08)
    white = Image.new("RGB", (w, h), (255, 255, 255))
    region = Image.composite(white, region, Image.new("L", (w, h), tint))  # alpha-scaled mask, never RGBA paste
    spec = Image.new("L", (w, h), 0)
    ImageDraw.Draw(spec).ellipse((-w * 0.4, -h * 1.1, w * 0.9, h * 0.45), fill=34)
    region = Image.composite(white, region, spec.filter(ImageFilter.GaussianBlur(40)))
    shade = Image.new("L", (w, h), 0)
    ImageDraw.Draw(shade).rectangle((0, int(h * 0.72), w, h), fill=40)
    region = Image.composite(Image.new("RGB", (w, h), (0, 0, 0)), region, shade.filter(ImageFilter.GaussianBlur(30)))
    sh = Image.new("L", (W, H), 0)
    ImageDraw.Draw(sh).rounded_rectangle((x0 + 6, y0 + 18, x1 + 6, y1 + 18), radius, fill=90)
    img.paste(Image.new("RGB", (W, H), (0, 0, 0)), (0, 0), sh.filter(ImageFilter.GaussianBlur(26)))
    img.paste(region, (x0, y0), rrect_mask((w, h), radius))
    rim = Image.new("L", (w, h), 0)
    ImageDraw.Draw(rim).rounded_rectangle((0, 0, w - 1, h - 1), radius, outline=150, width=2)
    img.paste(h_gradient(w, h, *STYLE["rim"]), (x0, y0), rim)
    d = ImageDraw.Draw(img, "RGBA")
    d.arc((x0 + 1, y0 + 1, x0 + radius * 2, y0 + radius * 2), 180, 270, fill=(255, 255, 255, 170), width=2)
    d.line((x0 + radius, y0 + 1, x0 + w * 0.55, y0 + 1), fill=(255, 255, 255, 140), width=2)


def text(img: Image.Image, xy: tuple[int, int], s: str, f: MixFont, fill: Any = INK) -> None:
    f.draw(ImageDraw.Draw(img), xy, s, fill)


def gradient_text(img: Image.Image, xy: tuple[int, int], s: str, f: MixFont, brand: bool = False) -> None:
    m = Image.new("L", (W, H), 0)
    f.draw(ImageDraw.Draw(m), xy, s, 255)
    bb = m.getbbox()
    if not bb:
        return
    layer = Image.new("RGB", (W, H))
    c1, c2 = BRAND_TEXT if brand else STYLE["accent_text"]
    layer.paste(h_gradient(bb[2] - bb[0] + 2, bb[3] - bb[1] + 2, c1, c2), (bb[0], bb[1]))
    img.paste(layer, (0, 0), m)


def wrap(s: str, f: MixFont, max_w: int) -> list[str]:
    """Wrap on spaces only — Lao has no safe character-level break."""
    lines: list[str] = []
    cur = ""
    for word in s.split(" "):
        trial = (cur + " " + word).strip()
        if not cur or f.length(trial) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def pill(img: Image.Image, x: int, y: int, label: str, f: MixFont, highlight: bool) -> tuple[int, int]:
    pw, ph = f.length(label) + 44, f.height() + 14
    if highlight:
        img.paste(h_gradient(pw, ph), (x, y), rrect_mask((pw, ph), ph // 2))
        text(img, (x + 22, y + 7), label, f, (255, 255, 255))
    else:
        d = ImageDraw.Draw(img, "RGBA")
        d.rounded_rectangle((x, y, x + pw, y + ph), ph // 2, fill=(255, 255, 255, 26), outline=(255, 255, 255, 70), width=2)
        text(img, (x + 22, y + 7), label, f)
    return pw, ph


def pill_row(img: Image.Image, y: int, labels: Sequence[str], f: MixFont, first_highlight: bool = False, gap: int = 14) -> int:
    """Lays out pills, wrapping to a new row inside the safe zone. Returns bottom y."""
    x, row_h = SAFE_X, 0
    for i, lab in enumerate(labels):
        pw = f.length(lab) + 44
        if x > SAFE_X and x + pw > W - SAFE_X:
            x, y = SAFE_X, y + row_h + gap
        w_, h_ = pill(img, x, y, lab, f, first_highlight and i == 0)
        x += w_ + gap
        row_h = h_
    return y + row_h


LOGO_CANDIDATES = [
    Path(__file__).resolve().parent / "brand" / "arnfar-logo.png",
    Path(__file__).resolve().parent / "arnfar-icon" / "arnfar-logo.png",
    Path(__file__).resolve().parent.parent / "arnfar-icon" / "arnfar-logo.png",
]
_logo_cache: dict[int, Image.Image] = {}


def logo(size: int) -> Image.Image:
    """The real Arnfar mark (arnfar-logo.png), cropped to its circle, RGBA, size x size.

    Refuses to fall back to a drawn stand-in: a card with a fake logo must not ship.
    """
    if size in _logo_cache:
        return _logo_cache[size]
    src = next((p for p in LOGO_CANDIDATES if p.exists()), None)
    if src is None:
        sys.exit("Arnfar logo missing: copy arnfar-icon/arnfar-logo.png into ./brand/ — never draw a substitute")
    im = Image.open(src).convert("RGBA")
    bb = im.getchannel("A").getbbox()
    if bb:
        im = im.crop(bb)
    side = max(im.size)
    sq = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    sq.paste(im, ((side - im.width) // 2, (side - im.height) // 2), im)
    out = sq.resize((size, size), Image.LANCZOS)
    _logo_cache[size] = out
    return out


def paste_logo(img: Image.Image, x: int, y: int, size: int) -> None:
    """Logo on a soft white disc so the thin outer ring and the 'ao' stay legible on any background."""
    disc = Image.new("L", (size, size), 0)
    ImageDraw.Draw(disc).ellipse((0, 0, size - 1, size - 1), fill=235)
    img.paste(Image.new("RGB", (size, size), (255, 255, 255)), (x, y), disc)
    lg = logo(size)
    img.paste(lg, (x, y), lg)


def chrome(img: Image.Image, tags: Sequence[str], hashtags: Sequence[str], ad: dict[str, str]) -> None:
    pill_row(img, SAFE_Y, tags, font(28), first_highlight=True, gap=12)
    # top-right: real logo + wordmark
    fw = font(46)
    wm_w = fw.length("Arnfar")
    lsz = 58
    wx = W - SAFE_X - wm_w
    paste_logo(img, wx - lsz - 12, SAFE_Y - 6, lsz)
    gradient_text(img, (wx, SAFE_Y - 2), "Arnfar", fw, brand=True)
    # hashtags
    fh = font(26)
    y = H - SAFE_Y - 156
    x = SAFE_X
    for t in hashtags:
        x += pill(img, x, y, t, fh, False)[0] + 10
    # ad band with the real logo
    band_y0 = H - SAFE_Y - 84
    glass(img, (SAFE_X, band_y0, W - SAFE_X, H - SAFE_Y), radius=24, tint=16)
    bsz = 58
    mx, my = SAFE_X + 22, band_y0 + (84 - bsz) // 2
    paste_logo(img, mx, my, bsz)
    fa = font(28)
    tx = mx + bsz + 18
    gradient_text(img, (tx, band_y0 + 20), ad.get("brand", "Arnfar"), fa, brand=True)
    text(img, (tx + fa.length(ad.get("brand", "Arnfar")) + 14, band_y0 + 20), ad.get("text", ""), fa, STYLE["ink_soft"])


def motif(img: Image.Image, name: str) -> None:
    if STYLE.get("overlay") in ("circuit", "netmap", "video", "diagram", "education"):
        return  # the backdrop art already fills the upper-right
    d = ImageDraw.Draw(img, "RGBA")
    cx, cy = W - 215, 320
    m1, m2 = STYLE["motif"]
    blue, green = (*m1, 80), (*m2, 90)
    if name == "shield":
        d.polygon([(cx, cy - 170), (cx + 140, cy - 110), (cx + 130, cy + 40), (cx, cy + 170), (cx - 130, cy + 40), (cx - 140, cy - 110)], outline=blue, width=5)
        d.rounded_rectangle((cx - 55, cy - 10, cx + 55, cy + 80), 14, outline=green, width=5)
        d.arc((cx - 38, cy - 70, cx + 38, cy + 10), 180, 360, fill=green, width=5)
        for dx, dy in [(-300, -40), (-260, 60), (-330, 140)]:
            d.line((cx - 140, cy + dy // 2, cx + dx, cy + dy), fill=(*m1, 45), width=3)
            d.ellipse((cx + dx - 7, cy + dy - 7, cx + dx + 7, cy + dy + 7), outline=blue, width=3)
    elif name == "chart":
        for i, h_ in enumerate([90, 150, 120, 210, 260]):
            x = cx - 150 + i * 66
            d.rounded_rectangle((x, cy + 120 - h_, x + 44, cy + 120), 8, outline=blue if i < 4 else green, width=5)
        d.line((cx - 160, cy + 140, cx + 180, cy + 140), fill=blue, width=4)


def check_icon(img: Image.Image, x: int, y: int, s: int = 56) -> None:
    img.paste(h_gradient(s, s), (x, y), rrect_mask((s, s), s // 2))
    ImageDraw.Draw(img).line([(x + s * 0.27, y + s * 0.52), (x + s * 0.44, y + s * 0.68), (x + s * 0.74, y + s * 0.34)], fill=(255, 255, 255), width=6, joint="curve")


# ---------------------------------------------------------------- card kinds


def card_hero(img: Image.Image, c: dict[str, Any]) -> None:
    motif(img, c.get("motif", "shield"))
    max_w = W - 2 * SAFE_X
    y = 300
    text(img, (SAFE_X, y), c.get("eyebrow", ""), font(30), STYLE["ink_soft"])
    y += 70
    fH = font(84)
    for line in c["headline"]:
        text(img, (SAFE_X, y), line, fH)
        y += int(fH.size * LINE_H)
    if c.get("accent"):
        fA = font(64)
        gradient_text(img, (SAFE_X, y), c["accent"], fA)
        y += int(fA.size * LINE_H) + 26
    fS = font(36)
    sub = [l for s in c.get("subhead", []) for l in wrap(s, fS, max_w - 90)]
    if sub:
        ph = 54 + int(len(sub) * fS.size * LINE_H) + 18
        glass(img, (SAFE_X, y, W - SAFE_X, y + ph), radius=30)
        img.paste(h_gradient(8, ph - 56), (SAFE_X + 30, y + 28), rrect_mask((8, ph - 56), 4))
        ty = y + 30
        for l in sub:
            text(img, (SAFE_X + 62, ty), l, fS)
            ty += int(fS.size * LINE_H)
        y += ph + 34
    if c.get("chips"):
        y = pill_row(img, y, c["chips"], font(30)) + 30
    if c.get("date"):
        text(img, (SAFE_X, y), c["date"], font(26), STYLE["ink_soft"])


def card_stat(img: Image.Image, c: dict[str, Any]) -> None:
    motif(img, c.get("motif", ""))
    max_w = W - 2 * SAFE_X
    y = 300
    for l in wrap(c.get("label_top", ""), font(36), max_w):
        text(img, (SAFE_X, y), l, font(36), STYLE["ink_soft"])
        y += int(36 * LINE_H)
    y += 10
    box = (SAFE_X, y, W - SAFE_X, y + 470)
    glass(img, box, radius=44)
    fV = font(250)
    vw = fV.length(c["value"])
    gradient_text(img, ((W - vw) // 2, y + 10), c["value"], fV)
    fL = font(44)
    ly = y + 330
    for l in wrap(c.get("label", ""), fL, max_w - 80):
        text(img, ((W - fL.length(l)) // 2, ly), l, fL)
        ly += int(fL.size * LINE_H)
    y = box[3] + 40
    if c.get("chips"):
        y = pill_row(img, y, c["chips"], font(30)) + 30
    if c.get("note"):
        for l in wrap(c["note"], font(28), max_w):
            text(img, (SAFE_X, y), l, font(28), STYLE["ink_soft"])
            y += int(28 * LINE_H)


def card_points(img: Image.Image, c: dict[str, Any]) -> None:
    max_w = W - 2 * SAFE_X
    y = 210
    text(img, (SAFE_X, y), c.get("eyebrow", ""), font(30), STYLE["ink_soft"])
    y += 62
    fT = font(72)
    text(img, (SAFE_X, y), c["title"], fT)
    y += int(fT.size * LINE_H) + 6
    img.paste(h_gradient(150, 8), (SAFE_X, y), rrect_mask((150, 8), 4))
    y += 50
    bottom = H - SAFE_Y - 156 - 30  # stay above the hashtag row
    items = c["items"]
    # shrink fonts/gaps until every row fits above the footer
    for fi, fsub, pad in ((38, 30, 44), (34, 27, 36), (31, 25, 30)):
        fN, fI, fs = font(52), font(fi), font(fsub)
        rows = []
        for it in items:
            tl = wrap(it["title"], fI, max_w - 170)
            sl = wrap(it.get("sub", ""), fs, max_w - 170) if it.get("sub") else []
            rh = pad + int(len(tl) * fI.size * LINE_H) + int(len(sl) * fs.size * LINE_H) + 20
            rows.append((tl, sl, rh))
        total = sum(r[2] for r in rows)
        gap = (bottom - y - total) / max(1, len(rows) - 1)
        if gap >= 18:
            gap = min(gap, 52)
            break
    else:
        sys.exit(f"points card '{c['title']}' has too many/long items to fit — shorten them")
    for i, (tl, sl, rh) in enumerate(rows, 1):
        glass(img, (SAFE_X, y, W - SAFE_X, y + rh), radius=30)
        bx, by = SAFE_X + 30, y + (rh - 84) // 2
        img.paste(h_gradient(84, 84), (bx, by), rrect_mask((84, 84), 24))
        n = str(i)
        text(img, (bx + (84 - fN.length(n)) // 2, by + (84 - fN.height()) // 2), n, fN, (255, 255, 255))
        ty = y + (rh - (int(len(tl) * fI.size * LINE_H) + int(len(sl) * fs.size * LINE_H))) // 2 - 4
        for l in tl:
            text(img, (SAFE_X + 140, ty), l, fI)
            ty += int(fI.size * LINE_H)
        for l in sl:
            text(img, (SAFE_X + 140, ty), l, fs, STYLE["ink_soft"])
            ty += int(fs.size * LINE_H)
        y += rh + int(gap)


def card_action(img: Image.Image, c: dict[str, Any]) -> None:
    max_w = W - 2 * SAFE_X
    y = 210
    text(img, (SAFE_X, y), c.get("eyebrow", ""), font(30), STYLE["ink_soft"])
    y += 62
    fT = font(64)
    for l in wrap(c["title"], fT, max_w):
        text(img, (SAFE_X, y), l, fT)
        y += int(fT.size * LINE_H)
    img.paste(h_gradient(150, 8), (SAFE_X, y + 6), rrect_mask((150, 8), 4))
    y += 60
    fI = font(36)
    items = [wrap(s, fI, max_w - 150) for s in c["items"]]
    ph = 40 + sum(int(len(t) * fI.size * LINE_H) + 34 for t in items)
    glass(img, (SAFE_X, y, W - SAFE_X, y + ph), radius=36)
    ty = y + 36
    for t in items:
        check_icon(img, SAFE_X + 34, ty + 2)
        for l in t:
            text(img, (SAFE_X + 116, ty), l, fI)
            ty += int(fI.size * LINE_H)
        ty += 34
    y += ph + 40
    if c.get("takeaway"):
        fK = font(40)
        for l in wrap(c["takeaway"], fK, max_w):
            gradient_text(img, (SAFE_X, y), l, fK)
            y += int(fK.size * LINE_H)
        y += 10
    if c.get("note"):
        for l in wrap(c["note"], font(28), max_w):
            text(img, (SAFE_X, y), l, font(28), STYLE["ink_soft"])
            y += int(28 * LINE_H)


KINDS = {"hero": card_hero, "stat": card_stat, "points": card_points, "action": card_action}


def render(spec: dict[str, Any], outdir: Path) -> list[Path]:
    cards = spec["cards"]
    if len(cards) != CARD_COUNT:
        sys.exit(f"spec has {len(cards)} cards — every set must be exactly {CARD_COUNT}")
    set_style(spec.get("style", "default"))
    global BG_IMAGE, BG_SHIFT_X, BG_SCALE
    BG_IMAGE = Path(spec["bg_image"]) if spec.get("bg_image") else None
    BG_SHIFT_X = int(spec.get("bg_shift_x", 0))
    BG_SCALE = float(spec.get("bg_scale", 1.0))
    if BG_IMAGE is not None and not BG_IMAGE.exists():
        sys.exit(f"bg_image not found: {BG_IMAGE}")
    outdir.mkdir(parents=True, exist_ok=True)
    seed = abs(hash(spec.get("prefix", "arnfar"))) % 10_000
    paths: list[Path] = []
    for i, c in enumerate(cards, 1):
        kind = c.get("kind")
        if kind not in KINDS:
            sys.exit(f"card {i}: unknown kind {kind!r} (use {sorted(KINDS)})")
        img = background(seed, kind)
        chrome(img, c.get("tags", spec.get("tags", [])), c.get("hashtags", spec.get("hashtags", [])), spec.get("ad", {}))
        KINDS[kind](img, c)
        p = outdir / f"{spec.get('prefix', 'arnfar')}-{i:02d}.png"
        img.save(p, optimize=True)
        paths.append(p)
    return paths


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("spec", type=Path)
    ap.add_argument("--outdir", type=Path, default=Path("output"))
    a = ap.parse_args()
    spec = json.loads(a.spec.read_text(encoding="utf-8"))
    print(f"style: {spec.get('style', 'default')} | font: {PRIMARY_PATH.name} (fallback for uncovered glyphs: {FALLBACK_FONT.name if FALLBACK_FONT.exists() else 'none'})")
    for p in render(spec, a.outdir):
        print(p)


if __name__ == "__main__":
    main()

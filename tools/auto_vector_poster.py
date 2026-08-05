#!/usr/bin/env python3
"""auto_vector_poster.py — auto-examine Arnfar post content and generate a
true-vector (SVG) liquid-glass poster + background, with optional PNG export.

Pipeline:
  1. ANALYZE   input is a post .md file path OR raw text (auto-detected).
               Extracts: headline, hook/subhead, topic (-> category label +
               motif), key stat, pros/cons (✅/❌ lines), chips (hashtags),
               date. All Lao text is normalized via tools/lao_fix.py
               (dictionary word correction included).
  2. DESIGN    emits a scalable SVG in the Arnfar liquid-glass style:
               navy gradient + grid + blue/green orb background, frosted
               glass panels (real backdrop blur via clipped <use> + filter),
               specular sweep, brand blue->green hairlines.
  3. EXPORT    renders PNG via resvg_py, tools/bin/resvg-<platform>, or
               rsvg-convert — whichever is available. By default only the
               PNG is kept on disk; pass --svg to also save the .svg (the
               SVG is always saved automatically if PNG export fails, or in
               --bg-only mode, or with --no-png, since it'd otherwise be the
               only output).

Usage:
    python3 tools/auto_vector_poster.py posts/2026-07-05-claude-sonnet5-launch.md
    python3 tools/auto_vector_poster.py "ຫົວຂໍ້ ຫຼື ເນື້ອຫາທີ່ຢາກເຮັດໂປສເຕີ..."
    python3 tools/auto_vector_poster.py post.md --size square --outdir output/vector
    python3 tools/auto_vector_poster.py post.md --svg            # also keep the .svg
    python3 tools/auto_vector_poster.py post.md --bg-only        # background SVG (+ PNG)
    python3 tools/auto_vector_poster.py post.md --no-png         # SVG only, skip raster export
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import html
import os
import platform
import random
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

TOOLS_DIR = Path(__file__).resolve().parent
REPO = TOOLS_DIR.parent
sys.path.insert(0, str(TOOLS_DIR))
from lao_fix import Options, normalize_lao  # noqa: E402

# ---- brand ----
BLUE = "#0394F1"
GREEN = "#15C67A"
INK = "#ECF2FA"
MUTE = "#96A5BA"
EYEBROW = "#21C68A"
BG0 = "#0E1022"
BG1 = "#090C1A"
FONT_FAMILY = "Arnfar Font"          # all text renders in Regular weight
DEFAULT_TAGS = "#arnfar   #ArnfarERP   #arnfar.com"
LOGO_PNG = REPO / "arnfar-icon" / "arnfar-nobg.png"

SIZES = {"portrait": (1080, 1350), "square": (1080, 1080),
         "landscape": (1200, 630), "story": (1080, 1920)}

# ----------------------------------------------------------------------------
# 1. ANALYZE
# ----------------------------------------------------------------------------

_EMOJI_RE = re.compile(
    "[\U0001F000-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF"
    "\U00002B00-\U00002BFF\U0000FE00-\U0000FE0F\U00002190-\U000021FF]+")

TOPICS: List[Tuple[List[str], str, str, str]] = [
    # (keywords lowercase, category chip, Lao eyebrow, motif)
    (["crypto", "bitcoin", "btc", "eth", "etf", "blockchain", "token",
      "ຄຣິບໂຕ", "ບິດຄອຍ", "ຫຼຽນ"], "CRYPTO", "ຂ່າວ Crypto", "coin"),
    (["stock", "ຫຸ້ນ", "nasdaq", "s&p", "trading", "ຕະຫຼາດຫຼັກຊັບ"],
     "STOCKS", "ຂ່າວຫຸ້ນ", "chart"),
    (["ai", "claude", "gpt", "gemini", "llm", "agent", "model", "openai",
      "anthropic", "ປັນຍາປະດິດ"], "AI NEWS", "ຂ່າວດ່ວນ AI", "chip"),
]
DEFAULT_TOPIC = ("TECH", "ຂ່າວເຕັກໂນໂລຊີ", "chip")

_STAT_RE = re.compile(
    r"\$\s?\d[\d,.]*\s?[kKmMbB]?|\d[\d,.]*\s?%|\d[\d,.]*[kKmMbB]\b")
_DATE_RE = re.compile(r"ວັນທີ\s?\d{1,2}\s\S+\s?\d{4}|\d{4}-\d{2}-\d{2}")


def _strip_emoji(s: str) -> str:
    return _EMOJI_RE.sub("", s).strip(" -—•:")


def _copy_block(text: str) -> str:
    lines = text.splitlines()
    s = e = None
    for i, ln in enumerate(lines):
        low = ln.lower()
        if s is None and "copy from here" in low:
            s = i + 1
        elif s is not None and "copy to here" in low:
            e = i
            break
    return "\n".join(lines[s:e]) if s is not None and e else text


def analyze(source: str) -> Dict:
    """Auto-examine a post file or raw text -> design content dict."""
    title = ""
    if os.path.isfile(source):
        raw = Path(source).read_text(encoding="utf-8")
        m = re.search(r"^#\s+(.+)$", raw, re.M)
        title = m.group(1).strip() if m else ""
        body = _copy_block(raw)
    else:
        body = source
    body, _ = normalize_lao(body, Options())
    title, _ = normalize_lao(title, Options()) if title else (title, None)

    lines = [ln.strip() for ln in body.splitlines() if ln.strip()]
    hook = _strip_emoji(lines[0]) if lines else ""

    # topic -> category / eyebrow / motif
    low = body.lower() + " " + title.lower()
    category, eyebrow, motif = DEFAULT_TOPIC
    best = 0
    for kws, cat, eb, mo in TOPICS:
        score = sum(low.count(k) for k in kws)
        if score > best:
            best, category, eyebrow, motif = score, cat, eb, mo

    # headline: prefer the md title; split on em-dash / colon
    src_head = title or hook
    src_head = _strip_emoji(src_head)
    parts = re.split(r"\s+[—–]\s+|:\s+", src_head, maxsplit=1)
    headline = [p.strip() for p in parts if p.strip()][:2]

    # subhead: don't repeat the headline — use the text after the headline
    # part of the hook, or the second line of the body
    subhead = hook
    if not title:  # headline was derived from the hook itself
        rest = hook
        for p in headline:
            rest = rest.replace(p, "", 1)
        subhead = rest.strip(" —–:!?") or (
            _strip_emoji(lines[1]) if len(lines) > 1 else "")

    # stat: first money/percent figure NOT already shown in the headline,
    # labelled with the short clause around it
    stat = None
    # line 2 of the headline is often truncated at render time, so only the
    # first (always fully visible) line counts as "already shown"
    head_txt = headline[0] if headline else ""
    search_lines = lines[1:] if len(lines) > 1 else lines
    for ln in search_lines:
        for m in _STAT_RE.finditer(ln):
            val = m.group(0).replace(" ", "")
            if val in head_txt and len(lines) == 1:
                continue  # raw text: don't repeat the headline figure
            after = _strip_emoji(ln[m.end():])
            before = _strip_emoji(ln[:m.start()])
            label = after if len(after) >= 6 else before
            label = re.split(r"[(—–]", label)[0]
            label = re.sub(r"\s+", " ", label).strip(" :,-•")
            if not label:
                label = re.split(r"[(—–]", before)[0].strip(" :,-•")
            stat = {"value": val, "label": label[:60]}
            break
        if stat:
            break

    pros, cons = [], []
    for ln in lines:
        s = _strip_emoji(ln)
        if s.startswith(("ຂໍ້ດີ", "ຂໍ້ເສຍ")):
            continue  # section header lines, not items
        if ln.startswith("✅") and len(s) > 12:
            pros.append(s)
        elif ln.startswith("❌") and len(s) > 12:
            cons.append(s)

    chips: List[str] = []
    for ln in lines:
        if ln.startswith("#arnfar"):
            chips = [t.lstrip("#") for t in ln.split()
                     if t.startswith("#") and t.lower() != "#arnfar"][:3]
            break

    dm = _DATE_RE.search(body)
    return {
        "headline": headline or ["Arnfar"],
        "subhead": subhead[:80],
        "category": category,
        "eyebrow": eyebrow,
        "motif": motif,
        "stat": stat,
        "pros": pros[:3],
        "cons": cons[:3],
        "chips": chips,
        "date": dm.group(0) if dm else "",
        "tags": DEFAULT_TAGS,
        "seed": int(hashlib.sha1(src_head.encode()).hexdigest()[:8], 16),
    }


# ----------------------------------------------------------------------------
# 2. DESIGN (SVG)
# ----------------------------------------------------------------------------

_LAO_MARKS = set("ຼຸູັິີຶືົໍ່້໊໋ຳ")


def est_w(s: str, size: float) -> float:
    """Approximate rendered width: combining marks ~0, Lao ~0.62em, Latin ~0.52em."""
    w = 0.0
    for c in s:
        if c in _LAO_MARKS:
            w += 0.04
        elif "຀" <= c <= "໿":
            w += 0.62
        elif c in "iIl.,:;'| ":
            w += 0.30
        else:
            w += 0.54
    return w * size


def fit_size(s: str, max_w: float, start: float, lo: float = 24) -> float:
    size = start
    while size > lo and est_w(s, size) > max_w:
        size -= 2
    return size


def truncate(s: str, size: float, max_w: float) -> str:
    if est_w(s, size) <= max_w:
        return s
    while s and est_w(s + "…", size) > max_w:
        s = s[:-1]
    return s.rstrip() + "…"


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def _motif_svg(motif: str, W: int, H: int) -> str:
    """Faint large topic motif behind the right side of the canvas."""
    cx, cy, s = W * 0.80, H * 0.34, min(W, H) * 0.26
    g = [f'<g opacity="0.10" stroke="url(#brand)" fill="none" stroke-width="6">']
    if motif == "coin":
        g.append(f'<circle cx="{cx}" cy="{cy}" r="{s}"/>')
        g.append(f'<circle cx="{cx}" cy="{cy}" r="{s*0.72}"/>')
        g.append(f'<path d="M {cx-s*0.22} {cy-s*0.34} v {s*0.68} '
                 f'M {cx+s*0.02} {cy-s*0.34} v {s*0.68} '
                 f'M {cx-s*0.32} {cy-s*0.18} h {s*0.5} a {s*0.16} {s*0.16} 0 0 1 0 {s*0.32} '
                 f'h -{s*0.5} M {cx-s*0.32} {cy+s*0.14} h {s*0.56} '
                 f'a {s*0.16} {s*0.16} 0 0 1 0 {s*0.32} h -{s*0.56}"/>')
    elif motif == "chart":
        x0, y0 = cx - s, cy + s * 0.8
        g.append(f'<path d="M {x0} {y0} h {2*s} M {x0} {y0} v {-1.6*s}"/>')
        pts = [(0.15, 0.35), (0.45, 0.75), (0.75, 0.45), (1.05, 1.05),
               (1.35, 0.85), (1.7, 1.35)]
        pl = " ".join(f"{x0+px*s:.0f},{y0-py*s:.0f}" for px, py in pts)
        g.append(f'<polyline points="{pl}" stroke-width="8"/>')
        for px, py in pts:
            g.append(f'<circle cx="{x0+px*s:.0f}" cy="{y0-py*s:.0f}" r="10" '
                     f'fill="url(#brand)" stroke="none"/>')
    else:  # chip
        r = s * 0.9
        g.append(f'<rect x="{cx-r/2}" y="{cy-r/2}" width="{r}" height="{r}" '
                 f'rx="{r*0.18}"/>')
        g.append(f'<rect x="{cx-r*0.28}" y="{cy-r*0.28}" width="{r*0.56}" '
                 f'height="{r*0.56}" rx="{r*0.1}"/>')
        for i in range(4):
            off = -r * 0.3 + i * r * 0.2
            g.append(f'<path d="M {cx+off} {cy-r/2} v {-r*0.18} '
                     f'M {cx+off} {cy+r/2} v {r*0.18} '
                     f'M {cx-r/2} {cy+off} h {-r*0.18} '
                     f'M {cx+r/2} {cy+off} h {r*0.18}"/>')
    g.append("</g>")
    return "".join(g)


def svg_background(W: int, H: int, seed: int = 1, motif: str = "chip",
                   as_group: bool = True) -> str:
    """Arnfar vector backdrop: navy gradient, faint grid, brand orbs,
    starfield, topic motif. Returns a <g id="bg"> group (or full SVG)."""
    rng = random.Random(seed)
    p: List[str] = [f'<g id="bg"><rect width="{W}" height="{H}" fill="url(#bgv)"/>']
    p.append(f'<rect width="{W}" height="{H}" fill="url(#gridp)"/>')
    # orbs
    p.append(f'<circle cx="{W*0.14:.0f}" cy="{H*0.10:.0f}" r="{W*0.42:.0f}" '
             f'fill="url(#orbB)"/>')
    p.append(f'<circle cx="{W*0.88:.0f}" cy="{H*0.86:.0f}" r="{W*0.40:.0f}" '
             f'fill="url(#orbG)"/>')
    p.append(f'<circle cx="{W*0.82:.0f}" cy="{H*0.24:.0f}" r="{W*0.30:.0f}" '
             f'fill="url(#orbG)" opacity="0.55"/>')
    p.append(_motif_svg(motif, W, H))
    # starfield + sparkles
    for _ in range(70):
        x, y = rng.uniform(0, W), rng.uniform(0, H)
        r = rng.uniform(1, 2.6)
        o = rng.uniform(0.08, 0.4)
        p.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" '
                 f'fill="#FFFFFF" opacity="{o:.2f}"/>')
    for _ in range(6):
        x, y = rng.uniform(W * 0.1, W * 0.9), rng.uniform(H * 0.1, H * 0.9)
        s = rng.uniform(8, 20)
        col = BLUE if rng.random() < 0.5 else GREEN
        p.append(f'<path d="M {x:.0f} {y-s:.0f} L {x+s*0.22:.0f} {y-s*0.22:.0f} '
                 f'L {x+s:.0f} {y:.0f} L {x+s*0.22:.0f} {y+s*0.22:.0f} '
                 f'L {x:.0f} {y+s:.0f} L {x-s*0.22:.0f} {y+s*0.22:.0f} '
                 f'L {x-s:.0f} {y:.0f} L {x-s*0.22:.0f} {y-s*0.22:.0f} Z" '
                 f'fill="{col}" opacity="{rng.uniform(0.25, 0.7):.2f}"/>')
    p.append("</g>")
    group = "".join(p)
    if as_group:
        return group
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
            f'viewBox="0 0 {W} {H}">{_defs(W, H)}{group}</svg>')


def _defs(W: int, H: int) -> str:
    return f"""<defs>
<linearGradient id="bgv" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="{BG0}"/><stop offset="1" stop-color="{BG1}"/>
</linearGradient>
<linearGradient id="brand" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="{BLUE}"/><stop offset="1" stop-color="{GREEN}"/>
</linearGradient>
<radialGradient id="orbB"><stop offset="0" stop-color="{BLUE}" stop-opacity="0.55"/>
  <stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></radialGradient>
<radialGradient id="orbG"><stop offset="0" stop-color="{GREEN}" stop-opacity="0.50"/>
  <stop offset="1" stop-color="{GREEN}" stop-opacity="0"/></radialGradient>
<radialGradient id="sheen" cx="0.18" cy="0.02" r="1.1">
  <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.20"/>
  <stop offset="0.45" stop-color="#FFFFFF" stop-opacity="0.05"/>
  <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></radialGradient>
<linearGradient id="innersh" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0.82" stop-color="#020610" stop-opacity="0"/>
  <stop offset="1" stop-color="#020610" stop-opacity="0.35"/></linearGradient>
<linearGradient id="rim" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.65"/>
  <stop offset="0.5" stop-color="#FFFFFF" stop-opacity="0.14"/>
  <stop offset="1" stop-color="#FFFFFF" stop-opacity="0.30"/></linearGradient>
<pattern id="gridp" width="60" height="60" patternUnits="userSpaceOnUse">
  <path d="M 60 0 H 0 V 60" fill="none" stroke="#FFFFFF" stroke-opacity="0.03"/>
</pattern>
<filter id="frost" x="-20%" y="-20%" width="140%" height="140%">
  <feGaussianBlur stdDeviation="16"/>
  <feColorMatrix type="saturate" values="1.5"/>
</filter>
<filter id="dropsh" x="-30%" y="-30%" width="160%" height="160%">
  <feGaussianBlur stdDeviation="14"/>
</filter>
</defs>"""


_CLIP_N = 0


def glass_panel(x: float, y: float, w: float, h: float, r: float = 22) -> str:
    """Vector liquid-glass panel: drop shadow, clipped+scaled blurred copy of
    the bg (backdrop blur + edge 'lensing' via 4% zoom), dark overlay, sheen,
    inner shadow, rim and brand hairline."""
    global _CLIP_N
    _CLIP_N += 1
    cid = f"cp{_CLIP_N}"
    cx, cy = x + w / 2, y + h / 2
    return f"""<rect x="{x}" y="{y+8}" width="{w}" height="{h}" rx="{r}"
  fill="#000000" opacity="0.45" filter="url(#dropsh)"/>
<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}"/></clipPath>
<g clip-path="url(#{cid})">
  <g transform="translate({cx} {cy}) scale(1.04) translate({-cx} {-cy})">
    <use href="#bg" filter="url(#frost)"/>
  </g>
  <rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#0A1020" opacity="0.52"/>
  <rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#sheen)"/>
  <rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#innersh)"/>
</g>
<rect x="{x+1}" y="{y+1}" width="{w-2}" height="{h-2}" rx="{r-1}"
  fill="none" stroke="url(#rim)" stroke-width="1.4"/>
<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}"
  fill="none" stroke="url(#brand)" stroke-opacity="0.35" stroke-width="1"/>"""


def _text(x: float, y: float, s: str, size: float, fill: str = INK,
          anchor: str = "start", opacity: float = 1.0) -> str:
    return (f'<text x="{x:.0f}" y="{y:.0f}" font-family="{FONT_FAMILY}" '
            f'font-size="{size:.0f}" fill="{fill}" text-anchor="{anchor}" '
            f'opacity="{opacity}">{esc(s)}</text>')


def _mark(x: float, y: float, ok: bool, s: float = 13) -> str:
    """Vector ✓ / ✕ marks (emoji glyphs don't rasterize reliably)."""
    if ok:
        return (f'<circle cx="{x}" cy="{y}" r="{s+6}" fill="{GREEN}" opacity="0.16"/>'
                f'<path d="M {x-s*0.55} {y} l {s*0.4} {s*0.45} l {s*0.75} {-s*0.95}" '
                f'stroke="{GREEN}" stroke-width="4" fill="none" stroke-linecap="round"/>')
    return (f'<circle cx="{x}" cy="{y}" r="{s+6}" fill="#F0506E" opacity="0.16"/>'
            f'<path d="M {x-s*0.5} {y-s*0.5} l {s} {s} M {x+s*0.5} {y-s*0.5} l {-s} {s}" '
            f'stroke="#F0506E" stroke-width="4" fill="none" stroke-linecap="round"/>')


def _logo_b64() -> str:
    if LOGO_PNG.is_file():
        return base64.b64encode(LOGO_PNG.read_bytes()).decode()
    return ""


def svg_poster(info: Dict, size: str = "portrait") -> str:
    global _CLIP_N
    _CLIP_N = 0
    W, H = SIZES.get(size, SIZES["portrait"])
    M = round(W * 0.078)
    colw = W - 2 * M
    out: List[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        _defs(W, H),
        svg_background(W, H, info.get("seed", 1), info.get("motif", "chip")),
    ]

    # ---- top bar: logo + wordmark left, category glass pill right ----
    logo = _logo_b64()
    if logo:
        out.append(f'<image x="{M}" y="66" width="72" height="72" '
                   f'href="data:image/png;base64,{logo}"/>')
        out.append(_text(M + 92, 116, "Arnfar", 44))
    else:
        out.append(_text(M, 116, "Arnfar", 44))
    cat = info["category"]
    pw = est_w(cat, 30) + 56
    out.append(glass_panel(W - M - pw, 70, pw, 60, 30))
    out.append(_text(W - M - pw / 2, 110, cat, 30, INK, "middle"))

    # ---- eyebrow ----
    y = int(H * 0.155)
    out.append(_text(M, y, info["eyebrow"], 30, EYEBROW))
    y += 26

    # ---- headline (<=2 lines; shrink to 44px, then truncate) ----
    hls = info["headline"]
    hsize = max(44.0, min(fit_size(ln, colw, 84, lo=44) for ln in hls))
    for ln in hls:
        y += int(hsize * 1.22)
        out.append(_text(M, y, truncate(ln, hsize, colw), hsize))
    y += 26
    uw = min(est_w(hls[-1], hsize) * 0.6, 420)
    out.append(f'<rect x="{M}" y="{y}" width="{uw:.0f}" height="12" rx="6" '
               f'fill="url(#brand)"/>')
    y += 54

    # ---- subhead ----
    if info["subhead"]:
        sub = truncate(info["subhead"], 36, colw)
        out.append(_text(M, y + 20, sub, 36, MUTE))
        y += 66

    # ---- stat hero ----
    if info.get("stat"):
        st = info["stat"]
        vsize = 88.0
        vw = est_w(st["value"], vsize)
        out.append(f'<text x="{M}" y="{y+76}" font-family="{FONT_FAMILY}" '
                   f'font-size="{vsize:.0f}" fill="url(#brand)">'
                   f'{esc(st["value"])}</text>')
        if st.get("label"):
            lbl = truncate(st["label"], 30, colw - vw - 30)
            out.append(_text(M + vw + 28, y + 68, lbl, 30, MUTE))
        y += 118

    # ---- pros / cons glass panels ----
    footer_top = H - 140
    chips_h = 96 if info["chips"] else 0
    row_h = 62
    pros, cons = info["pros"], info["cons"]
    # fit both panels into the remaining budget: shed rows before panels
    avail = footer_top - chips_h - 20 - y
    def _need(a: List[str], b: List[str]) -> int:
        return sum(84 + row_h * len(x) + 26 for x in (a, b) if x)
    while _need(pros, cons) > avail and (len(pros) > 2 or len(cons) > 2):
        if len(pros) >= len(cons):
            pros = pros[:-1]
        else:
            cons = cons[:-1]
    for items, head, ok in ((pros, "ຂໍ້ດີ", True),
                            (cons, "ຂໍ້ຄວນລະວັງ", False)):
        if not items:
            continue
        ph = 84 + row_h * len(items)
        if y + ph > footer_top - chips_h - 20:
            break
        out.append(glass_panel(M, y, colw, ph, 24))
        out.append(_text(M + 34, y + 52, head, 32,
                         GREEN if ok else "#F0506E"))
        ry = y + 84 + row_h // 2
        for it in items:
            out.append(_mark(M + 44, ry - 10, ok))
            out.append(_text(M + 84, ry, truncate(it, 29, colw - 118), 29))
            ry += row_h
        y += ph + 26

    # ---- chips ----
    if info["chips"] and y + 70 <= footer_top - 10:
        cx = M
        for c in info["chips"]:
            cw = est_w(c, 28) + 64
            if cx + cw > W - M:
                break
            out.append(glass_panel(cx, y, cw, 60, 18))
            out.append(f'<rect x="{cx+16}" y="{y+16}" width="8" height="28" '
                       f'rx="4" fill="url(#brand)"/>')
            out.append(_text(cx + 38, y + 40, c, 28))
            cx += cw + 18
        y += 88

    # ---- footer ----
    out.append(f'<rect x="{M}" y="{H-118}" width="{colw}" height="6" rx="3" '
               f'fill="url(#brand)"/>')
    out.append(_text(W / 2, H - 62, info["tags"], 36, INK, "middle"))
    if info.get("date"):
        out.append(_text(W - M, H - 132, info["date"], 26, MUTE, "end"))
    out.append("</svg>")
    return "\n".join(out)


# ----------------------------------------------------------------------------
# 3. EXPORT
# ----------------------------------------------------------------------------

def to_png(svg: str, out_path: Path, W: int, H: int) -> bool:
    font_dir = str(REPO / "font")
    try:  # 1) resvg_py python module
        import resvg_py
        png = resvg_py.svg_to_bytes(svg_string=svg, width=W, height=H,
                                    font_dirs=[font_dir],
                                    font_family=FONT_FAMILY)
        out_path.write_bytes(bytes(png))
        return True
    except ImportError:
        pass
    plat = {"Darwin": "macos", "Linux": "linux"}.get(platform.system(), "")
    arch = {"arm64": "aarch64", "aarch64": "aarch64",
            "x86_64": "x86_64"}.get(platform.machine(), "")
    cand = TOOLS_DIR / "bin" / f"resvg-{plat}-{arch}"
    svg_tmp = out_path.with_suffix(".svg.tmp")
    svg_tmp.write_text(svg, encoding="utf-8")
    try:
        for cmd in ([str(cand), "--use-fonts-dir", font_dir,
                     "--width", str(W), "--height", str(H),
                     str(svg_tmp), str(out_path)] if cand.is_file() else None,
                    ["rsvg-convert", "-w", str(W), "-h", str(H),
                     "-o", str(out_path), str(svg_tmp)]):
            if cmd is None:
                continue
            try:
                if subprocess.run(cmd, capture_output=True).returncode == 0:
                    return True
            except FileNotFoundError:
                continue
    finally:
        svg_tmp.unlink(missing_ok=True)
    return False


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Auto-examine post content -> Arnfar poster PNG (SVG optional).")
    ap.add_argument("source", help="post .md path or raw text")
    ap.add_argument("--size", default="portrait", choices=list(SIZES))
    ap.add_argument("--outdir", default=str(REPO / "output" / "vector"))
    ap.add_argument("--prefix", default=None)
    ap.add_argument("--bg-only", action="store_true",
                    help="emit only the background (also saves its .svg, "
                         "since that's the point of this mode)")
    ap.add_argument("--no-png", action="store_true", help="skip PNG export")
    ap.add_argument("--svg", action="store_true",
                    help="also save the .svg poster (default: PNG only)")
    args = ap.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    info = analyze(args.source)
    W, H = SIZES[args.size]

    if args.prefix:
        stem = args.prefix
    elif os.path.isfile(args.source):
        stem = Path(args.source).stem
    else:
        stem = "arnfar-poster"
    stem += "-bg" if args.bg_only else ""

    if args.bg_only:
        svg = svg_background(W, H, info["seed"], info["motif"], as_group=False)
    else:
        svg = svg_poster(info, args.size)

    svg_path = outdir / f"{stem}.svg"
    keep_svg = args.svg or args.no_png or args.bg_only
    if keep_svg:
        svg_path.write_text(svg, encoding="utf-8")
        print("saved", svg_path)
    if not args.no_png:
        png_path = outdir / f"{stem}.png"
        if to_png(svg, png_path, W, H):
            print("saved", png_path)
        elif keep_svg:
            print("PNG export skipped: install `pip install resvg-py` or "
                  "rsvg-convert (SVG was saved).", file=sys.stderr)
        else:
            # Neither export worked out -- fall back to saving the SVG so
            # the run doesn't come away with nothing.
            svg_path.write_text(svg, encoding="utf-8")
            print("PNG export skipped: install `pip install resvg-py` or "
                  "rsvg-convert. Saved", svg_path, "instead.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

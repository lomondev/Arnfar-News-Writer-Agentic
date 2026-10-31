#!/usr/bin/env python3
"""Arnfar 9:16 reel cover (thumbnail) from a story.json.

Usage:
  python3 make_cover.py <story_dir>/story.json out/arnfar-<slug>-cover.jpg

story.json may carry an optional "cover" block; anything missing falls back to
the hook scene (title, photo, credit) and the first stat scene (big number):

  "cover": {
    "photo": "photo1.jpg",            # full-bleed background
    "kicker": "ຂ່າວດ່ວນ",              # small pill above the headline (default: story tag)
    "title": ["ເອລນີໂຍ ແຮງສຸດ", "ໂລກຮ້ອນຂຶ້ນ"],   # line 2 is drawn in the accent colour
    "big": "+3.7°C",                  # sticker number (optional)
    "big_label": "ນ້ຳທະເລຄາດທ້າຍປີ",   # caption under the number
    "focus": "50% 40%",               # CSS object-position for the photo
    "credit": "ຮູບ: NASA"
  }

Layout keeps every word inside the zone that survives the IG 3:4 grid crop and
the TikTok right-rail/bottom caption overlay (x 70-930, y 250-1500); header pill + badge at top 260 (inside the 3:4 profile-grid crop y 240-1680).
"""
from __future__ import annotations

import base64
import html
import json
import mimetypes
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
FONTS = HERE / "fonts"


def data_uri(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode()}"


def pick(story: dict) -> dict:
    scenes = story.get("scenes", [])
    hook = next((s for s in scenes if s.get("type") == "hook"), {})
    stat = next((s for s in scenes if s.get("type") == "stat"), {})
    cv = dict(story.get("cover", {}))
    cv.setdefault("photo", hook.get("photo") or next((s["photo"] for s in scenes if s.get("photo")), None))
    cv.setdefault("title", hook.get("title") or [story.get("tag", "Arnfar")])
    cv.setdefault("kicker", story.get("tag", ""))
    cv.setdefault("credit", hook.get("credit", ""))
    if "big" not in cv and stat.get("value"):
        cv["big"] = stat["value"]
        cv.setdefault("big_label", stat.get("label", ""))
    cv.setdefault("focus", "50% 40%")
    if isinstance(cv["title"], str):
        cv["title"] = [cv["title"]]
    return cv


def fit_size(text: str, base: int, max_chars: int) -> int:
    n = len(text)
    return base if n <= max_chars else max(78, int(base * max_chars / n))


def build_html(story: dict, cv: dict, root: Path) -> str:
    warn = story.get("accent") == "warn"
    acc = "linear-gradient(90deg,#ffd23a,#ff7a1a)" if warn else "linear-gradient(90deg,#29b6ff,#2ee59d)"
    pill = "linear-gradient(90deg,#d8342c,#f29a1a)" if warn else "linear-gradient(90deg,#0394F1,#15C67A)"
    glow = "rgba(255,110,30,.55)" if warn else "rgba(21,198,122,.5)"
    photo = data_uri(root / cv["photo"]) if cv.get("photo") else ""
    logo_path = root / story.get("logo", "arnfar-logo.png")
    logo = data_uri(logo_path) if logo_path.exists() else ""
    lines = cv["title"][:2]
    l1 = lines[0]
    l2 = lines[1] if len(lines) > 1 else ""
    s1 = fit_size(l1, 132, 13)
    s2 = fit_size(l2, 150, 11) if l2 else 0
    e = html.escape
    big = ""
    if cv.get("big"):
        big = f"""<div class="big"><div class="num">{e(cv['big'])}</div>{f'<div class="bl">{e(cv.get("big_label", ""))}</div>' if cv.get('big_label') else ''}</div>"""
    return f"""<!doctype html><html lang="lo"><head><meta charset="utf-8"><style>
@font-face{{font-family:LaoBlack;src:url("{data_uri(FONTS / 'NotoSansLao-Black.woff2')}") format("woff2");}}
@font-face{{font-family:LatBlack;src:url("{data_uri(FONTS / 'NotoSans-Black.woff2')}") format("woff2");}}
@font-face{{font-family:LaoReg;src:url("{data_uri(FONTS / 'Phetsarath-Regular.ttf')}") format("truetype");}}
html,body{{margin:0;background:#050c1d}}
*{{box-sizing:border-box}}
#c{{width:1080px;height:1920px;position:relative;overflow:hidden;color:#fff;font-family:LatBlack,LaoBlack,sans-serif;background:#050c1d}}
#c>img.bg{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:{cv['focus']};filter:saturate(1.25) contrast(1.08)}}
.shade{{position:absolute;inset:0;background:
  linear-gradient(180deg,rgba(5,12,29,.55) 0%,rgba(5,12,29,0) 22%,rgba(5,12,29,0) 40%,rgba(5,12,29,.82) 62%,rgba(5,12,29,.96) 100%)}}
.vign{{position:absolute;inset:0;box-shadow:inset 0 0 260px rgba(0,0,0,.65)}}
.top{{position:absolute;left:60px;right:60px;top:260px;display:flex;justify-content:space-between;align-items:center}}
.brand{{display:flex;align-items:center;gap:14px;padding:10px 28px 10px 10px;border-radius:999px;background:rgba(5,12,29,.55);border:1px solid rgba(255,255,255,.25);font-size:40px}}
.brand img{{width:64px;height:64px;border-radius:50%;background:#fff}}
.kick{{padding:14px 32px;border-radius:999px;background:{pill};font-family:LaoReg,sans-serif;font-size:36px;box-shadow:0 10px 40px rgba(0,0,0,.35)}}
.big{{position:absolute;right:150px;top:600px;transform:rotate(-5deg);padding:26px 40px 22px;border-radius:34px;
  background:rgba(5,12,29,.72);border:3px solid rgba(255,255,255,.85);box-shadow:0 0 90px {glow},0 24px 60px rgba(0,0,0,.5);text-align:center}}
.big .num{{font-size:150px;line-height:1;background:{acc};-webkit-background-clip:text;background-clip:text;color:transparent}}
.big .bl{{font-family:LaoReg,sans-serif;font-size:34px;margin-top:10px;color:#e6eef8}}
.head{{position:absolute;left:70px;right:150px;top:1010px;display:flex;flex-direction:column;gap:6px}}
.l1{{font-size:{s1}px;line-height:1.28;white-space:nowrap;text-shadow:0 6px 0 rgba(0,0,0,.35),0 0 40px rgba(0,0,0,.6)}}
.l2{{font-size:{s2}px;line-height:1.28;white-space:nowrap;background:{acc};-webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 6px 0 rgba(0,0,0,.4)) drop-shadow(0 0 30px rgba(0,0,0,.5))}}
.bar{{width:260px;height:14px;border-radius:7px;background:{acc};margin-top:26px}}
.credit{{position:absolute;left:70px;top:1456px;font-family:LaoReg,sans-serif;font-size:24px;color:#b9cbe0}}
</style></head><body><div id="c">
{f'<img class="bg" src="{photo}">' if photo else ''}
<div class="shade"></div><div class="vign"></div>
<div class="top">{f'<div class="kick">{e(cv["kicker"])}</div>' if cv.get('kicker') else '<div></div>'}<div class="brand">{f'<img src="{logo}">' if logo else ''}<div>Arnfar</div></div></div>
{big}
<div class="head"><div class="l1">{e(l1)}</div>{f'<div class="l2">{e(l2)}</div>' if l2 else ''}<div class="bar"></div></div>
{f'<div class="credit">{e(cv["credit"])}</div>' if cv.get('credit') else ''}
</div></body></html>"""


def main() -> None:
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    story_path = Path(sys.argv[1]).resolve()
    out = Path(sys.argv[2]).resolve()
    story = json.loads(story_path.read_text(encoding="utf-8"))
    cv = pick(story)
    page_html = build_html(story, cv, story_path.parent)
    out.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--force-color-profile=srgb"])
        pg = b.new_page(viewport={"width": 1080, "height": 1920})
        pg.set_content(page_html, wait_until="load")
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(300)
        # keep each headline line on one row: shrink until it fits the column (Lao must never break mid-word)
        pg.evaluate("""() => { document.querySelectorAll('.l1,.l2').forEach(e => {
            const w = e.parentElement.clientWidth; let fs = parseFloat(getComputedStyle(e).fontSize);
            while (e.scrollWidth > w + 1 && fs > 60) { fs -= 4; e.style.fontSize = fs + 'px'; } }); }""")
        overflow = pg.evaluate("""() => { const h = document.querySelector('.head').getBoundingClientRect();
            const b = document.querySelector('.big'); const r = b ? b.getBoundingClientRect() : null;
            return {head_bottom: h.bottom, head_right: h.right, big_bottom: r ? r.bottom : 0, head_top: h.top}; }""")
        pg.locator("#c").screenshot(path=str(out), type="jpeg", quality=92)
        b.close()
    if overflow["head_bottom"] > 1490 or (overflow["big_bottom"] and overflow["big_bottom"] > overflow["head_top"]):
        print(f"WARN layout: {overflow} - shorten title/big_label", file=sys.stderr)
    print(out)


if __name__ == "__main__":
    main()

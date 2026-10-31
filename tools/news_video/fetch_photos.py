#!/usr/bin/env python3
"""Find and download free-licence photos from Wikimedia Commons for Arnfar videos.

Usage:
  python3 fetch_photos.py "<search words>" -n 3 -o photos/ [--prefix drought] [--portrait]

For each hit it saves <prefix>-<k>.jpg (1920 px wide thumbnail, or 1600 px tall for
portrait images) and appends to <out>/credits.json:
  {"file": "drought-1.jpg", "credit": "ຮູບ: Tomas Castelazo / Wikimedia Commons (CC BY 3.0)",
   "title": "...", "page": "https://commons.wikimedia.org/wiki/File:...", "w": 2336, "h": 3504}

Only public-domain, CC0, CC BY and CC BY-SA files are kept. LOOK at every
downloaded file before using it: search hits can be off-topic.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://commons.wikimedia.org/w/api.php"
UA = "ArnfarNewsVideo/1.0 (https://arnfar.com; arnfars@gmail.com)"
OK_LICENSES = re.compile(r"^(public domain|pd|cc0|cc by(-sa)? [0-9.]+)", re.I)


def get(url: str, tries: int = 5) -> bytes:
    last: Exception | None = None
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=40) as r:
                return r.read()
        except Exception as e:  # 429 / transient network errors: back off and retry
            last = e
            time.sleep(5 * (k + 1) ** 2)  # 5, 20, 45, 80 s: Commons rate-limits bursts (HTTP 429)
    raise RuntimeError(f"download failed: {url}: {last}")


def strip_html(s: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", s or ""))).strip()


def search(query: str, limit: int) -> list[dict]:
    params = {
        "action": "query", "format": "json", "generator": "search",
        "gsrsearch": f"{query} filetype:bitmap", "gsrnamespace": "6", "gsrlimit": str(limit),
        "prop": "imageinfo", "iiprop": "url|size|extmetadata", "iiurlwidth": "1920",
    }
    data = json.loads(get(API + "?" + urllib.parse.urlencode(params)))
    pages = sorted(data.get("query", {}).get("pages", {}).values(), key=lambda p: p.get("index", 0))
    out = []
    for p in pages:
        ii = (p.get("imageinfo") or [{}])[0]
        meta = ii.get("extmetadata", {})
        lic = strip_html(meta.get("LicenseShortName", {}).get("value", ""))
        if not OK_LICENSES.match(lic):
            continue
        out.append({
            "title": p["title"].removeprefix("File:"),
            "page": ii.get("descriptionurl", ""),
            "w": ii.get("width", 0), "h": ii.get("height", 0),
            "thumb": ii.get("thumburl") or ii.get("url"),
            "artist": strip_html(meta.get("Artist", {}).get("value", "")) or "Unknown",
            "license": lic,
        })
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("-n", type=int, default=3)
    ap.add_argument("-o", "--out", default="photos")
    ap.add_argument("--prefix", default=None)
    ap.add_argument("--portrait", action="store_true", help="prefer portrait images (best for full-screen 9:16)")
    ap.add_argument("--min-width", type=int, default=1000)
    a = ap.parse_args()

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    prefix = a.prefix or re.sub(r"[^a-z0-9]+", "-", a.query.lower()).strip("-")[:24]
    hits = [h for h in search(a.query, max(12, a.n * 4)) if max(h["w"], h["h"]) >= a.min_width]
    if a.portrait:
        hits.sort(key=lambda h: h["w"] / max(h["h"], 1))
    if not hits:
        sys.exit(f"no free-licence hits for {a.query!r}")

    cred_path = out / "credits.json"
    credits = json.loads(cred_path.read_text(encoding="utf-8")) if cred_path.exists() else []
    saved = 0
    for h in hits:
        if saved >= a.n:
            break
        name = f"{prefix}-{saved + 1}.jpg"
        try:
            (out / name).write_bytes(get(h["thumb"]))
        except RuntimeError as e:
            print(e, file=sys.stderr)
            continue
        artist = h["artist"][:60]
        credits = [c for c in credits if c.get("file") != name]
        credits.append({
            "file": name,
            "credit": f"ຮູບ: {artist} / Wikimedia Commons ({h['license']})",
            "title": h["title"], "page": h["page"], "w": h["w"], "h": h["h"],
        })
        print(f"{name}  {h['w']}x{h['h']}  {h['license']}  {h['title'][:70]}")
        saved += 1
        time.sleep(1)
    cred_path.write_text(json.dumps(credits, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()

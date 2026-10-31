#!/usr/bin/env python3
"""Split an HQ master MP4 into 9.5 MB chunks for the Claude in Chrome file_upload bridge.

file_upload can send at most 10 MB per call (and per browser_batch). Paths must be inside the
session workspace (for example /home/claude/...). Paths under /mnt/user-data/outputs are
refused. The page rebuilds the file from the chunks, so the HQ master reaches Meta and TikTok
unchanged (sha256 checked in the page).

usage: hq_chunks.py <master.mp4>
Writes <master dir>/up-<stem>/c00..cNN and prints the sha256 plus the JS snippets to run.
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

CHUNK = 9_500_000


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    src = Path(sys.argv[1]).resolve()
    data = src.read_bytes()
    out = src.parent / f"up-{src.stem}"
    out.mkdir(exist_ok=True)
    for old in out.glob("c*"):
        old.unlink()
    n = 0
    for i in range(0, len(data), CHUNK):
        (out / f"c{n:02d}").write_bytes(data[i:i + CHUNK])
        n += 1
    sha = hashlib.sha256(data).hexdigest()
    name = src.stem.replace("-web", "") + ".mp4"
    print(f"{n} chunks in {out}  ({len(data)} bytes)  sha256 {sha}")
    print("1) stage input JS:")
    print("window.__ch=[];const i=document.createElement('input');i.type='file';i.id='arnfar_stage';"
          "i.setAttribute('aria-label','arnfar stage file input');i.style.cssText='position:fixed;left:-9999px';"
          "document.body.appendChild(i);i.addEventListener('change',()=>{if(i.files[0])window.__ch.push(i.files[0]);});'ok'")
    print(f"2) find 'arnfar stage file input', then one file_upload call per chunk: {out}/c00 ... c{n - 1:02d}")
    print("3) build + verify JS:")
    print("const ch=window.__ch.slice().sort((a,b)=>a.name.localeCompare(b.name));"
          f"window.__hq=new File(ch,'{name}',{{type:'video/mp4'}});"
          "const hx=[...new Uint8Array(await crypto.subtle.digest('SHA-256',await window.__hq.arrayBuffer()))]"
          ".map(b=>b.toString(16).padStart(2,'0')).join('');"
          f"'chunks='+ch.length+' size='+window.__hq.size+' match='+(hx==='{sha}')")
    print("4) give it to the site's real file input (captured with the click hook) JS:")
    print("const dt=new DataTransfer();dt.items.add(window.__hq);INPUT.files=dt.files;"
          "INPUT.dispatchEvent(new Event('input',{bubbles:true}));INPUT.dispatchEvent(new Event('change',{bubbles:true}));'set'")


if __name__ == "__main__":
    main()

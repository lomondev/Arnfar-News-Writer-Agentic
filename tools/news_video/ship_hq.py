#!/usr/bin/env python3
"""Prepare an HQ master MP4 for transfer to Lomon's Windows PC.

device_commit_files limits: 30 MB per file and 100 MB per call, and it alters a file that starts
with an MP4 header. So the master is split into 20 MiB parts. Part 000 gets a 16-byte
"ARNFARPART000000" prefix so it is not treated as video, and the PC strips that prefix again
when it joins the parts.

usage: ship_hq.py <master.mp4> <slug>
Writes /mnt/user-data/outputs/<slug>-hq/part000.bin ... plus manifest.json.
It then prints the commit batches (each 4 parts or fewer, under 100 MB) and the device_bash join
command, which also checks the md5.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

PART = 20 * 1024 * 1024
MAGIC = b"ARNFARPART000000"


def main() -> None:
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    src, slug = Path(sys.argv[1]).resolve(), sys.argv[2]
    data = src.read_bytes()
    md5 = hashlib.md5(data).hexdigest()
    out = Path("/mnt/user-data/outputs") / f"{slug}-hq"
    out.mkdir(parents=True, exist_ok=True)
    for old in out.glob("part*.bin"):
        old.unlink()
    parts = []
    for i in range(0, len(data), PART):
        chunk = data[i:i + PART]
        name = f"part{len(parts):03d}.bin"
        (out / name).write_bytes((MAGIC + chunk) if not parts else chunk)
        parts.append(name)
    dest_name = f"{src.stem}-HQ.mp4"
    manifest = {"source": str(src), "md5": md5, "bytes": len(data), "parts": parts, "dest_name": dest_name}
    (out / "manifest.json").write_text(json.dumps(manifest, indent=1), encoding="utf-8")
    pc_dir = f"~/mnt/Arnfar-News-Writer-Agentic/output/videos/{slug}"
    print(f"{len(parts)} parts, {len(data) / 1e6:.1f} MB, md5 {md5}")
    for b in range(0, len(parts), 4):
        batch = [{"stagedPath": str(out / p), "devicePath": f"{pc_dir}/parts/{p}"} for p in parts[b:b + 4]]
        print(f"commit batch {b // 4 + 1}: {json.dumps(batch, ensure_ascii=False)}")
    rest = " ".join(f"parts/{p}" for p in parts[1:])
    join = (f'cd "$HOME/mnt/Arnfar-News-Writer-Agentic/output/videos/{slug}" && '
            f'(tail -c +17 parts/{parts[0]}; cat {rest}) > {dest_name} && '
            f'echo "{md5}  {dest_name}" | md5sum -c - && ffprobe -v error -show_entries '
            f'stream=width,height,bit_rate:format=duration -of compact {dest_name}')
    print("device_bash join:", join)


if __name__ == "__main__":
    main()

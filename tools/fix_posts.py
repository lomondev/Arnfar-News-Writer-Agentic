#!/usr/bin/env python3
"""
fix_posts.py — auto-correct the Lao text inside Arnfar post files.

It normalizes ONLY the copy-paste body of a post (the lines between the
`copy from here` / `copy to here` markers) so the surrounding template prose,
hashtags and source URLs are never touched. Uses the rules in lao_fix.py.

Dictionary word correction is ON by default: it uses the bundled wordlist at
tools/data/lao_words.txt (~524k words merged from the tesseract lao.traineddata
training list, LaoNLP corpora incl. lao-eng-dictionary.csv, Google spellcheck,
and Lao Wiktionary). Pass --no-dict to disable it.

Usage:
    python3 tools/fix_posts.py commands/*.md            # fix in place
    python3 tools/fix_posts.py commands/*.md --check     # report only, exit 1 if changes
    python3 tools/fix_posts.py draft.md --whole          # normalize the whole file
    python3 tools/fix_posts.py draft.md --no-dict        # structural fixes only
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List, Optional, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lao_fix import Options, normalize_lao  # noqa: E402

START_HINT = "copy from here"
END_HINT = "copy to here"


def _find_block(lines: List[str]) -> Optional[Tuple[int, int]]:
    """Return (start, end) line indices exclusive of the marker lines, or None."""
    start = end = None
    for i, ln in enumerate(lines):
        low = ln.lower()
        if start is None and START_HINT in low:
            start = i + 1
        elif start is not None and END_HINT in low:
            end = i
            break
    if start is not None and end is not None and end > start:
        return start, end
    return None


def fix_text(text: str, whole: bool, use_dict: bool = True) -> Tuple[str, int]:
    """Return (new_text, total_changes)."""
    # safe defaults: am=compose, keep digits, no intra-space strip,
    # bundled dictionary correction on (tools/data/lao_words.txt)
    opts = Options(use_dict=use_dict)
    lines = text.splitlines(keepends=True)
    block = None if whole else _find_block(lines)

    if block is None:
        fixed, st = normalize_lao(text, opts)
        return fixed, _count(st)

    s, e = block
    body = "".join(lines[s:e])
    fixed_body, st = normalize_lao(body, opts)
    # normalize_lao strips trailing newline via line-join; restore block newline shape
    if body.endswith("\n") and not fixed_body.endswith("\n"):
        fixed_body += "\n"
    new = "".join(lines[:s]) + fixed_body + "".join(lines[e:])
    return new, _count(st)


def _count(st) -> int:
    return (st.junk_removed + st.orphans_dropped + st.clusters_reordered
            + st.dup_marks_dropped + st.am_composed + st.spaces_fixed
            + st.dict_corrections)


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(description="Auto-correct Lao text in post files.")
    p.add_argument("files", nargs="+", help="markdown post files")
    p.add_argument("--check", action="store_true",
                   help="report changes without writing; exit 1 if any")
    p.add_argument("--whole", action="store_true",
                   help="normalize the entire file, ignore copy markers")
    p.add_argument("--no-dict", action="store_true",
                   help="disable dictionary word correction")
    args = p.parse_args(argv)

    changed_files = 0
    for path_str in args.files:
        path = Path(path_str)
        if not path.is_file():
            print(f"skip (not a file): {path}", file=sys.stderr)
            continue
        original = path.read_text(encoding="utf-8")
        fixed, n = fix_text(original, args.whole, use_dict=not args.no_dict)
        if fixed == original:
            print(f"ok    {path}  (no changes)")
            continue
        changed_files += 1
        if args.check:
            print(f"WOULD-FIX {path}  ({n} corrections)")
        else:
            path.write_text(fixed, encoding="utf-8")
            print(f"fixed {path}  ({n} corrections)")

    if args.check and changed_files:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

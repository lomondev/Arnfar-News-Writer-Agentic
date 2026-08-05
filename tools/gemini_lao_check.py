#!/usr/bin/env python3
"""Second-opinion Lao proofreading pass, powered by the Gemini CLI.

Runs *after* tools/fix_posts.py: fix_posts.py handles mechanical Unicode /
dictionary normalization, this handles judgment — awkward or literal phrasing,
wrong word choice, slang, rare/literary words an ordinary reader would trip on,
and grammar/particle errors.

Usage (from the repo root):

    python3 tools/gemini_lao_check.py posts/2026-07-14-nvidia-1-trillion-selloff.md
    python3 tools/gemini_lao_check.py posts/foo.md --apply
    python3 tools/gemini_lao_check.py posts/*.md --strict
    python3 tools/gemini_lao_check.py posts/foo.md --raw        # dump model JSON

Requires the Gemini CLI on PATH:

    npm install -g @google/gemini-cli
    gemini            # once, to sign in

Exit codes: 0 = clean (or issues found without --strict), 1 = issues found with
--strict, 2 = hard error (no CLI, bad JSON, unreadable file).
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

DEFAULT_MODEL = "gemini-2.5-pro"
TIMEOUT_SEC = 180

START_MARKER = re.compile(r"^##\s*POST\s*\(copy from here", re.I)
END_MARKER = re.compile(r"^##\s*\(copy to here", re.I)

LAO_RE = re.compile(r"[຀-໿]")
THAI_RE = re.compile(r"[฀-๿]")
FENCE_RE = re.compile(r"^\s*```(?:json)?\s*|\s*```\s*$", re.S)

SEVERITY_ORDER = {"high": 0, "medium": 1, "low": 2}
SEVERITY_TAG = {"high": "HIGH  ", "medium": "MEDIUM", "low": "LOW   "}

PROMPT = """You are a native Lao (ພາສາລາວ) proofreader and copy editor reviewing a
Facebook post for the Arnfar brand before it is published.

House rules for the writing:
- Formal, standard Lao — no slang, chat-speak, or regional colloquialisms.
- But "formal" means the PLAIN, COMMON formal word, never a rare or literary
  one. A reader must never be stopped by an unfamiliar word.
- Tone: conversational, clear, professional. Not a dry wire report, not hype.
- Industry-standard English/proper nouns (AI, GPU, ETF, NVIDIA, Bloomberg,
  ticker symbols, numbers, %, USD) are ALLOWED inline and are NOT errors.
  Never flag them. Never flag emojis, hashtags, or markdown.
- Do not fact-check, restructure, shorten, or rewrite for style preference.
  Only report genuine language defects.

Report ONLY these defect classes:
1. awkward  — literal / translated-sounding phrasing a Lao writer would not use
2. wordchoice — a technically-correct word that is not what a native speaker reaches for here
3. slang    — casual, regional, or non-standard vocabulary
4. rare     — a formal word that is too rare or literary for an ordinary reader
5. grammar  — classifier, particle, connector, spacing, or tone-mark/spelling errors

For each defect, rewrite the WHOLE sentence or clause naturally — do not patch a
single word in place.

Return STRICT JSON ONLY. No prose, no markdown fences. Schema:

{"issues":[{"line":<int, the LNNN number of the line>,
            "original":"<exact substring copied verbatim from that line>",
            "suggestion":"<the corrected replacement for that exact substring>",
            "kind":"awkward|wordchoice|slang|rare|grammar",
            "severity":"high|medium|low",
            "reason":"<short reason, in English>"}]}

"original" MUST appear verbatim in the given line — copy it character for
character, including tone marks. If the post is clean, return {"issues":[]}.

Here is the post. Each line is prefixed with LNNN| — that prefix is NOT part of
the text; never include it in "original" or "suggestion".

"""


@dataclass(frozen=True)
class Issue:
    line: int
    original: str
    suggestion: str
    kind: str
    severity: str
    reason: str


def extract_body(lines: list[str]) -> tuple[int, int]:
    """Return [start, end) line indices of the post body between copy markers."""
    start = end = None
    for i, line in enumerate(lines):
        if start is None and START_MARKER.match(line):
            start = i + 1
        elif start is not None and END_MARKER.match(line):
            end = i
            break
    if start is None or end is None:
        return 0, len(lines)
    return start, end


def build_payload(lines: list[str], start: int, end: int) -> str:
    out: list[str] = []
    for i in range(start, end):
        if LAO_RE.search(lines[i]):
            out.append(f"L{i + 1:04d}| {lines[i]}")
    return "\n".join(out)


def run_gemini(prompt: str, payload: str, model: str) -> str:
    exe = shutil.which("gemini")
    if exe is None:
        sys.exit(
            "error: `gemini` not found on PATH.\n"
            "       npm install -g @google/gemini-cli   # then run `gemini` once to sign in"
        )
    try:
        proc = subprocess.run(
            [exe, "-m", model, "-p", prompt],
            input=payload,
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SEC,
        )
    except subprocess.TimeoutExpired:
        sys.exit(f"error: gemini timed out after {TIMEOUT_SEC}s")
    if proc.returncode != 0:
        sys.exit(f"error: gemini exited {proc.returncode}\n{proc.stderr.strip()}")
    return proc.stdout.strip()


def parse_issues(raw: str) -> list[Issue]:
    text = FENCE_RE.sub("", raw).strip()
    # The CLI sometimes prefixes a banner line; salvage the outermost JSON object.
    if not text.startswith("{"):
        lo, hi = text.find("{"), text.rfind("}")
        if lo == -1 or hi <= lo:
            sys.exit(f"error: no JSON in gemini output:\n{raw[:800]}")
        text = text[lo : hi + 1]
    try:
        data: Any = json.loads(text)
    except json.JSONDecodeError as exc:
        sys.exit(f"error: could not parse gemini JSON ({exc}):\n{text[:800]}")

    issues: list[Issue] = []
    for it in data.get("issues", []):
        try:
            issues.append(
                Issue(
                    line=int(it["line"]),
                    original=str(it["original"]),
                    suggestion=str(it["suggestion"]),
                    kind=str(it.get("kind", "?")),
                    severity=str(it.get("severity", "medium")).lower(),
                    reason=str(it.get("reason", "")),
                )
            )
        except (KeyError, TypeError, ValueError):
            continue  # skip malformed entries rather than dying on one bad row
    issues.sort(key=lambda i: (SEVERITY_ORDER.get(i.severity, 1), i.line))
    return issues


def check_thai(path: Path, lines: list[str]) -> None:
    for i, line in enumerate(lines, 1):
        for m in THAI_RE.finditer(line):
            ch = m.group()
            if not LAO_RE.match(ch):
                print(f"  !! {path}:{i} Thai-script character U+{ord(ch):04X} {ch!r}")


def apply_issues(path: Path, lines: list[str], issues: list[Issue]) -> int:
    applied = 0
    for iss in issues:
        idx = iss.line - 1
        if not (0 <= idx < len(lines)) or iss.original not in lines[idx]:
            print(f"  ~~ skipped L{iss.line}: original no longer matches")
            continue
        lines[idx] = lines[idx].replace(iss.original, iss.suggestion, 1)
        applied += 1
    if applied:
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return applied


def review(path: Path, model: str, apply: bool, raw_dump: bool) -> int:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"error: {path}: {exc}", file=sys.stderr)
        return 2

    lines = text.split("\n")
    start, end = extract_body(lines)
    payload = build_payload(lines, start, end)
    if not payload:
        print(f"ok    {path}  (no Lao text found)")
        return 0

    raw = run_gemini(PROMPT, payload, model)
    if raw_dump:
        print(raw)
        return 0

    issues = parse_issues(raw)
    check_thai(path, lines[start:end])

    if not issues:
        print(f"ok    {path}  (Gemini found no language issues)")
        return 0

    print(f"\n{path}  — {len(issues)} issue(s)\n")
    for iss in issues:
        tag = SEVERITY_TAG.get(iss.severity, "MEDIUM")
        print(f"  [{tag}] L{iss.line}  ({iss.kind}) {iss.reason}")
        print(f"      -  {iss.original}")
        print(f"      +  {iss.suggestion}\n")

    if apply:
        n = apply_issues(path, lines, issues)
        print(f"  applied {n}/{len(issues)} suggestion(s) to {path}")
        print("  → re-run: python3 tools/fix_posts.py " + str(path))
    else:
        print("  (dry run — pass --apply to write these in)")
    return 1


def main() -> None:
    ap = argparse.ArgumentParser(description="Gemini-powered Lao proofreading pass.")
    ap.add_argument("paths", nargs="+", type=Path, help="post .md file(s)")
    ap.add_argument("--model", default=DEFAULT_MODEL, help=f"default: {DEFAULT_MODEL}")
    ap.add_argument("--apply", action="store_true", help="write suggestions into the file")
    ap.add_argument("--raw", action="store_true", help="print the model's raw JSON and exit")
    ap.add_argument("--strict", action="store_true", help="exit 1 if any issue is found")
    args = ap.parse_args()

    found = False
    for path in args.paths:
        if review(path, args.model, args.apply, args.raw) == 1:
            found = True

    sys.exit(1 if (found and args.strict) else 0)


if __name__ == "__main__":
    main()

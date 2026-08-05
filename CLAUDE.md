# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This is primarily a **content/prompt repository** — reusable prompt templates
(a "swipe file") used to generate Lao-language social media content with
Claude. There's no build system, package manager, or test suite, but it is
**not zero application code**: `tools/` and `skills/*/scripts/` hold real,
executable Python that several workflows depend on (Lao text normalization,
card image rendering) — treat changes there as code changes, not prose edits.

## Repository layout

- `commands/` — reusable copy-paste prompt templates. Two kinds share this
  directory: `*-prompt.md` (swipe files — reuse as-is, only the bracketed
  input line changes) and `*-example.md` (finished reference posts kept for
  illustration — not templates, don't treat their body text as editable
  boilerplate).
- `posts/` — actual drafted/finished Lao Facebook posts (the output of using a
  template or a Skill), each with a Sources list; matching images live in
  `posts/images/`.
- `skills/` — Claude Code Skills that automate the workflow:
  `breaking-news-report/` (research → draft → card generation; includes
  `sources.md`, a curated list of official/specific sources for topic
  auto-discovery, and `scripts/arnfar_news_card.py`, the in-house PIL card
  renderer) and `poster-design/` (general poster/flyer generation). Also
  `lao-accounting-coa/` — not a Skill (no SKILL.md), just a reference dataset
  (multilingual Lao chart-of-accounts JSON) used by the accounting posts.
- `tools/` — Python scripts run from the repo root: `fix_posts.py` (Lao
  Unicode + dictionary-based correction; run on every post before publishing),
  `lao_fix.py` (the underlying correction engine, backed by
  `data/lao_words.txt`, a ~524k-word Lao dictionary), `auto_vector_poster.py`
  (zero-spec SVG/PNG poster generator), `liquid_glass.py`. A prebuilt `resvg`
  binary for SVG→PNG export lives in `tools/bin/`.
- `output/` — generated card images, JSON card specs, and SVGs produced by the
  tools/skills above.
- `preview/` — a small static HTML/CSS/JS app for browsing generated card
  specs in-browser. It loads spec JSON via `fetch()`, which fails silently
  under `file://` (CORS) — serve it locally first, e.g. `python3 -m
  http.server` from the repo root, then open `http://localhost:8000/preview/`.
- `font/` — brand font files (`Arnfar Font Regular.ttf` / `Bold.ttf`, plus Mac
  variants). **In `skills/breaking-news-report/`, every generated image uses
  Regular only, never Bold** — enforced via `ALL_REGULAR = True` in
  `scripts/arnfar_news_card.py` and by only registering Regular in
  `tools/auto_vector_poster.py`. Note: `skills/poster-design/SKILL.md`
  currently still documents mapping heavy weights → Bold — that's a real
  inconsistency between the two image paths, not an intentional exception;
  reconcile it with the user before assuming either behavior when touching
  poster-design.

## Working in this repository

- Most edits are Markdown prose and prompt instructions — there's nothing to
  build or lint. But `tools/*.py` and `skills/*/scripts/*.py` are real code;
  verify changes there by actually running the script, not just by reading it.
- This directory is **not a git repository**. If version control is needed, initialize one (`git init`) before committing.

## Prompt template conventions

The existing template (`commands/lao-facebook-post-prompt.md`) establishes conventions to preserve when editing it or authoring new templates:

- **Output language is Lao** (ພາສາລາວ). Prompts target a Lao-speaking Facebook audience and explain Technology, AI, Stock Trading, and Crypto in accessible terms. Industry-standard English terms (AI, Crypto, Blockchain, App) are allowed inline, but body text stays Lao.
- **Copy-paste boundaries.** The actual prompt lives between explicit `## PROMPT (copy from here ↓)` and `## (copy to here ↑)` markers. Only a single `[INSERT YOUR TOPIC HERE]` line is meant to change per use — keep the rest stable so the file works as a swipe file.
- **Fixed post structure** the generated post must follow, in order: Hook → Intro → The Action → Pros & Cons (✅/❌ bullets) → Summary & CTA → Hashtags.
- **Hashtags must start with `#arnfar`**, followed by 3–4 relevant hashtags. This branded-hashtag rule is a hard requirement across templates.
- **Every template's PROMPT block ends with a mandatory self-review pass** — before outputting, re-read the draft as a native Lao proofreader would and fix awkward/literal phrasing, wrong word choice, slang/non-standard words, rare/literary words an ordinary reader would trip on, and grammar/particle errors. This runs every time a template is used, in addition to (not instead of) the repo's mechanical `tools/fix_posts.py` normalization. Keep this instruction in place when editing or authoring templates.
- **Word choice is formal and standard Lao, but always easy to understand.** No slang, chat-speak, or regional colloquialisms — but "formal" means the plain, common formal word, never a rare or literary one. A reader should never be stopped by an unfamiliar word. Keep this rule in every template's Language Rules section.

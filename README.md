# Arnfar News Writer — Agentic

A content and automation repository for producing **Lao-language (ພາສາລາວ) social
media content** — Facebook/TikTok posts about Technology, AI, Stock Trading, and
Crypto — with Claude. It pairs reusable prompt templates (a "swipe file") with
real Python tooling for Lao text correction and branded card/poster rendering.

> This is primarily a prompt/content repo, but `tools/` and `skills/*/scripts/`
> contain executable Python that several workflows depend on. Treat changes there
> as code, not prose.

## What's inside

| Path | Purpose |
| --- | --- |
| `commands/` | Copy-paste prompt templates (`*-prompt.md`) and finished reference posts (`*-example.md`). |
| `posts/` | Drafted and finished Lao posts (46+), each with a Sources list; images in `posts/images/`. |
| `skills/` | Claude Skills that automate the workflow (see below). |
| `tools/` | Python: Lao text correction, poster/card generation, Facebook posting. |
| `output/` | Generated card images, JSON card specs, and SVGs. |
| `preview/` | Small static HTML app for browsing generated card specs in-browser. |
| `font/` | Brand font files (`Arnfar Font Regular/Bold.ttf`). |

## Skills

- **`breaking-news-report/`** — research → draft → card generation. Turns a
  breaking-news event into a ready-to-publish Lao post using a 7-beat
  storytelling flow, then renders branded cards via
  `scripts/arnfar_news_card.py`. Includes `sources.md`, a curated source list for
  topic auto-discovery.
- **`poster-design/`** — general poster/flyer/social-graphic generation.
- **`lao-accounting-coa/`** — reference dataset (multilingual Lao chart-of-accounts
  JSON) used by accounting posts. Not a Skill (no `SKILL.md`).

## Tools

| Script | What it does |
| --- | --- |
| `tools/fix_posts.py` | Lao Unicode + dictionary-based correction. **Run on every post before publishing.** |
| `tools/lao_fix.py` | The underlying correction engine, backed by a ~524k-word Lao dictionary. |
| `tools/auto_vector_poster.py` | Zero-spec SVG/PNG poster/background generator. |
| `tools/liquid_glass.py` | Liquid-glass visual effect helper. |
| `tools/fb_post.py` | Posts to the Arnfar Facebook Page via the Graph API (drafts by default). |
| `tools/gemini_lao_check.py` | Optional LLM-based Lao proofreading pass. |

A prebuilt `resvg` binary for SVG→PNG export lives in `tools/bin/`.

## Requirements

- Python 3.10+
- `pip install pillow numpy`

The Lao correction engine relies on `data/lao_words.txt`. Rendering uses the
`.ttf` files in `font/` — **the `breaking-news-report` image path uses Regular
only, never Bold** (enforced in code).

## Conventions

- **Output language is Lao.** Industry-standard English terms (AI, Crypto,
  Blockchain, App) are allowed inline; body text stays Lao.
- **Fixed post structure:** Hook → Intro → The Action → Pros & Cons (✅/❌) →
  Summary & CTA → Hashtags.
- **Hashtags must start with `#arnfar`**, followed by 3–4 relevant tags.
- **Word choice is formal, standard, and easy** — no slang, no rare/literary words.
- Every template ends with a mandatory native-proofreader self-review pass, in
  addition to the mechanical `tools/fix_posts.py` normalization.

## Preview app

`preview/` loads spec JSON via `fetch()`, which fails silently under `file://`
(CORS). Serve locally first:

```bash
python3 -m http.server   # from repo root
# then open http://localhost:8000/preview/
```

## Notes

- Secrets (`tools/.env`) are **not** committed — see `tools/.env.example` and
  `tools/FACEBOOK_SETUP.md` to configure Facebook posting.
- Large font source/export files (`.svg`, `.birdfont`, `.eot`) are gitignored
  because they exceed GitHub's 100MB limit; only the `.ttf` files needed by the
  pipeline are tracked.

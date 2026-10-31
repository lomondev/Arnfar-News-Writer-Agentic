# Arnfar News Writer — Agentic

Everything behind the **Arnfar** news page: researching a story, writing it as a
Lao-language (ພາສາລາວ) Facebook / Instagram / TikTok post with Claude, and turning
it into branded card images and 9:16 news videos.

Topics: Technology, AI, business and the economy, Lao tax and accounting, stocks
and crypto — explained in plain, formal Lao for an everyday reader.

> Most of this repo is prompts and posts (Markdown), but `tools/` and
> `skills/*/scripts/` are real Python that the workflow depends on. Treat changes
> there as code changes and test them by running the script.

---

## How a story gets made

```
 1. Research      skills/breaking-news-report  → verified facts + sources
 2. Write         commands/*-prompt.md         → Lao post in posts/
 3. Clean         tools/fix_posts.py           → Lao spelling / Unicode fixes
 4. Visuals       tools/render_cards.py        → 4-card image set (1080×1350)
                  tools/single_post/           → one-image post
 5. Video         tools/news_video/            → 9:16 MP4 with voice + captions
 6. Publish       tools/fb_post.py             → Facebook Page (draft by default)
```

## Repository layout

| Path | What's in it |
| --- | --- |
| `commands/` | Copy-paste prompt templates (`*-prompt.md`) and finished reference posts (`*-example.md`, for illustration only). |
| `posts/` | Drafted and published Lao posts, each with a Sources list. `posts/daily/` holds daily reports with their fact ledgers; `posts/_posted-log.md` tracks what went live. |
| `skills/` | Claude Skills: `breaking-news-report/` (research → draft → cards, with a curated `sources.md`) and `poster-design/`. `lao-accounting-coa/` is a reference dataset (Lao chart of accounts, JSON), not a Skill. |
| `tools/` | Python tooling — see below. |
| `output/` | Card specs (`spec.json`) and render scripts. Rendered images and videos stay local. |
| `preview/` | Small static web app for browsing card specs in a browser. |
| `font/` | Arnfar brand fonts (`Arnfar Font Regular.ttf` / `Bold.ttf`). |
| `arnfar-icon/` | Brand logos, loaded by the renderers at runtime. |

## Tools

### Text

| Script | What it does |
| --- | --- |
| `tools/fix_posts.py` | Fixes the Lao text inside a post (Unicode order, spacing, dictionary spelling). **Run it on every post before publishing.** |
| `tools/lao_fix.py` | The correction engine behind `fix_posts.py`. |
| `tools/gemini_lao_check.py` | Optional AI proofreading pass for Lao. |

```bash
python3 tools/fix_posts.py posts/my-post.md            # fix in place
python3 tools/fix_posts.py posts/my-post.md --check    # report only
python3 tools/fix_posts.py posts/my-post.md --no-dict  # skip the dictionary
```

### Images

| Script | What it does |
| --- | --- |
| `tools/render_cards.py` | Liquid-glass 4-card set (hero / stat / points / action), 1080×1350. `python3 tools/render_cards.py spec.json --outdir output` |
| `tools/single_post/render_single.py` | The house single-image post: headline, photo in a glass frame, credit line, Arnfar ERP ad band. `python3 tools/single_post/render_single.py spec.json` |
| `skills/breaking-news-report/scripts/arnfar_news_card.py` | The card renderer used by the breaking-news Skill. |
| `tools/auto_vector_poster.py` | Zero-spec SVG/PNG poster and background generator. |
| `tools/liquid_glass.py` | Liquid-glass effect helper. |

### Video (`tools/news_video/`)

| Script | What it does |
| --- | --- |
| `render_video.py` | Renders a 1080×1920 news video from `story.json` + a voice WAV. Captions and scene cuts follow the voice. `--preview` writes a contact sheet instead of an MP4. |
| `make_cover.py` | 9:16 reel cover / thumbnail, kept inside the IG and TikTok safe zones. |
| `fetch_photos.py` | Downloads free-licence photos (PD, CC0, CC BY, CC BY-SA) from Wikimedia Commons and records credits. |
| `gen_music.py` | Copyright-free background music made from code, plus synced sound effects. |
| `scenes.py` | Text-free flat illustrations for scenes. |

See `tools/news_video/story_example.json` for the story format.

### Publishing

`tools/fb_post.py` posts to the Arnfar Facebook Page through the Graph API
(drafts by default). Setup: `tools/FACEBOOK_SETUP.md` and `tools/.env.example`.

## Setup

```bash
pip install pillow numpy fonttools          # text + images
pip install scipy playwright                # video
playwright install chromium
```

- Python 3.10+
- `ffmpeg` / `ffprobe` on your `PATH` for video.
- `tools/bin/` ships a `resvg` binary for macOS (Apple Silicon) only. On other
  systems, install [resvg](https://github.com/linebender/resvg) yourself.
- **Lao dictionary:** `fix_posts.py` looks for `tools/data/lao_words.txt`
  (~524k words). It isn't in this repo — add it locally, or use `--no-dict`.

### Preview app

`preview/` loads specs with `fetch()`, which doesn't work from `file://`. Serve
it first:

```bash
python3 -m http.server        # from the repo root
# open http://localhost:8000/preview/
```

## Writing rules

These apply to every template and post:

- **Lao body text.** Common English terms (AI, Crypto, Blockchain, App) are fine inline.
- **Formal, standard and easy.** No slang or chat-speak, and no rare or literary
  words that would stop an ordinary reader.
- **Post structure:** Hook → Intro → The Action → Pros & Cons (✅/❌) → Summary & CTA → Hashtags.
- **Hashtags start with `#arnfar`**, then 3–4 relevant tags.
- **Self-review:** every prompt ends with a native-proofreader pass, and
  `fix_posts.py` still runs after it.
- **Fonts:** the news card images use the Regular weight only, never Bold.

## What isn't committed

- **Images, video and audio.** Rendered cards, photos, MP4s and voice files stay on
  your machine (see `.gitignore`). The only exception is the logos in
  `arnfar-icon/`.
- **Secrets.** `.env` files are never committed.
- **Large font sources** (`font/*.svg`, `.birdfont`, `.eot`). They're over GitHub's
  100 MB limit; only the `.ttf` files are tracked.

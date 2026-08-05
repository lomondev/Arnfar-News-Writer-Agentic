---
name: breaking-news-report
description: >-
  Turn a breaking news event into a ready-to-publish Arnfar Facebook post in Lao
  (ພາສາລາວ), grounded in freshly searched facts. Default structure is the 7-beat
  storytelling flow: Hook → Reality → Why → Data → Impact → Solution → Ending
  (a question or takeaway), then #arnfar hashtags, plus a Sources list. Use
  whenever the user wants to post about breaking news, an unfolding event, a new
  product or model release, an "ຂ່າວດ່ວນ", or pastes a headline/link and says
  "write this up" or "make a post about this". Also use with no topic given —
  "find me something to post", "what's new today" — where it scans a curated
  source list to pick the story. The go-to for news-driven Facebook/TikTok posts
  where accuracy matters. Uses formal, standard Lao only (no slang), can also
  emit a short TikTok caption, runs a Facebook/TikTok community-guidelines
  compliance check, and supports three body shapes: the default 7-beat flow
  plus two optional alternates — ✅/❌ Pros & Cons and news-style/announcement.
---

# Breaking News → Arnfar Facebook Post (Lao)

Produce a ready-to-publish **Arnfar Facebook post in Lao** about a breaking news
event. Two things have to be true at once: the facts must be accurate and
freshly researched (it's *news*), and the writing must be engaging and on-brand
for the Arnfar feed (it's a *Facebook post*). Get the facts first, then dress
them for the feed.

Output is **Lao script (ພາສາລາວ)**. Industry-standard English/proper nouns (AI,
ETF, MCP, company names, tickers, place names) may stay inline, but all
connective prose is Lao.

**Bilingual output (Lao + English).** By default produce the Lao post. When the
user asks for an English version too (or says "bilingual" / "Lao and English"),
keep **both inside a single `## POST` block** so one copy drops a single
Facebook post carrying both languages: a divider line
`— — — [ English Below ⬇️ ] — — —` at the very top (so scrollers see English
exists), then the full Lao version, then the localized English version directly
after it — all between the same `copy from here ↓` / `copy to here ↑` markers.
The divider appears **once, at the top only** — not again at the Lao→English
transition. **Hashtags appear only once**, at the very end after the English
half; do **not** repeat them after the Lao half.
Keep **one** `## Sources` list at the bottom (outside the block). The English
version is **localized, not a literal translation** — same facts, same
structure (whichever body shape the Lao half uses — by default the 7-beat
Hook → Reality → Why → Data → Impact → Solution → Ending flow) and the
same sourced numbers, but rewritten idiomatically for an English-speaking reader
(natural tone, phrasing, and hashtags). Keep the two versions factually
identical; only the language and phrasing differ. See "Bilingual post structure"
and the English tone rules below.

## Why research comes first

A news post is only as good as its facts, and the biggest failure mode is
writing a confident post from memory that's stale or wrong — dates drift,
numbers get revised, "latest" changes by the hour. So gather facts from the live
web *before* drafting, and never invent figures, quotes, or attributions. If a
key fact can't be confirmed, leave it out rather than guess. The engaging tone
never comes at the cost of accuracy.

## Finding a topic automatically (no topic given)

When the user runs this skill **without naming a story** — "find me something
to post", "what's new today", "auto find news" — you pick the topic yourself
instead of asking them for one:

1. **Scan the curated list.** Open `sources.md` (next to this file) and
   `WebFetch` a handful of entries across AI/Tech, Stock Trading, and Crypto —
   these are official (the subject's own site) or specific (a named outlet with
   a track record on that beat), so they're higher-signal than a generic
   search. Use `WebSearch "site:<domain> <topic>"` on any entry that needs
   date-filtering rather than a static blog listing.
2. **Check for duplicates.** `ls posts/` and skim recent filenames/titles so
   you don't redraft a story already covered.
3. **Pick the single best story.** Prefer the most recent, most consequential,
   most Arnfar-relevant item (AI/Tech, Stock Trading, Crypto — per this repo's
   focus) that isn't a duplicate. If nothing genuinely newsworthy turned up
   across the curated sources, say so plainly rather than manufacturing a post
   from a thin story.
4. **Tell the user what you picked** (one line: story + why), then continue
   into the normal research-and-draft workflow below using that story as the
   topic.

This same curated list is also the first stop in step 1 below when the user
*does* name a topic — it's just that here it's also how you choose the topic
in the first place.

## Workflow

1. **Search before writing.** Check the relevant entries in `sources.md` first
   (`WebFetch`/`WebSearch site:<domain>`), then use general `WebSearch` (and
   `WebFetch` for promising sources) to fill in the rest and triangulate — a
   single source can be wrong or behind. Prefer primary sources (official
   statements, the org's own site, filings) and reputable outlets. Note the
   date of each fact and confirm it reflects the current state of the story,
   not an earlier version.

2. **Lock down the 5W1H.** Before drafting, make sure you can answer: **who**,
   **what**, **when**, **where**, **why** it matters, and **how** it unfolded.
   These feed the Intro and The Action sections. If one is genuinely
   unconfirmed, say so plainly rather than inventing it.

3. **Draft the post.** Use the **default 7-beat storytelling flow** (Hook →
   Reality → Why → Data → Impact → Solution → Ending) below unless the user asks
   otherwise. Two optional alternates exist: the **✅/❌ Pros & Cons analysis**
   (switch to it for "pros and cons", "ຂໍ້ດີ ຂໍ້ເສຍ", or a straight
   benefits-vs-risks breakdown — see "Alternate: ✅/❌ Pros & Cons structure"),
   and the **News-style / announcement variant** — headline-led, Key Highlights
   + Why It Matters, restrained emojis (switch to it for a "news-style" /
   "viral" / pure launch/announcement post — see "Alternate: News-style
   variant"). Whichever shape you pick, the language, compliance, and cleaning
   rules below are identical.

4. **Ground the Data, Impact, and Solution in reality.** The Data beat carries
   real, sourced numbers (attributed); the Impact beat states honest stakes, not
   scare-mongering; the Solution beat gives concrete, doable steps for the Lao
   reader / developer / business. If you use the ✅/❌ alternate instead, the same
   rule applies to the Pros & Cons: real benefits and real risks, never filler.
   Keep it honest — a balanced post is more trustworthy and more shareable.

5. **Self-review the Lao for word quality — every time, before cleaning.**
   Re-read your own draft as a native Lao proofreader would, sentence by
   sentence, and fix:
   - **Awkward or literal phrasing** — anything that reads as a word-for-word
     translation rather than something a Lao speaker would actually write.
   - **Wrong or unnatural word choice** — a technically-correct word that isn't
     what a native speaker reaches for in this context.
   - **Slang or non-standard words** — swap any casual chat-speak, regional
     slang, or shortened internet Lao for the formal, standard equivalent (see
     "Language and tone rules").
   - **Words an ordinary reader would trip on** — if a formal word is rare or
     literary, swap it for the plainer formal word most readers already know.
     Formal should never mean harder to read.
   - **Grammar/particle errors** — classifiers, tone-sensitive spelling,
     sentence-final particles, connectors between clauses.
   Rewrite any offending sentence in full rather than patching a word in
   place — a natural sentence beats a technically-fixed one. This is a
   judgment pass (does this sound right, and would every reader understand
   it instantly?), distinct from step 6's mechanical Unicode/dictionary pass —
   do this one first, then run step 6 on the result.

6. **Clean the Lao output** with the repo tool (see "Cleaning the Lao output").

6b. **(Bilingual only) Add the localized English version — same block.** If an
   English version was requested, append it *inside the same `## POST` block*
   directly after the Lao version. Put the `— — — [ English Below ⬇️ ] — — —`
   divider at the **top** of the block (announcing the English half), not
   between the two halves. Follow the identical structure and the
   same sourced facts and numbers, phrased idiomatically for an English reader
   (see the English tone rules under "Language and tone rules"). Because the
   English text lives between the Lao copy markers, `fix_posts.py` will scan it
   too — that's fine (it won't alter Latin text), but run the **Lao** self-review
   (step 5) only on the Lao half. Verify the two halves state the same facts.

6c. **Second-opinion Lao proofread (Gemini).** Once the post file is written and
   `fix_posts.py` is clean, run the independent Lao language check and **show the
   user its output** (see "Second-opinion Lao check (Gemini CLI)"):

   ```bash
   python3 tools/gemini_lao_check.py <path-to-post>.md
   ```

   This is a *third* pass, and it is not redundant: step 5 is your own judgment,
   step 6 is mechanical Unicode/dictionary normalization, and this is a second
   model reading the Lao cold. It catches the class of error you are least likely
   to catch yourself — phrasing that is grammatical and correctly spelled but
   still reads as translated. Report the findings to the user rather than silently
   applying them; only pass `--apply` if they ask, and re-run `fix_posts.py`
   afterwards. If `gemini` is not installed the script says so and exits — that is
   not a failure of the post; note it and move on to step 7.

6d. **Platform-compliance check — mandatory before the post ships.** Read the
   finished post (both halves, if bilingual) against the Facebook and TikTok
   rules in "Platform compliance (Facebook & TikTok)" below and fix anything
   that could get the post removed, limited, or demonetized. This is not
   optional and not a style pass — it is a policy gate. In particular, for
   Arnfar's AI / Stock Trading / Crypto beat, watch financial claims (no
   "guaranteed profit", no buy/sell advice framed as certainty), AI-generated
   media disclosure, misinformation, and scam-adjacent wording. If a claim
   can't be sourced, cut it. Note to the user anything you changed for
   compliance and any residual risk they should eyeball before publishing.

6e. **(Optional) Produce the TikTok caption.** If the user wants to post to
   TikTok too (or asks for "both platforms" / "a TikTok version"), add a
   `## TIKTOK CAPTION` block after the Facebook post — a short, TikTok-tuned
   caption built from the *same sourced facts*, following the TikTok formatting
   rules below. It is a caption, not a re-report: keep it tight. The same
   formal-words rule, compliance gate, and Lao cleaning passes apply to it.

7. **Generate the visuals** — turn your analysis of the news into one or more
   modern Facebook cards (see "Generating Facebook visuals"). Always render at
   least the hero card; add more only when the story genuinely carries more.
   For a scalable/editable deliverable (SVG) or a fast one-image post straight
   from the finished `.md`, use the vector path (Path C).

## Post structure (default — 7-beat storytelling flow)

This is the **default Arnfar Facebook post format**: a seven-beat storytelling
arc that carries the reader from a scroll-stopping hook to a clear takeaway —
**Hook → Reality → Why → Data → Impact → Solution → Ending**. Follow the beats
in order. Write them as **short, flowing paragraphs (1–3 sentences each)**, not
as printed English headers — the bracketed beat names below are guidance for
you, not text to paste into the post. Put the body between the copy markers, and
keep the Sources list *outside* the markers (it's for verification, not for
pasting into Facebook).

**Emojis: restrained and purposeful — aim for 3 or fewer in the whole post.** A
hook emoji and the closing 👉 question are natural; don't prefix every beat with
an emoji. This is an analysis/insight tone, not a sticker wall.

```
## POST (copy from here ↓)

[1. HOOK — ດຶງດູດຄວາມສົນໃຈ: one punchy sentence (+1–2 emojis) that stops the
scroll. Name the thing that happened; don't just tease it.]

[2. REALITY — ຄວາມຈິງທີ່ກຳລັງເກີດຂຶ້ນ: this is really happening, right now.
Front-load who / what / when so the reader knows it's real and current.]

[3. WHY — ເປັນຫຍັງຈຶ່ງເກີດ: the cause — why this is happening now, what's driving
it. One short paragraph.]

[4. DATA — ຂໍ້ມູນ / ຕົວເລກອ້າງອີງ: the proof — key figures, a report, or a
sourced fact, explained simply. Attribute non-obvious claims ("ອີງຕາມ...",
"ບໍລິສັດ ... ລະບຸວ່າ..."). A few • bullets are good for concrete numbers/specs.
Every number must trace to your Sources.]

[5. IMPACT — ຜົນກະທົບ / ຖ້າບໍ່ຮັບມືຈະເປັນແນວໃດ: the stakes — what it means for the
reader / developer / business, and what happens if it's ignored. Honest, not
scare-mongering. Keep any real risk/caveat here (for stock/crypto, the
"ການລົງທຶນມີຄວາມສ່ຽງ — ນີ້ບໍ່ແມ່ນຄຳແນະນຳການລົງທຶນ" line belongs here).]

[6. SOLUTION — ທາງອອກ / ອົງກອນຄວນເຮັດຫຍັງ: concrete, doable steps — what an
organization, developer, or reader should actually do about it.]

[7. ENDING — ສະຫຼຸບ + ຄຳຖາມ: one-line wrap-up of the takeaway, then a genuine
question to drive comments.]
👉 [engaging question] 💬

#arnfar #[Topic] #[Topic] #[Topic]

## (copy to here ↑)

---

## Sources
- [Source title — publisher — URL]
- [Source title — publisher — URL]
```

### Alternate: ✅/❌ Pros & Cons structure

Switch to this shape when the user asks for a **pros-and-cons / "ຂໍ້ດີ ຂໍ້ເສຍ"**
breakdown, or when a straight benefits-vs-risks analysis fits the story better
than the narrative arc. Everything outside the body (formal Lao, self-review,
`fix_posts.py`, Gemini, the compliance gate, `#arnfar`-first hashtags, visuals)
is identical to the default.

```
## POST (copy from here ↓)

[1. Hook — ດຶງດູດຄວາມສົນໃຈ: 1–2 punchy sentences with a couple of emojis that
stop the scroll and signal this is breaking/fresh news.]

[2. Intro — ແນະນຳ: briefly introduce the event and why a Lao reader should care
*right now*. Front-load who/what/when.]

🔍 [3. The Action — ເນື້ອໃນຫຼັກ / ເຫດການທີ່ເກີດຂຶ້ນ: the core of the story —
what actually happened, the key facts and numbers, explained simply. Attribute
non-obvious claims ("ອີງຕາມ...", "ບໍລິສັດ ... ລະບຸວ່າ..."). Use a few • bullets
for the concrete details/specs.]

✅ ຂໍ້ດີ
✅ [real benefit for a Lao reader / developer / business]
✅ [another]
✅ [another]

❌ ຂໍ້ເສຍ / ສິ່ງທີ່ຕ້ອງລະວັງ
❌ [real limitation, risk, or caveat]
❌ [another]
❌ [another]

📌 ສະຫຼຸບ: [one-sentence wrap-up of what it means.]

👉 [engaging question to drive comments.] 💬

#arnfar #[Topic] #[Topic] #[Topic]

## (copy to here ↑)

---

## Sources
- [Source title — publisher — URL]
- [Source title — publisher — URL]
```

### TikTok caption structure (optional second output)

When a TikTok caption is requested, append it **after** the Facebook post's
Sources list, in its own block. TikTok is a video-first platform, so the caption
supports a video — it doesn't carry the whole story. Keep it short (aim ~150
characters, hard cap well under TikTok's limit), front-load the hook in the
first line (the part shown before "…more"), and end with a tight hashtag set.

```
## TIKTOK CAPTION (copy from here ↓)

[1. Hook line — one short, formal Lao sentence + 1–2 emojis. This is the only
part most viewers read, so lead with the single most important fact.]

[2. One-line context or takeaway — optional, one short sentence.]

👉 [short question or CTA] 💬

#arnfar #[Topic] #[Topic] #fyp
## (copy to here ↑)
```

TikTok caption rules: start hashtags with `#arnfar` (the hard branded-hashtag
rule still applies), then 3–5 total including one discovery tag such as `#fyp`
or `#lao`; no links in the caption (TikTok suppresses/blocks them — direct
viewers to the bio link instead); same formal-words rule; and it must pass the
same compliance gate as the Facebook post. Numbers, dates, and any claim must
trace to the same Sources — do not introduce a fact the Facebook post didn't
have.

### Bilingual post structure (Lao + English in one block)

When an English version is requested, keep **both languages inside one `## POST`
block** so a single copy posts them together: an `[ English Below ⬇️ ]` divider
at the top, then the full Lao post, then the localized English post directly
after it, then **one shared** Sources list outside the block.

Both halves follow the **same body shape** — by default the 7-beat flow (Hook →
Reality → Why → Data → Impact → Solution → Ending). If the Lao half uses the
✅/❌ or news-style alternate, the English half mirrors that same shape.

```
## POST (copy from here ↓)

— — — [ English Below ⬇️ ] — — —

[...the full Lao post exactly as in the default structure above — Hook →
Reality → Why → Data → Impact → Solution → Ending + 👉 question. NO hashtags
after the Lao half — the single #arnfar hashtag line goes only at the very end,
after the English half...]

[1. HOOK — one punchy sentence + 1–2 emojis, signalling breaking/fresh news.
Localized, not a word-for-word translation of the Lao hook.]

[2. REALITY — this is really happening now. Front-load who / what / when.]

[3. WHY — the cause: why this is happening now.]

[4. DATA — key figures / a report / a sourced fact, explained simply. Attribute
non-obvious claims ("According to...", "[Company] said..."). A few • bullets for
concrete numbers. Same sourced figures as the Lao half.]

[5. IMPACT — what it means and what happens if ignored. Honest stakes; keep the
"not investment advice" line on trading/crypto posts.]

[6. SOLUTION — concrete steps: what an organization / developer / reader should
do about it.]

[7. ENDING — one-line takeaway, then a genuine question.]
👉 [engaging question to drive comments.] 💬

#arnfar #[Topic] #[Topic] #[Topic]

## (copy to here ↑)

---

## Sources
- [Source title — publisher — URL]
- [Source title — publisher — URL]
```

### On the hook

This is breaking news, so the hook should feel timely — lead with the newest,
most surprising fact ("ຫາກໍປ່ອຍ...", "ມື້ນີ້...", "ຂ່າວໃຫຍ່..."). Concrete beats
vague: name the thing that happened, don't just tease it.

### On The Action

This is where the journalism lives. Lead with the most consequential
development, then the supporting facts. Keep paragraphs short (1–3 sentences) —
people read Facebook on phones. Bullets are good for specs, numbers, dates.
Every non-obvious claim gets attributed to its source.

### On the hashtags

Always start with `#arnfar`, then 3–4 relevant topic hashtags (English or Lao).
This branded-hashtag rule is a hard requirement across Arnfar templates.

## Alternate: News-style variant (announcement format)

An **optional alternate structure** for the post body — reach for it when the
user asks for a "news-style", "viral", or "breaking industry news" post, or when
the story is a **product launch, system/ERP update, new AI feature, company
announcement, or tech-business release** (a headline-led announcement report).
The default 7-beat storytelling flow above remains the default; this is one of
the two alternate shapes you switch to on request or when it clearly fits.

Everything outside the body is unchanged: **output is still formal, standard
Lao** (the formal-words rule applies in full), it still runs the self-review,
`fix_posts.py`, Gemini, and — critically — the **compliance gate** (step 6d),
and it still starts hashtags with **`#arnfar`, then 3–4 total** (this branded
rule wins over any "8–15 hashtags" advice — Facebook down-ranks hashtag walls).
It can still emit a TikTok caption and visuals.

**What's different from the default format:**

- **A headline leads** (5–15 words) — surprising or important, genuine curiosity,
  never fake or clickbait. The body then reads like an industry-news report.
- **Key Highlights + Why It Matters replace the ✅/❌ Pros & Cons** section. But
  honesty and compliance don't lapse: keep any real caveat in "Why It Matters",
  and for **stock/crypto posts still include the risk line**
  ("ການລົງທຶນມີຄວາມສ່ຽງ — ນີ້ບໍ່ແມ່ນຄຳແນະນຳການລົງທຶນ") and never imply
  guaranteed returns. Newsy tone is not a licence to drop the financial-risk
  framing the compliance section requires.
- **Restrained emojis — maximum 3 in the whole post.** This overrides the
  default's section-marker emojis (🔍✅❌📌👉): in this variant do *not* prefix
  sections with emojis; use at most three, purposefully.
- **Tone models tech/business outlets** — Bloomberg, TechCrunch, Forbes, The
  Verge: professional, modern, short sentences, mobile-friendly, emotional but
  trustworthy, every sentence pulling the reader to the next. Still Lao, still
  formal words.

**Structure (put the body between the copy markers as usual):**

```
## POST (copy from here ↓)

[HEADLINE — 5–15 words, formal Lao, curiosity without clickbait. One strong line.]

[Hook — 1–3 short sentences. Open with "something important just happened":
name what changed and why a Lao reader should care right now.]

[Main Story — short paragraphs (1–3 sentences each), reported like an
announcement. Optionally walk the arc: the situation/problem before → the
solution/what's new → the impact. Attribute non-obvious claims
("ອີງຕາມ...", "ບໍລິສັດ ... ລະບຸວ່າ...").]

ຈຸດເດັ່ນສຳຄັນ (Key Highlights)
• [biggest benefit or fact — concrete, sourced]
• [what changed / what's new]
• [who benefits and what to expect next]

ເປັນຫຍັງຈຶ່ງສຳຄັນ (Why It Matters)
[1–2 sentences on the real-world impact for the reader/business. Fold in any
honest caveat here; keep the risk line on trading/crypto posts.]

[Call to Action — one genuine question or invite: "ທ່ານຄິດແນວໃດ?",
"ນີ້ຈະຊ່ວຍທຸລະກິດຂອງທ່ານໄດ້ບໍ?", "ຕິດຕາມ Arnfar ເພື່ອອັບເດດເພີ່ມ." — no
engagement-bait like "tag 3 friends".]

#arnfar #[Topic] #[Topic] #[Topic]

## (copy to here ↑)

---

## Sources
- [Source title — publisher — URL]
```

The bilingual (Lao + English) and TikTok-caption rules apply here too — same
markers, same single Sources list, same `#arnfar`-first hashtags.

## Language and tone rules

- Natural, grammatically correct Lao script throughout.
- Conversational, exciting, yet professional — this is a brand's news post, not
  a dry wire report and not hype that oversells.
- **Word choice: formal & standard only, always easy to understand.** Use
  formal, standard Lao vocabulary (ຄຳສັບທາງການ/ມາດຕະຖານ) throughout — while
  keeping the tone warm and conversational. Within "formal," always pick the
  plain, common version of a word over a rare or literary one, so an ordinary
  reader understands it immediately without needing to re-read. Formal ≠
  complicated: the goal is a reader who is never stopped by an unfamiliar word.
  This is a **hard rule**, not a preference — a single slang word breaks the
  brand voice. **Never use, anywhere in the post:**
  - **Slang / chat-speak / internet Lao** — shortened or phonetic spellings,
    meme words, gamer/streamer lingo, or anything you'd type in a private DM
    but not in a published article.
  - **Regional colloquialisms** — words specific to one province or dialect
    that a general Lao reader might not share. Choose the nationally-standard
    word.
  - **Casual sentence-final particles used for a chummy tone** (e.g. ເນາະ,
    ວ່ະ, ໂລດ, ຫວາ used as filler). A warm tone comes from clear phrasing, not
    from casual particles.
  - **Loanword slang / Thai-isms / romanized abbreviations** used as slang
    (555, ok, 5G-speak). Industry-standard English terms (AI, Crypto, ETF, App)
    are still fine inline — those are terminology, not slang.
  - **Crude, aggressive, or clickbait-y wording** — no insults, no "you won't
    believe…", no fake urgency that overstates the facts.
  When unsure whether a word is too casual, assume it is and use the plain
  formal equivalent.
- Explain jargon briefly in Lao the first time it appears
  (e.g. "ETF (ກອງທຶນຊື້-ຂາຍໃນຕະຫຼາດຫຼັກຊັບ)").
- Emojis are welcome but purposeful (hook, section markers, CTA) — don't litter
  every line.
- Numbers, currency, dates: format for a Lao reader. Use LAK with thousands
  separators for kip (e.g. "12,500 ກີບ"); keep foreign currencies labeled (USD).
  Write dates as ວັນທີ DD ເດືອນ YYYY.

### English version — tone rules (bilingual posts)

When writing the `## POST — ENGLISH` block, keep the same facts, structure, and
sourced numbers as the Lao post, but write it as a native English social post,
not a translation:

- **Localize, don't translate.** Rewrite each section idiomatically. If a Lao
  turn of phrase has no natural English equal, use the closest natural English
  phrasing rather than a literal calque.
- **Tone:** clear, warm, professional — engaging without hype. Short paragraphs
  (1–3 sentences); people read on phones.
- **Keep the same body shape as the Lao half.** By default that's the 7-beat
  flow: Hook → Reality → Why → Data → Impact → Solution → Ending → 👉 question →
  hashtags. If the Lao half used the ✅/❌ alternate, mirror it (Pros → Cons /
  Watch-outs → Bottom line) with the English section labels. The English half
  sits inside the same `## POST` block, directly after the Lao half (the
  `— — — [ English Below ⬇️ ] — — —` divider is at the top of the block only).
- **Explain jargon briefly in English** the first time it appears
  (e.g. "ETF (an exchange-traded fund)").
- **Numbers, currency, dates for an English reader:** keep foreign currencies
  labeled (USD); for kip write "12,500 LAK (~USD X)"; write dates as
  "Month DD, YYYY".
- **Hashtags:** still start with `#arnfar`, then 3–4 relevant English topic
  hashtags — mirror the Lao post's topics, don't invent new claims.
- **Facts must match the Lao version exactly.** Every number, name, and claim in
  the English half must trace to the same Sources. If you revise a fact, revise
  both halves.
- **`fix_posts.py` scans the whole block**, including the English half, since
  both languages sit between the Lao copy markers. That's fine — it leaves Latin
  text alone. Just run the judgment-based Lao self-review (step 5) on the Lao
  half only.

## Platform compliance (Facebook & TikTok)

Every post has to survive two gatekeepers before it's worth publishing: Meta's
**Facebook Community Standards** and TikTok's **Community Guidelines**. Content
that trips them gets removed, down-ranked ("shadow-limited"), or costs the Page
its reach — so treat this as a hard gate (workflow step 6d), not advice. Write
to the stricter of the two by default; a post that satisfies both is safe on
either. Policies evolve, so when a post sits near a line, check the current
official pages: Facebook — https://transparency.meta.com/policies/community-standards/ ,
TikTok — https://www.tiktok.com/community-guidelines .

### Content rules that apply to both platforms

- **No misinformation / misleading content.** This is the fastest way to get
  limited on both platforms (TikTok's 2026 rules tightened "misleading
  content" specifically). Every factual claim must trace to your Sources; if
  it can't be confirmed, cut it. Don't overstate, don't imply certainty the
  source doesn't support, don't use an old number as if it were current.
- **Financial content — the biggest risk for Arnfar's beat.** Stock/crypto
  posts must be framed as *information and education, not investment advice*.
  Never promise or imply guaranteed returns ("ກຳໄລແນ່ນອນ", "ລວຍໄວ", "ບໍ່ມີ
  ຄວາມສ່ຽງ"), never tell readers to buy/sell a specific asset as a sure thing,
  and keep the honest ❌ risk points. A short risk/disclaimer line
  ("ການລົງທຶນມີຄວາມສ່ຽງ — ນີ້ບໍ່ແມ່ນຄຳແນະນຳການລົງທຶນ") is good practice on any
  trading/crypto post. Avoid anything resembling a pump, a "signal group", or a
  get-rich scheme — both platforms treat those as scams/fraud.
- **No health/medical claims** without a credible source; no miracle cures or
  dosage advice.
- **Disclose AI-generated media.** Both Facebook and TikTok now require realistic
  AI-generated or heavily-synthetic images/video to be labeled. If a card or
  visual is AI-generated and could be mistaken for a real photo, label it (in
  caption and, where the platform offers it, with the built-in AI-content
  toggle). Illustrative brand graphics (the liquid-glass cards) are clearly
  non-photographic and don't need this, but a realistic fake photo does.
- **No hate speech, harassment, violence, or attacks** on people or protected
  groups; keep criticism about ideas/products, not people.
- **No scams, fraud, deceptive engagement, or spam** — no "comment to get rich",
  no fake giveaways, no misleading thumbnails/hooks that the body doesn't
  deliver on.
- **Respect IP.** Don't paste copyrighted article text, photos, or logos you
  don't have rights to; summarize in your own Lao words and cite the source.
  For TikTok video, use only commercially-cleared or platform-provided audio.
- **No restricted/illegal goods** (weapons, drugs, regulated financial products
  sold directly, counterfeit) and no adult content.
- **No dangerous acts or harmful challenges** (chiefly a TikTok concern).
- **Avoid engagement-bait phrasing.** "Tag 3 friends", "share to win", "comment
  YES" are down-ranked by Facebook. A genuine open question (the ✅ CTA style
  this skill already uses) is fine and encouraged.

### Facebook-specific formatting

- Links are allowed in the post body, but a post that is *mostly* an outbound
  link gets less reach — lead with real value in the text, put the link lower.
- Keep hashtags modest (the `#arnfar` + 3–4 topical set this skill already
  uses); walls of hashtags read as spam on Facebook.
- No fake urgency or clickbait hooks; the hook must match what the body
  actually delivers.

### TikTok-specific formatting

- **Caption is short and hook-first** — see "TikTok caption structure". The
  first line is often all that's shown before "…more", so the key fact leads.
- **No links in the caption** (TikTok blocks/suppresses them) — send viewers to
  the bio link instead.
- **Hashtags:** `#arnfar` first, then 3–5 total, may include one discovery tag
  (`#fyp`, `#lao`); don't stuff.
- **Label AI content** with the in-app AI-generated toggle when the video/image
  is realistic synthetic media, and disclose paid/commercial content per
  TikTok's branded-content rules if the post is promotional.
- The formal-words rule still applies — TikTok's casual culture is not a licence
  for slang here; Arnfar's voice stays formal and clear.

### Pre-publish compliance checklist

Run this against the finished post (and TikTok caption, if any) before shipping:

- [ ] Every claim/number traces to a Source; nothing overstated or stale.
- [ ] No guaranteed-profit / buy-sell-advice framing; risk points kept; trading/
      crypto posts carry a short "not investment advice" line.
- [ ] No misinformation, hate, harassment, scams, or engagement-bait.
- [ ] Realistic AI-generated visuals are labeled (both platforms).
- [ ] No copyrighted text/media reused without rights; sources cited.
- [ ] Facebook: link placed low, hashtags modest, hook matches body.
- [ ] TikTok: caption short & hook-first, no links, `#arnfar` + ≤5 hashtags.
- [ ] Formal-words rule holds — no slang/chat-speak/casual particles anywhere.

## Cleaning the Lao output

This is the mechanical pass, and it runs **after** the judgment-based
self-review in workflow step 5 — the self-review catches *wrong words and
awkward grammar*; this tool catches *rendering-level* issues (combining marks,
spacing, cluster order) and known dictionary typos. Neither substitutes for
the other; both run every time, in that order. From the repo root:

```bash
python3 tools/fix_posts.py <path-to-post>.md
```

Use `--check` to preview corrections without writing, or `--whole` to normalize
a file that has no copy markers.

Beyond the structural Unicode fixes, **dictionary word correction is on by
default**: it segments the Lao (DP longest-match) against the bundled
`tools/data/lao_words.txt` (~524k words merged from the Tesseract
`lao.traineddata` training list, LaoNLP corpora incl. `lao-eng-dictionary.csv`,
Google's Lao spellcheck dict, and Lao Wiktionary) and fixes an uncovered span
only when a single unambiguous edit-distance-1 candidate exists — so brand
names and transliterations (ຄຣິບໂຕ, ເຕັກໂນໂລຢີ) pass through untouched. Pass
`--no-dict` for structural fixes only.

## Second-opinion Lao check (Gemini CLI)

The last language gate before the post ships, and the only one where a *different
model* reads the Lao cold. Run it after `fix_posts.py` reports clean:

```bash
python3 tools/gemini_lao_check.py <path-to-post>.md          # dry run — report only
python3 tools/gemini_lao_check.py <path-to-post>.md --apply  # write suggestions in
python3 tools/gemini_lao_check.py posts/*.md --strict        # exit 1 on any issue
```

It sends only the lines **between the copy markers** that contain Lao (the `#`
title and the Sources list are excluded), each prefixed `LNNN|` so every
suggestion maps back to an exact line, and asks Gemini for strict JSON limited to
five defect classes: `awkward` (translated-sounding), `wordchoice`, `slang`,
`rare` (a formal word too literary for an ordinary reader), and `grammar`. The
prompt explicitly tells the model **not** to flag English/proper nouns (AI, GPU,
NVDA), numbers, emoji, hashtags, or markdown, and not to fact-check or restyle —
so it stays a language check, not a rewrite. It also scans for Thai-script leaks
while it's there.

Two things to keep in mind when using it:

- **Report, don't auto-apply.** Show the user the findings and let them decide.
  `--apply` does a verbatim substring replace and *skips* any suggestion whose
  `original` no longer matches character-for-character (printing `~~ skipped`)
  rather than corrupting the line — but a silent rewrite of the user's Lao is
  worse than a flagged issue. After any `--apply`, re-run `fix_posts.py`.
- **It is non-deterministic.** Two runs will flag slightly different things. Treat
  it as a second opinion, not a linter; `fix_posts.py` remains the deterministic
  gate.

Requires the Gemini CLI on PATH (`npm install -g @google/gemini-cli`, then run
`gemini` once to sign in). Flags: `--model` (default `gemini-2.5-pro`), `--raw`
(dump the model's JSON), `--strict`, `--apply`.

## Generating Facebook visuals

A breaking-news post lands harder with a strong image. Either way the rule is the
same: the visual must reflect *your analysis of the news*, and every number or
claim on it must be backed by your Sources — never decorative invention.

There are **three production paths**; pick per the job:

- **Path A — In-house PIL cards (default for news).** Fast, free, pixel-precise,
  and fully on-brand via the bundled `scripts/arnfar_news_card.py`. Best for
  news cards: hero headline, "what changed" lists, big stat, and a code-editor
  card for dev news. Dark **liquid-glass** look — a deep navy background with a
  blue glow (top-left) and green glow (bottom-right), frosted glass panels with
  saturation-lifted backdrop blur, **edge refraction** (the glows bend at the
  panel rim), a curved top-left specular sweep + hot spot, an inner depth
  shadow, and blue→green gradient accents. Use this unless the user
  specifically wants a richer illustrated style.
- **Path B — Canva MCP (rich/illustrated promos).** Use when the user wants a
  polished, illustrated, 3D, or product-promo look (e.g. a bright mascot poster,
  a feature showcase, an app/dashboard mockup) that vector drawing can't
  reproduce. Generates editable designs in the user's Canva account.
- **Path C — Auto vector poster (`tools/auto_vector_poster.py`).** One command
  turns the finished post `.md` (or raw text) into a poster PNG in the same
  liquid-glass style, no spec needed — it auto-examines the content (headline,
  subhead, topic motif, key stat, ✅/❌ items, hashtag chips, date). **Only the
  PNG is saved by default**; pass `--svg` when the user actually wants the
  scalable/editable vector file (Figma/Illustrator) or a background asset
  (`--bg-only` always keeps its `.svg`, since that mode's whole point is the
  vector layer). Use this path for a quick single-image post without writing a
  card spec.

All are documented below. For a routine multi-card news post, Path A is almost
always the right call; Path C is the fastest single-image path.

## Path A — In-house cards (`arnfar_news_card.py`)

The bundled renderer does the drawing; your job is to decide *what each card
should say*, an editorial choice driven by the facts you gathered.

### Content-design patterns (write each card to this)

Every card should move the reader **Attention → Interest → Trust → Value →
Action**. Use this master shape to decide a card's text:

```
ATTENTION   big title — one idea, creates a curiosity gap
INTEREST    evidence — a mockup / chart / dashboard / UI, not a claim
TRUST       a number — proof, not adjectives
VALUE       2–3 concrete benefits
ACTION      one-line takeaway
```

Apply these rules when filling a spec:

- **One card = one idea.** Each image teaches exactly one thing — never mix
  topics. A 3-card post is 3 separate ideas (e.g. *what it is* → *the proof* →
  *why it matters*), not one idea spread thin. Map this to the post arc:
  hero/`feature`/`showcase` = the BIG IDEA, `points` = the EVIDENCE/benefits,
  `stat` = the TRUST number.
- **Curiosity-gap headlines.** The `headline`/`accent` states the *result*
  without fully explaining it, so the reader has to read on — "Xiaowei", "163
  Websites Built with Claude", "Polygraph". Don't pre-answer the question the
  image should raise. Push the explanation into `subhead` and `points`.
- **Show evidence, don't assert.** Prefer a `feature` mockup (browser / video /
  dashboard), a `showcase` chart, or `points` with concrete items over vague
  claims. "Claude builds websites" is weak; "163 real websites" with a UI shot
  is strong. People trust screenshots and specifics over adjectives.
- **Numbers create trust.** Put at least one real, sourced figure on the card —
  a `stat` value, a `badge`, a chart bar, or a `body_sub`. Write "adoption +189x"
  / "1.4B MAU" / "$269B", never "growing fast". Every number must trace to your
  Sources.
- **Visual hierarchy ≈ 40/30/20/10.** ~40% headline, ~30% evidence, ~20%
  takeaway, ~10% branding. Keep card text short and glanceable — Level 1 (title)
  > Level 2 (`subhead`) > Level 3 (`points`/chips). The renderer already enforces
  most of this; your job is to keep each level terse.
- **Tool/launch template.** For any new tool, model, framework, or technique, a
  reliable 3-card fill is: card 1 `feature`/`showcase` = *[Name] + one-line value
  prop + mockup/chart + badges*; card 2 `points` = *3 key benefits*; card 3
  `stat` = *the one number*. End on a single-line conclusion.

These are editorial rules for choosing card text — the brand look (glass, glow,
gradient) is handled by the renderer.

### Reference design DNA (the "made-with-Claude" look)

The strongest Arnfar cards follow a consistent shape worth copying:

- **3-pill tag row, top-left.** A `tags` array of 2–3 short labels — the first
  renders highlighted (white), the rest dark glass (e.g. `["AIagent","DevTools",
  "Coding"]`). Use it as the at-a-glance category. (`Arnfar` wordmark stays
  top-right.)
- **A big, realistic product mockup as the evidence** filling the upper ~60%:
  an app gallery, a terminal, a window collage, a browser being driven, or a
  **comparison leaderboard**. Show real UI, not claims.
- **A bottom band that reads name → promise → proof:** a huge headline (the
  product/subject name as a curiosity hook), a bold local-language line
  (`accent`), a blue `subhead` with a left accent bar, and optionally a `url`.
- **In any comparison, highlight the "self / winner" row** in brand teal so the
  eye lands on it (see the `leaderboard` mockup's `highlight`).
- **Numbers everywhere**, each traceable to Sources.

### How many cards — default to 4

**Default to a 4-card set** that walks the Attention → Interest → Trust → Value
arc, since every kind now shares the same modern look (particles, glow, glass
depth, badges, icon/marker chips):

1. **Hero** — `feature` (product/tool) or `showcase` (benchmark), else `hero`/`code`. The BIG IDEA.
2. **Evidence** — a `points` card of *what it is / what it does* (3–5 items).
3. **Trust** — a `stat` card: the one number, with `badges` and sub-metric `chips`.
4. **Value/caveats** — a `points` card of benefits + ✅/❌ from your Pros & Cons.

Drop to 3 only for a genuinely thin story, or add a 5th for a meaty release;
never exceed 5. The kinds below are the building blocks:

- **`hero`/`feature`/`showcase`/`code`** — the headline angle. Every post gets one.
- **Add a `points` card** when the story has 3+ concrete takeaways worth
  showing on their own (specs, what-changed, the ✅/❌ from your Pros & Cons).
  Reuse the analysis you already wrote — don't invent new claims for the image.
- **Add a `stat` card** when one number *is* the story (a price, a record, an
  adoption figure, a percentage). One striking figure, big.
- **Use a `code` card** as the hero for dev / AI-coding / developer-tool news
  (a new model, SDK, runtime, framework). It draws a glassy `main.go`-style
  code-editor mockup under the headline, with an "AI Agent" badge — great for a
  programming-flavored story. Set `hashtags` to show them across the bottom.
- **Use a `showcase` card** as the hero for **model-release / benchmark news**
  (a new frontier model, a "X beats Y" leaderboard story). It's the premium,
  Apple-style release card: a benchmark **bar chart** up top, a **Sol/Terra/Luna
  solar-system** illustration in the middle, and a big bold bottom headline with
  a blue subhead. Reach for it when one image should carry "here's the score and
  here's who won." Full-bleed — it draws no source footer. Add `body_subs`
  (a caption under each planet, e.g. price/role) and `badges` (floating glass
  pills) for extra detail.
- **Use a `feature` card** as the hero for **product / tool / how-to posts**
  (an app, SDK, framework, service). It's the modern, detailed product hero:
  headline + a glassy **mockup** (browser, video player, or dashboard) with
  floating **stat badges** and a row of **feature chips with icons**, over
  particles and glow. Reach for it when the story is "here's a tool and what it
  does" rather than a benchmark. Keeps the normal footer/hashtags. The `stat`
  card also takes `badges` (floating pills) and `chips` (a centered row of
  sub-metric glass pills); `points` cards take an optional `eyebrow`.

Because each card is rendered from the same researched facts, the images stay
accurate. Never put a number or claim on a card that isn't backed by your
Sources.

### Run the renderer

Write a JSON spec describing the cards, then run:

```bash
python3 skills/breaking-news-report/scripts/arnfar_news_card.py spec.json --outdir <dir>
```

It writes one PNG per card (`<prefix>-01.png`, `-02.png`, … or just
`<prefix>.png` for a single card). It applies the Arnfar brand automatically in a
dark **liquid-glass style**: **frosted glass cards that refract** blue/green
glows with a top gloss sheen and a bright specular edge, bright legible text, the
logo + wordmark, the brand fonts, and blue→green gradient accents (headline
underline, pills, the stat number, marker chips). Default size is **Facebook
portrait 1080×1350**; set `"size"` to `square` (1080×1080), `landscape`
(1200×630), or `story` (1080×1920), or `[W, H]`.

**Backgrounds are cinematic, multi-layer, and tech-themed.** Each card gets a
*different* on-brand backdrop (cycled by position): glow placement and grid style
change so a 4-card set never repeats. Behind the glass, a layered scene builds
real depth, back→front: a **far perspective grid** converging to a vanishing
point (atmospheric perspective), **volumetric light rays** from the scene's light
source, a **mid-ground circuit-trace network** with nodes (the tech motif, with
perspective scaling — lower nodes larger/brighter), accent rings + sparkles, and
big **out-of-focus bokeh discs** hugging the edges (depth of field / foreground
framing). Elements hug the side rails / top / bottom, leaving the centre as
**negative space** for the headline and cards — and the frosted panels refract
the whole scene. All automatic — no spec field needed.

**Thematic motif (`motif`).** Set a top-level (or per-card) `motif` to draw a
large faint line-art scene element matching the story — `robot`, `ai` (neural
net), `aicoding` (a.k.a. `computer`/`laptop`/`coding` — a laptop showing code with
an AI sparkle), `code`, `chip`, `gear` (a.k.a. `tools`/`software`), `cloud`,
`chart`, `rocket`, `shield`, `globe`, `calculator` (a.k.a. `accounting`/`ledger`/
`invoice` — a calculator body with a screen and button grid), `warning` (a.k.a.
`danger`/`dangerous`/`alert`/`hazard`/`risk` — a warning triangle with an
exclamation mark), `support` (a.k.a. `help`/`headset` — a headset), `heart`
(a.k.a. `healthy`/`health`/`wellness`/`pulse` — a heart with a pulse/EKG line).
It renders in the upper-right behind the glass with a soft glow. **Pick per
situation**: an AI assistant → `robot` or `ai`; AI coding / dev agent →
`aicoding`; a dev tool / SDK → `code` or `chip`; a launch → `rocket`; security
news → `shield`; cloud/infra → `cloud`; markets/data → `chart`; accounting/tax/
finance-ops → `calculator`; a threat, breach, or risk story → `warning`;
customer support/help content → `support`; wellness/health content → `heart`.
Omit it for a clean tech backdrop. If you set `style` (below) and omit `motif`,
the style's default motif is used automatically.

**Category style (`style`) — a distinct backdrop mood per content category, not
just a different icon.** Set a top-level (or per-card) `style` to recolor the
background glow, circuit-trace network, and motif tint away from the standard
Arnfar blue→green — while the logo, wordmark, glass-card chrome, and `#arnfar`
footer always stay brand blue→green so every card still reads as Arnfar:

| `style` | Accent colors | Default motif |
|---|---|---|
| `ai` | blue → green (brand default) | `ai` |
| `technology` (a.k.a. `tech`) | blue → green (brand default) | `chip` |
| `tools` | blue → green (brand default) | `gear` |
| `accounting` (a.k.a. `account`/`accountancy`/`bookkeeping`) | navy → gold | `calculator` |
| `danger` (a.k.a. `dangerous`/`hazard`/`risk`) | deep red → amber | `warning` |
| `support` (a.k.a. `helpdesk`/`customer-support`/`help`) | soft blue → warm amber | `support` |
| `healthy` (a.k.a. `health`/`wellness`) | green → teal | `heart` |

Omit `style` (or use `ai`/`technology`/`tools`) to keep the original all-blue→
green look — this is a pure addition, every existing spec renders unchanged.
Pick `style` by the *content*, not just the topic label: a ransomware/breach
story is `danger` even though it's also "tech news"; an accounting/tax post is
`accounting` even though Arnfar also covers stock trading in the brand blue→
green. When in doubt, `danger` and `healthy` are the two styles most worth
reaching for deliberately — they're the ones where the default blue→green
would actively undersell the content's tone (urgency, calm).

**Footer is a branded hashtag line.** Every card (except full-bleed `showcase`)
ends with a centered `#arnfar   #ArnfarERP   #arnfar.com` sign-off. Override it
per-post or per-card with `footer_tags`. (Source domains are no longer drawn on
the image — keep them in the post's Sources list instead.)

### Spec format

Top-level keys (`brand`, `category`, `tags`, `footer_tags`, `motif`, `style`,
`size`, `prefix`) apply to every card; any card can override them. `cards` is
the list. `tags` (a 2–3 item array) draws the highlighted pill row top-left in
place of `category`.

```json
{
  "size": "portrait",
  "prefix": "arnfar-<slug>",
  "category": "ຂ່າວເຕັກໂນໂລຊີ",
  "style": "ai",
  "footer_tags": "#arnfar   #ArnfarERP   #arnfar.com",
  "cards": [
    {"kind": "hero", "eyebrow": "SHORT LATIN LABEL",
     "headline": ["Lao line 1", "Lao line 2"], "accent": "gradient line",
     "subhead": "one supporting line", "chips": ["tag", "tag", "tag"],
     "date": "ສະບັບ ...", "date_sub": "..."},
    {"kind": "code", "headline": ["Lao headline"], "accent": "v0.30.9",
     "subhead": "one supporting line", "file": "main.go", "badge": "AI Agent",
     "hashtags": "#arnfar  #AICoding  #LaoDev"},
    {"kind": "points", "title": "Lao title",
     "items": [{"mark": "check", "text": "..."},
               {"mark": "cross", "text": "..."},
               {"mark": "dot",  "text": "..."}]},
    {"kind": "stat", "value": "10,000+", "label": "Lao label", "note": "Lao note"},
    {"kind": "showcase",
     "chart": {"title": "TerminalBench 2.1",
               "legend": ["GPT-5.6", "Mythos5", "AInews"],
               "bars": [{"label": "GPT-5.6 Sol Ultra", "value": 91.9, "highlight": true},
                        {"label": "GPT-5.6 Sol", "value": 88.8, "color": "light"},
                        {"label": "Claude Mythos 5", "value": 88.0, "muted": true},
                        {"label": "GPT-5.6 Terra", "value": 80.2, "color": "light"}]},
     "bodies": ["Sol", "Terra", "Luna"],
     "body_subs": ["$5 / 1M", "$2.5 / 1M", "$1 / 1M"],
     "badges": ["Limited Preview", "API + Codex"],
     "date": "ວັນທີ 26 ມິຖຸນາ 2026 · Product · Release",
     "headline": ["Lao line 1", "Lao line 2"],
     "subhead": ["Lao supporting line 1", "Lao supporting line 2"]},
    {"kind": "feature", "eyebrow": "SHORT LATIN LABEL",
     "headline": ["Brand"], "accent": "Lao tagline",
     "subhead": "one supporting line",
     "mockup": {"type": "video", "title": "promo.html", "tag": "1080p", "time": "0:06 / 0:15"},
     "badges": ["Apache 2.0", "v1.0"],
     "features": [{"icon": "code", "text": "Lao feature 1"},
                  {"icon": "bolt", "text": "Lao feature 2"},
                  {"icon": "layers", "text": "Lao feature 3"},
                  {"icon": "globe", "text": "Lao feature 4"}],
     "hashtags": "#arnfar  #Tool  #LaoDev"}
  ]
}
```

Card kinds:

- **`hero`** — the headline card. `headline` is a list of short Lao lines (the
  renderer auto-fits the font to width); `accent` is one line drawn in the
  brand gradient; optional `eyebrow`, `subhead`, `chips`, `stat`, `date`/`date_sub`.
- **`code`** — a dev/AI-coding headline card. Same `headline`/`accent`/`subhead`
  as hero, plus a glassy code-editor mockup. Optional `file` (default
  `"main.go"`), `badge` (default `"AI Agent"`, set `""` to hide), and `hashtags`
  (a string shown across the bottom in place of the footer). The code lines are
  decorative, seeded per card — no real source is rendered.
- **`points`** — a list of dark liquid-glass cards. Each item has `text` and a
  `mark`: `check` (green ✓), `cross` (red ✕), `dot` (blue), or `num` (numbered
  badge). Long text wraps automatically. Ideal for "what changed" or your ✅/❌
  analysis.
- **`stat`** — one big gradient number (`value`) with a `label` and optional
  `note`. Use when a single figure is the headline.
- **`stack`** — a "tools / tech stack" card: a `title`/`eyebrow` plus a list of
  `tools`, each `{icon, name, role}` rendered as a glass row (gradient icon
  badge + bold name + one-line role). Use it to show *what a product is built on
  or which tools to use* (e.g. WeLM · DeepSeek · Mini-Programs). Icon names are
  the same set as `feature`.
- **`showcase`** — the premium Apple-style release/benchmark card. Keys:
  `chart` (`title`, `legend` up to 3 — first pill is highlighted white, and
  `bars`: each `{label, value, ...}` where the bar color is `highlight: true`
  → brand blue→green gradient, `muted: true` → dark gray competitor, else light;
  override with `color: "grad"|"light"|"dark"`, optional `value_label`, and a
  chart-level `max` defaulting to 100); `bodies` (the three sphere labels,
  default `["Sol","Terra","Luna"]` — Sol is the glowing sun, Terra the blue-green
  earth, Luna the gray moon); `date` (a centered line under the planets);
  `headline` (bold white Lao lines, auto-fit); and `subhead` (string or list,
  blue, with a gradient left bar). The `chart` block is optional — omit it for a
  planets-only hero. Add `body_subs` (3 captions, one under each sphere) and
  `badges` (floating glass pills) for extra detail. Renders full-bleed, no footer.
- **`feature`** — the modern, detailed product/tool hero. Keys: `headline` /
  `accent` / `subhead` / `eyebrow` / `url` (the `url` renders as a blue link line
  under the subhead); `mockup` (`type`: `"browser"` with a `url`, `"video"` with
  `title`/`tag`/`time`, `"dashboard"` with `tiles`, or **`"leaderboard"`** with
  `label` + `rows`); `badges` (floating glass pills); and `features` (a list of
  `{icon, text}` → a 2-column chip grid; omit for a mockup-only hero). Icon
  names: `code`, `bolt`, `layers`, `globe`, `play`, `video`, `chart`, `lock`,
  `doc`, `clock`, `check`, `spark`, `dot`.
  - **`leaderboard` mockup** — a ranked comparison (the Oxlo.ai look). `rows` is
    a list of `{icon, name, value, highlight?}`; the `highlight: true` row is the
    brand-teal "self / winner" row. Great for pricing / "X vs the field" stories.

Any card may also override `footer_tags` (the branded footer line) and
`category`. The footer is always the branded hashtag sign-off — topical
post hashtags live in the `.md` post body, not on the image.

### Visual content rules

- Keep card text **short** — headlines are glanceable, not paragraphs. Push
  detail into the post body, not the image.
- Latin `eyebrow`/labels may be uppercase; **never uppercase Lao** and avoid
  tight letter-spacing on Lao (it collides with tone marks).
- **Every image uses `Arnfar Font Regular.ttf` only — never Bold, for any text.**
  This applies to *all* on-card text — Lao, Latin, headlines, eyebrows, badges,
  the wordmark, everything — not just Lao. The Bold face is too heavy for the
  Arnfar liquid-glass look and collides with Lao tone marks/vowel clusters, so
  it is never used. This is a hard brand rule, enforced centrally so no card
  kind or spec field can opt back into Bold:
  - **Path A (`arnfar_news_card.py`):** `ALL_REGULAR = True` aliases
    `BOLD_PATH` to `REG_PATH` at the top of the script, so every `font(BOLD_PATH,
    ...)` call site actually loads `Arnfar Font Regular.ttf`. Do not flip this
    to `False` and do not reintroduce a separate Bold path in new code — if you
    add a new card kind, keep using the existing `font`/`fit_font` helpers so it
    inherits this automatically.
  - **Path C (`auto_vector_poster.py`):** `FONT_FAMILY = "Arnfar Font"` with no
    `font-weight` ever set, and only `Arnfar Font Regular.ttf` is registered
    from the repo `font/` dir — so it renders Regular by construction.
  - **Path B (Canva):** the on-brand style prompt doesn't request a weight;
    treat any bold-looking Canva output the same as the existing Lao-garbling
    caveat — cosmetic, not something to chase, since Canva isn't using the
    Arnfar font files at all.
- Run any Lao that will appear on a card through the same `fix_posts.py`
  normalization, and check for Thai-script leaks
  (`grep -nP '[\x{0E00}-\x{0E7F}]'`) — Lao and Thai look alike but are different
  Unicode blocks.
- **Always view each rendered PNG before presenting it** to confirm the Lao
  shaped correctly and nothing overflows or collides.

## Path C — Auto vector poster (`tools/auto_vector_poster.py`)

The zero-spec path: point it at content and it designs the poster itself.
From the repo root:

```bash
# from the finished post file (best: headline from the md title, stat/✅❌ from the body)
python3 tools/auto_vector_poster.py posts/<post>.md

# from raw text / a topic line
python3 tools/auto_vector_poster.py "ຂ່າວດ່ວນ! ..." --prefix <slug>

# also want the editable vector file, not just the PNG
python3 tools/auto_vector_poster.py posts/<post>.md --svg

# just the vector background layer (for use behind other compositions)
python3 tools/auto_vector_poster.py posts/<post>.md --bg-only
```

Outputs `<name>.png` to `output/vector/` (override with `--outdir`) — that's
the deliverable for a normal post; add `--svg` only if the user actually wants
the scalable/editable file too (Figma/Illustrator). `--bg-only` always keeps
its `.svg` alongside the PNG, since the vector layer is the point of that
mode. `--size` accepts `portrait` (1080×1350, default), `square`, `landscape`,
`story`. `--no-png` skips rasterization (keeps the `.svg` only, since it'd
otherwise be the sole output).

What the auto-examine extracts (all Lao normalized through the same
`lao_fix` engine, dictionary correction included):

- **headline** — the md `#` title (or the hook), split on — / : into ≤2 lines,
  auto-fit and truncated;
- **topic → category pill + eyebrow + motif** — keyword scoring picks AI
  (`chip` motif), crypto (`coin`), stocks (`chart`), else tech;
- **key stat** — first $/% figure not already visible in headline line 1, with
  a short clause as its label;
- **✅/❌ panels** — up to 2+2 items (section headers ຂໍ້ດີ/ຂໍ້ເສຍ filtered out;
  rows shed automatically to fit the canvas);
- **chips** — the post's topic hashtags (minus `#arnfar`); **date** if present.

The SVG is true vector: the glass panels are real backdrop blur (clipped
`<use>` of the background + blur/saturate filter) with sheen, rim light, and
brand hairlines — editable in Figma/Illustrator and infinitely scalable.
PNG export tries `resvg_py` (pip), then the bundled
`tools/bin/resvg-<os>-<arch>` binary, then `rsvg-convert`; fonts load from the
repo `font/` dir (family "Arnfar Font", Regular weight only). Emoji are
stripped and ✓/✕ are drawn as vector paths. **View the PNG before presenting**
— same rule as Path A.

## Path B — Canva (rich/illustrated promo posters)

Use the Canva MCP when the user wants a photorealistic look the vector renderer
can't produce: the **Apple Liquid Glass** premium style (the default — see the
prompt pattern below), a glossy product/app promo, an illustrated mascot, or a
feature showcase with an app-dashboard mockup. Canva's generator renders that
fidelity; you supply a detailed prompt and curate the results.

### Flow

1. **(Optional) brand kit.** If exact brand colors/logo/fonts matter, call
   `list-brand-kits` and ask the user which to use, then pass `brand_kit_id` to
   `generate-design`. Otherwise encode the Arnfar palette in the prompt (below)
   and offer a brand-kit regeneration afterward.
2. **Generate.** Call `generate-design` with `design_type: "instagram_post"`
   (1080×1350 portrait, 4:5 — ideal for the Facebook feed) and a rich `query`.
   For a square FB post use `facebook_post`; for a print piece use `poster`.
3. **Curate.** It returns ~4 candidates as Canva URLs. You can't preview the
   image thumbnails inline (they're images, not fetchable text), so present the
   candidate links and ask the user to pick.
4. **Make it editable.** On their choice, call `create-design-from-candidate`
   (`job_id` + `candidate_id`) to add it to their Canva account, then share the
   editable link.

### Prompt pattern — Apple Liquid Glass (default style)

This is the **default Arnfar image style**. Build every `generate-design` query
from three parts: (1) the Liquid Glass **style block** below verbatim, (2) the
**Arnfar palette override**, (3) the **content** — layout slots + every on-image
text string spelled out. Style first, then brand, then content.

**(1) Style block — paste this into the query:**

> Design a premium social media post using Apple's Liquid Glass design language.
> Create a futuristic, elegant, highly modern composition with translucent glass
> panels, frosted glass effects, soft reflections, subtle transparency, and
> realistic light refractions. Style: Liquid Glass UI aesthetic; glassmorphism
> with layered depth; smooth rounded corners; soft ambient lighting; elegant
> gradients with vibrant highlights; crystal-clear reflections and blur effects;
> premium technology-inspired appearance; minimalist luxury design. Layout: a
> central glass card floating above a soft gradient background; multiple
> translucent glass layers creating depth; modern typography with strong visual
> hierarchy; clean spacing and balanced composition; space reserved for logo,
> title, subtitle, and call-to-action. Background: abstract fluid gradients;
> light particles and subtle glow; depth-of-field effect; premium digital
> atmosphere. Visual quality: ultra high resolution, photorealistic glass
> materials, sharp details, professional advertising quality, clean and
> sophisticated. Keywords: Liquid Glass, Glassmorphism, Apple Design, Modern UI,
> Premium Technology, Transparent Layers, Luxury Branding, High-End Digital Design.

**(2) Arnfar palette override (always include — overrides the generic "purple/
silver" tones):**

> Color palette: Arnfar blue-to-green gradient — blue #0394F1, cyan, through
> green #15C67A — with soft silver/white accents. The frosted glass panels,
> glows, gradient highlights, light particles, and the logo all use this
> blue→cyan→green range. Avoid purple/magenta. Dark deep-navy backdrop so the
> blue-green glass and reflections pop.

**(3) Content — fill the reserved slots and spell out the text:**

- **Logo:** the "Arnfar" wordmark (top-right; news category pill top-left to
  match the in-house layout).
- **Title / subtitle / CTA:** give the exact Lao strings for each.
- **Supporting elements:** mirror any reference the user shared (stat chips, an
  app/code mockup, etc.), rendered as translucent glass layers.
- **Aspect ratio:** square `facebook_post` (1080×1080) for this style by default,
  or `instagram_post` (1080×1350 portrait) for the feed — pick per the request.

### The Lao-text caveat (important)

Canva's AI commonly **garbles complex Lao script**. Treat any Lao it renders as a
placeholder. Always hand the user the exact Lao strings (normalized through
`fix_posts.py` first) so they can replace the on-poster text in the Canva editor.
List them clearly: logo, tagline, each stat label, dashboard labels, each pill.
Don't claim the generated Lao is correct — tell the user to verify and fix it.

### Stats and honesty

The same accuracy rule applies: real numbers must trace to a source. If you use
sample figures to fill a promo layout, label them to the user as illustrative
placeholders to swap later — never present invented stats as real.

## Example (abbreviated)

**Input topic:** "Z.ai released GLM-5.2, a new open-source AI model"

**Output shape:**

```
## POST (copy from here ↓)

🚀 AI ໂອເພນຊອດໂຕໃໝ່ມາແລ້ວ! GLM-5.2 ອ່ານໄດ້ເຖິງ 1 ລ້ານຄຳໃນເທື່ອດຽວ ⚡️

[REALITY] ບໍລິສັດ Z.ai ຫາກໍປ່ອຍ AI ໂມເດລລ່າສຸດຊື່ GLM-5.2 ເມື່ອວັນທີ 13 ມິຖຸນາ
2026 ແລະ ຕອນນີ້ນັກພັດທະນາທົ່ວໂລກເລີ່ມນຳໄປໃຊ້ແລ້ວ.

[WHY] ການແຂ່ງຂັນ AI ໂອເພນຊອດກຳລັງຮ້ອນແຮງ — ຜູ້ພັດທະນາຢາກໄດ້ໂມເດລທີ່ເກັ່ງ ແຕ່
ບໍ່ຜູກຂາດ ແລະ ນຳໄປຕິດຕັ້ງເອງໄດ້.

[DATA] ອີງຕາມເອກະສານທາງການຂອງ Z.ai:
• Context window ໃຫຍ່ເຖິງ 1 ລ້ານ token
• ນ້ຳໜັກໂມເດລປ່ອຍແບບ Open Source (MIT)

[IMPACT] ຖ້າທຸລະກິດລາວບໍ່ເລີ່ມສຶກສາ AI ແບບນີ້ ອາດຕາມຄູ່ແຂ່ງບໍ່ທັນ — ແຕ່ການ host
ເອງກໍຕ້ອງໃຊ້ server ແຮງສູງ ແລະ ຄວາມຮູ້ດ້ານເຕັກນິກ.

[SOLUTION] ເລີ່ມທົດລອງຜ່ານ API ກ່ອນ, ຫຼື ຮ່ວມກັບທີມທີ່ມີປະສົບການ ກ່ອນຈະລົງທຶນ
ຕິດຕັ້ງເອງເຕັມຮູບແບບ.

[ENDING] 📌 ສະຫຼຸບ: GLM-5.2 ເປີດໂອກາດໃຫ້ຄົນລາວເຂົ້າເຖິງ AI ລະດັບໂລກແບບຟຣີ.
👉 ທ່ານຢາກເອົາ AI ນີ້ໄປເຮັດຫຍັງ? ມາແບ່ງປັນກັນ! 💬

#arnfar #GLM #OpenSourceAI #LaoTech

## (copy to here ↑)

---

## Sources
- New Released — Z.AI Developer Document — https://docs.z.ai/release-notes/new-released
```

The bracketed `[REALITY]`/`[WHY]`/… labels above are shown only to mark the beats
for this example — **don't print them in a real post**; write each beat as a
flowing paragraph. The fixed points: a timely Lao hook, a reality beat that
front-loads who/what/when, a why beat for the cause, a sourced data beat with
attribution, an honest impact beat (with any caveat), a concrete solution beat, a
one-line takeaway + comment-driving question, `#arnfar` + topic hashtags, and a
Sources list (outside the copy markers) backing every key fact.

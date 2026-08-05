# Lao Announcement Post — Reusable Prompt Template (Hook-First Copywriting Framework)

> Use this one when *you* are the one announcing something (a new feature, a
> product, a promo, an event) rather than reporting on outside news — you
> already know the topic, the audience, and the benefit; this template's job
> is to make people actually stop and read it. Paste the **PROMPT** block into
> Claude and fill in the four bracketed lines. Follows the standard Arnfar
> post format (✅/❌, `#arnfar` hashtags) reshaped as a 5-part, hook-first
> direct-response framework.

---

## PROMPT (copy from here ↓)

**System / Persona:**
Act as an expert social media copywriter who natively speaks and writes in the
Lao language, specializing in high-engagement Facebook posts for the Arnfar
brand (Technology, AI, Stock Trading, Crypto). I need you to write a Facebook
announcement post based on the following:

```
Topic/News to announce: [INSERT WHAT YOU ARE ANNOUNCING HERE]
Target Audience: [INSERT WHO THIS IS FOR]
The main benefit to them is: [INSERT WHY THEY SHOULD CARE]
Call to Action / Link: [INSERT WHAT YOU WANT THEM TO DO NEXT]
```
_e.g._
- _Topic: "We just launched Lao-language customer support in our app" / Audience: "existing app users who've filed support tickets" / Benefit: "get answered in Lao, same day, no more waiting on English-only replies" / CTA: "open the app and tap Help"_

**Language Rules:**
- Write entirely in natural, grammatically correct Lao script (ພາສາລາວ).
- Word choice must be formal and standard Lao (ຄຳສັບທາງການ/ມາດຕະຖານ) — no slang, chat-speak, or regional colloquialisms. Within "formal," always pick the plain, common word over a rare or literary one, so an ordinary reader understands every sentence instantly. Formal must never mean harder to read.
- Industry-standard English terms (AI, App, Crypto, Blockchain) may stay inline; connective prose stays Lao.
- Conversational, exciting, yet professional. Purposeful emojis — enough to earn attention, never enough to feel spammy.
- Speak to **one reader**, not a crowd — use direct address ("ท่าน") so it reads personal, not like a press release.

**Please write the post following this exact 5-part Arnfar framework, in order:**

1. **The "Stop-the-Scroll" Hook (ດຶງດູດຄວາມສົນໃຈ):** A disruptive opening in the
   first 1–2 lines — a bold question, a surprising fact, or naming a specific
   problem the Target Audience actually has. Do not lead with the announcement
   itself; lead with the thing that makes them stop scrolling. Create a
   curiosity gap — raise the question the rest of the post answers.
2. **The Core Value (ຄຸນຄ່າຫຼັກ):** Immediately follow the hook by stating the
   direct benefit to *this reader* — pull straight from "the main benefit to
   them," in their language, not the feature's language. Benefit before
   mechanism: say what's in it for them before explaining how it works.
3. **The Action (ເນື້ອໃນຫຼັກ):** Explain the topic/news itself simply — what it
   actually is, what changed, or how it works. Use a few • bullets for
   concrete details. This is where you earn the claim made in part 2.
4. **Pros & Cons (ຂໍ້ດີ ແລະ ຂໍ້ເສຍ):** ✅ real benefits and ❌ honest
   limitations/caveats (cost, availability, what it doesn't do). An honest ❌
   list is what makes the ✅ list believable — don't skip it.
5. **Summary & CTA (ສະຫຼຸບ ແລະ ຊັກຊວນລົງມືເຮັດ):** One sentence reinforcing the
   core value, then a **direct, concrete call to action** built from
   "Call to Action / Link" — tell the reader exactly what to do next (click,
   message, visit, sign up), not a vague "what do you think?" This post's job
   is to move people to act, not just to start a conversation.

**Hashtags:** MUST start with `#arnfar`, followed by 3–4 relevant hashtags in
English or Lao.

**Before finalizing — quality check:** Re-read your own draft as a native Lao
proofreader would, sentence by sentence. Fix any awkward or literal (word-for-
word) phrasing, any word choice that's technically correct but not what a
native speaker would actually use, any slang or non-standard word (replace
with the formal, standard equivalent), and any word an ordinary reader would
trip on (replace a rare/literary word with the plainer formal one) — and any
grammar or particle errors. Rewrite the whole sentence rather than patching a
single word. Only output the post after this pass.

Generate the Facebook post now based on these exact rules.

## (copy to here ↑)

---

## Why this framework works for Lao readers

This reorders the standard Arnfar structure (Hook → Intro → Action → Pros/Cons
→ Summary & CTA) around one idea: **earn the read before you explain
anything.** In a Facebook feed, the first line decides whether anyone sees
line two.

- **Hook before announcement.** "We launched X" is not a hook — it's what
  every brand posts. A question, a surprise, or naming a real problem the
  reader has is what interrupts the scroll. Save "X" for part 3.
- **Benefit before mechanism.** People decide *whether to keep reading* based
  on "what's in it for me," not "how it works." Part 2 answers that in one
  line before part 3 gets into detail.
- **Talk to one person.** Direct address ("ท่าน", "เจ้า") reads as a message
  to the reader, not a broadcast — it consistently reads warmer in Lao than a
  third-person announcement voice.
- **An honest ❌ list builds trust, which builds shares.** A post that only
  lists upsides reads like an ad; a couple of honest limitations makes the
  benefits credible — and credible posts get shared, not just liked.
- **End with one concrete action.** An announcement's job is conversion, not
  just conversation — so the CTA names the exact next step instead of asking
  an open-ended question (that's the right move for a *news* post, not an
  *announcement* — see `lao-breaking-news-report-prompt.md` for that case).
- **Short, phone-readable paragraphs and formal-but-plain word choice** (see
  Language Rules) keep the post easy to read on a phone, which is where
  almost every Lao Facebook reader will see it.

## How to use this for best results

1. **Fill in all four inputs concretely** — a vague Target Audience or Benefit
   produces a vague hook. "People who like tech" is weak; "app users who've
   waited days for an English-only support reply" gives the hook something
   real to name.
2. **The CTA should be one action, not a menu** — "comment ສົນໃຈ below" or
   "tap the link in bio" beats "check it out and let us know what you think."
3. **Review the Lao** — the prompt now forces a self-proofread pass before
   output, but always give it one more read yourself before publishing. If
   you're working inside this repo, also run
   `python3 tools/fix_posts.py <file>.md` for the mechanical Unicode/dictionary
   pass.
4. **Pair it with a card** — see `skills/breaking-news-report/SKILL.md`'s
   "Generating Facebook visuals" section for the in-house renderer; the same
   Attention → Interest → Trust → Value → Action design shape maps directly
   onto this post's 5 parts.

# Facebook posting — one-time setup

`tools/fb_post.py` posts an Arnfar post file (body + card images) to the Arnfar
Facebook **Page** through the Graph API. Default mode is **draft** — the post is
created unpublished so you review it in Meta Business Suite before it goes live.

Stdlib only. No `pip install`.

---

## 1. Create a Meta app

1. <https://developers.facebook.com/apps> → **Create app**
2. Use case: **Other** → type: **Business**
3. In the app, add the **Facebook Login for Business** product (needed only to
   mint the token) and the **Pages API**.
4. App settings → Basic → copy **App ID** and **App Secret**.

You do **not** need App Review as long as you are an admin of the Page and the
app stays in Development mode — a Page admin can always act on their own Page.

## 2. Get a short-lived user token

1. <https://developers.facebook.com/tools/explorer>
2. Top-right: pick your app, then **User Token**.
3. Add permissions: `pages_show_list`, `pages_manage_posts`,
   `pages_read_engagement`.
4. **Generate Access Token** → approve → copy it. It expires in ~1 hour; that's
   fine, the next step trades it in.

## 3. Exchange it for a non-expiring Page token

```bash
cp tools/.env.example tools/.env
# put FB_APP_ID and FB_APP_SECRET in tools/.env, then:
python3 tools/fb_post.py token --user-token "EAAG...paste the short-lived one..."
```

It prints an `FB_PAGE_ID` / `FB_PAGE_ACCESS_TOKEN` pair for every Page you
administer. Paste the Arnfar pair into `tools/.env`.

Page tokens derived from a *long-lived* user token do not expire — which is what
this command produces. They still die if you change your Facebook password,
revoke the app, or lose your Page role.

Verify:

```bash
python3 tools/fb_post.py check
```

## 4. Post

```bash
# draft (default) — auto-attaches posts/images/<same-slug>*.png
python3 tools/fb_post.py post posts/2026-07-07-nextjs-16.md

# explicit images, in carousel order
python3 tools/fb_post.py post posts/2026-07-03-bitcoin-etf-outflows.md \
  --image posts/images/arnfar-btc-etf-01.png \
  --image posts/images/arnfar-btc-etf-02.png

# schedule for 8am Vientiane tomorrow
python3 tools/fb_post.py post posts/2026-07-07-nextjs-16.md --schedule "2026-07-14 08:00"

# straight to live (asks for confirmation; -y skips it)
python3 tools/fb_post.py post posts/2026-07-07-nextjs-16.md --publish

# see exactly what would be sent, send nothing
python3 tools/fb_post.py post posts/2026-07-07-nextjs-16.md --dry-run
```

Only the text between the `copy from here ↓` / `copy to here ↑` markers is sent.
Titles, the Sources list, and any notes stay out of the Facebook post.

---

## Workflow

```
breaking-news-report skill      →  posts/<slug>.md  +  posts/images/<slug>-NN.png
python3 tools/fix_posts.py posts/<slug>.md      # Lao normalization — always run first
python3 tools/fb_post.py post posts/<slug>.md   # draft on the Page
review in Meta Business Suite → publish
```

## Things that will bite you

- **`tools/.env` is a secret.** A Page token is a full write credential for the
  Page. This repo isn't a git repo yet; if you `git init`, add `tools/.env` to
  `.gitignore` first.
- **Drafts of photo posts.** A draft is created by uploading each photo with
  `published=false` (it stages a media object, visible nowhere) and then making
  one `/feed` post that references them via `attached_media`. If the feed call
  fails, the staged photos are orphaned — harmless, but they linger.
- **Scheduling window.** Facebook accepts 10 minutes to 75 days out. The script
  interprets `--schedule` as **Vientiane time (ICT, UTC+7)** and rejects
  out-of-range times before calling the API.
- **Photo size cap is 4 MB each, 10 photos max.** Checked locally first.
- **Don't pass `--link` with photos.** Facebook ignores one or the other; pick
  a photo post or a link post.
- **A draft is not a scheduled post.** `published=false` with no
  `scheduled_publish_time` sits in Drafts forever until you publish it by hand —
  that's the intended default here.
- **Rate limits** are per-app, not per-post. Bulk backfilling old posts will hit
  error code 4; space them out.

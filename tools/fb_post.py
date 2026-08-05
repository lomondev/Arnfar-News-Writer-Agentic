#!/usr/bin/env python3
"""
fb_post.py — publish an Arnfar post file to a Facebook Page via the Graph API.

Default mode is DRAFT (published=false): the post is created as an unpublished
Page post that you review in Meta Business Suite before it goes live.

Stdlib only (urllib) — no pip install required.

Typical use
-----------
    # 1. one-time: get a long-lived Page token (see tools/FACEBOOK_SETUP.md)
    python3 tools/fb_post.py token --user-token EAAG...short-lived...

    # 2. draft a post + its card image(s)
    python3 tools/fb_post.py post posts/2026-07-07-nextjs-16.md \
        --image posts/images/arnfar-nextjs-01.png

    # 3. schedule it instead (Vientiane time, ICT = UTC+7)
    python3 tools/fb_post.py post posts/2026-07-07-nextjs-16.md \
        --image posts/images/arnfar-nextjs-01.png \
        --schedule "2026-07-14 08:00"

    # 4. go live now (no review step)
    python3 tools/fb_post.py post posts/2026-07-07-nextjs-16.md --publish

Config — tools/.env (see tools/.env.example), or real env vars, which win:
    FB_PAGE_ID=1234567890
    FB_PAGE_ACCESS_TOKEN=EAAG...
    FB_APP_ID=...            # only needed for `token`
    FB_APP_SECRET=...        # only needed for `token`
    FB_GRAPH_VERSION=v23.0   # optional
"""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

REPO = Path(__file__).resolve().parent.parent
ENV_FILE = REPO / "tools" / ".env"
DEFAULT_GRAPH_VERSION = "v23.0"
GRAPH = "https://graph.facebook.com"

# Vientiane is UTC+7, year-round (no DST).
ICT = timezone(timedelta(hours=7))

# Facebook's own limits, enforced client-side so we fail fast with a clear
# message instead of a cryptic Graph error.
FB_MAX_MESSAGE_CHARS = 63_206
FB_MAX_PHOTO_BYTES = 4 * 1024 * 1024  # 4 MB per photo
FB_MIN_SCHEDULE_SEC = 10 * 60  # >= 10 minutes out
FB_MAX_SCHEDULE_SEC = 75 * 24 * 3600  # <= 75 days out
FB_MAX_ATTACHED_MEDIA = 10

BODY_START = re.compile(r"copy\s+from\s+here", re.IGNORECASE)
BODY_END = re.compile(r"copy\s+to\s+here", re.IGNORECASE)


class FBError(RuntimeError):
    """A Graph API error, or a local precondition failure."""


# --------------------------------------------------------------------------- #
# config
# --------------------------------------------------------------------------- #


def load_env() -> Dict[str, str]:
    """Read tools/.env (KEY=VALUE, # comments). Real env vars take precedence."""
    env: Dict[str, str] = {}
    if ENV_FILE.exists():
        for raw in ENV_FILE.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            val = val.strip().strip('"').strip("'")
            env[key.strip()] = val
    for key in (
        "FB_PAGE_ID",
        "FB_PAGE_ACCESS_TOKEN",
        "FB_APP_ID",
        "FB_APP_SECRET",
        "FB_GRAPH_VERSION",
    ):
        if os.environ.get(key):
            env[key] = os.environ[key]
    return env


def require(env: Dict[str, str], *keys: str) -> Tuple[str, ...]:
    missing = [k for k in keys if not env.get(k)]
    if missing:
        raise FBError(
            "missing config: "
            + ", ".join(missing)
            + f"\nset them in {ENV_FILE} (copy tools/.env.example) or export them"
        )
    return tuple(env[k] for k in keys)


def graph_version(env: Dict[str, str]) -> str:
    return env.get("FB_GRAPH_VERSION") or DEFAULT_GRAPH_VERSION


# --------------------------------------------------------------------------- #
# graph transport
# --------------------------------------------------------------------------- #


def _read_json(resp: Any) -> Dict[str, Any]:
    raw = resp.read().decode("utf-8")
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:  # pragma: no cover - graph always sends json
        raise FBError(f"non-JSON response from Graph: {raw[:400]}") from exc


def _raise_graph_error(exc: urllib.error.HTTPError) -> "FBError":
    raw = exc.read().decode("utf-8", "replace")
    try:
        err = json.loads(raw).get("error", {})
    except json.JSONDecodeError:
        return FBError(f"HTTP {exc.code}: {raw[:400]}")
    parts = [
        f"HTTP {exc.code}",
        err.get("type", ""),
        f"code={err.get('code')}",
        f"subcode={err.get('error_subcode')}" if err.get("error_subcode") else "",
        err.get("message", ""),
    ]
    msg = " ".join(p for p in parts if p)
    hint = ""
    if err.get("code") == 190:
        hint = "\nhint: token is invalid or expired — re-run `fb_post.py token`"
    elif err.get("code") in (200, 10):
        hint = (
            "\nhint: the token is missing a permission. The Page token needs "
            "pages_manage_posts + pages_read_engagement, and your account must "
            "have a content role on the Page."
        )
    elif err.get("code") == 4:
        hint = "\nhint: app-level rate limit hit — back off and retry later"
    return FBError(msg + hint)


def graph_get(env: Dict[str, str], path: str, params: Dict[str, str]) -> Dict[str, Any]:
    url = f"{GRAPH}/{graph_version(env)}/{path}?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return _read_json(resp)
    except urllib.error.HTTPError as exc:
        raise _raise_graph_error(exc) from None


def graph_post(
    env: Dict[str, str],
    path: str,
    fields: Dict[str, str],
    file: Optional[Tuple[str, Path]] = None,
) -> Dict[str, Any]:
    """POST to Graph. Multipart when `file` is given, urlencoded otherwise."""
    url = f"{GRAPH}/{graph_version(env)}/{path}"

    if file is None:
        data = urllib.parse.urlencode(fields).encode("utf-8")
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
    else:
        field_name, path_obj = file
        boundary = f"----arnfar{uuid.uuid4().hex}"
        ctype = mimetypes.guess_type(path_obj.name)[0] or "application/octet-stream"
        chunks: List[bytes] = []
        for key, val in fields.items():
            chunks.append(
                f"--{boundary}\r\n"
                f'Content-Disposition: form-data; name="{key}"\r\n\r\n'
                f"{val}\r\n".encode("utf-8")
            )
        chunks.append(
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="{field_name}"; '
            f'filename="{path_obj.name}"\r\n'
            f"Content-Type: {ctype}\r\n\r\n".encode("utf-8")
        )
        chunks.append(path_obj.read_bytes())
        chunks.append(f"\r\n--{boundary}--\r\n".encode("utf-8"))
        data = b"".join(chunks)
        headers = {"Content-Type": f"multipart/form-data; boundary={boundary}"}

    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            return _read_json(resp)
    except urllib.error.HTTPError as exc:
        raise _raise_graph_error(exc) from None


# --------------------------------------------------------------------------- #
# post file parsing
# --------------------------------------------------------------------------- #


def extract_body(md_path: Path) -> str:
    """Pull the publishable body out of an Arnfar post file.

    The body is what sits between the `copy from here ↓` and `copy to here ↑`
    markers. Everything else (title, Sources list, notes) stays out of Facebook.
    Falls back to the whole file if the markers are absent.
    """
    text = md_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    start = end = None
    for i, line in enumerate(lines):
        if start is None and BODY_START.search(line):
            start = i + 1
        elif start is not None and BODY_END.search(line):
            end = i
            break

    if start is None or end is None:
        body_lines = [ln for ln in lines if not ln.lstrip().startswith("#")]
    else:
        body_lines = lines[start:end]

    body = "\n".join(body_lines).strip()
    # collapse 3+ blank lines; Facebook renders them literally
    body = re.sub(r"\n{3,}", "\n\n", body)
    if not body:
        raise FBError(f"{md_path}: no post body found between the copy markers")
    if len(body) > FB_MAX_MESSAGE_CHARS:
        raise FBError(
            f"{md_path}: body is {len(body)} chars, Facebook caps a post at "
            f"{FB_MAX_MESSAGE_CHARS}"
        )
    return body


def guess_images(md_path: Path) -> List[Path]:
    """Find card images that share the post's slug, e.g.
    posts/2026-07-07-nextjs-16.md -> posts/images/2026-07-07-nextjs-16*.png
    """
    images_dir = md_path.parent / "images"
    if not images_dir.is_dir():
        return []
    stem = md_path.stem
    found = sorted(
        p
        for p in images_dir.iterdir()
        if p.stem == stem or p.stem.startswith(stem + "-")
        if p.suffix.lower() in {".png", ".jpg", ".jpeg"}
    )
    return found


def validate_images(images: List[Path]) -> None:
    if len(images) > FB_MAX_ATTACHED_MEDIA:
        raise FBError(
            f"{len(images)} images given; Facebook attaches at most "
            f"{FB_MAX_ATTACHED_MEDIA} to one post"
        )
    for img in images:
        if not img.is_file():
            raise FBError(f"image not found: {img}")
        size = img.stat().st_size
        if size > FB_MAX_PHOTO_BYTES:
            raise FBError(
                f"{img} is {size / 1_048_576:.1f} MB; Facebook rejects photos "
                f"over {FB_MAX_PHOTO_BYTES // 1_048_576} MB"
            )


def parse_schedule(value: str) -> int:
    """'2026-07-14 08:00' (Vientiane time) or a raw unix ts -> unix ts."""
    value = value.strip()
    if value.isdigit():
        ts = int(value)
    else:
        for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M:%S"):
            try:
                ts = int(datetime.strptime(value, fmt).replace(tzinfo=ICT).timestamp())
                break
            except ValueError:
                continue
        else:
            raise FBError(
                f"can't parse --schedule {value!r}; use 'YYYY-MM-DD HH:MM' "
                "(Vientiane time) or a unix timestamp"
            )

    delta = ts - int(time.time())
    if delta < FB_MIN_SCHEDULE_SEC:
        raise FBError(
            "Facebook requires a scheduled time at least 10 minutes in the future "
            f"(yours is {delta // 60} min out)"
        )
    if delta > FB_MAX_SCHEDULE_SEC:
        raise FBError("Facebook won't schedule more than 75 days ahead")
    return ts


# --------------------------------------------------------------------------- #
# publishing
# --------------------------------------------------------------------------- #


@dataclass
class PostResult:
    post_id: str
    photo_ids: List[str]
    mode: str
    permalink: Optional[str] = None


def upload_photo_unpublished(env: Dict[str, str], page_id: str, token: str, img: Path) -> str:
    """Upload one photo with published=false. Returns its media fbid.

    An unpublished photo is a staging object: it doesn't appear anywhere until
    it's referenced from a feed post via attached_media. That's what lets a
    photo post be a real draft.
    """
    res = graph_post(
        env,
        f"{page_id}/photos",
        {"published": "false", "access_token": token},
        file=("source", img),
    )
    fbid = res.get("id")
    if not fbid:
        raise FBError(f"photo upload for {img.name} returned no id: {res}")
    return str(fbid)


def create_post(
    env: Dict[str, str],
    body: str,
    images: List[Path],
    mode: str,
    scheduled_ts: Optional[int],
    link: Optional[str],
) -> PostResult:
    page_id, token = require(env, "FB_PAGE_ID", "FB_PAGE_ACCESS_TOKEN")

    photo_ids = [upload_photo_unpublished(env, page_id, token, img) for img in images]

    fields: Dict[str, str] = {"message": body, "access_token": token}
    if link:
        fields["link"] = link
    for i, fbid in enumerate(photo_ids):
        # Graph wants attached_media[0]={"media_fbid":"..."} as bracketed keys.
        fields[f"attached_media[{i}]"] = json.dumps({"media_fbid": fbid})

    if mode == "publish":
        fields["published"] = "true"
    elif mode == "schedule":
        fields["published"] = "false"
        fields["scheduled_publish_time"] = str(scheduled_ts)
    else:  # draft
        fields["published"] = "false"

    res = graph_post(env, f"{page_id}/feed", fields)
    post_id = str(res.get("id", ""))
    if not post_id:
        raise FBError(f"feed post returned no id: {res}")

    permalink = None
    if mode == "publish":
        try:
            permalink = graph_get(
                env, post_id, {"fields": "permalink_url", "access_token": token}
            ).get("permalink_url")
        except FBError:
            pass  # cosmetic only — the post exists either way

    return PostResult(post_id=post_id, photo_ids=photo_ids, mode=mode, permalink=permalink)


# --------------------------------------------------------------------------- #
# token exchange
# --------------------------------------------------------------------------- #


def exchange_token(env: Dict[str, str], user_token: str) -> None:
    """short-lived user token -> long-lived user token -> non-expiring Page token."""
    app_id, app_secret = require(env, "FB_APP_ID", "FB_APP_SECRET")

    long_lived = graph_get(
        env,
        "oauth/access_token",
        {
            "grant_type": "fb_exchange_token",
            "client_id": app_id,
            "client_secret": app_secret,
            "fb_exchange_token": user_token,
        },
    )
    ll_token = long_lived.get("access_token")
    if not ll_token:
        raise FBError(f"no long-lived token in response: {long_lived}")

    accounts = graph_get(
        env, "me/accounts", {"fields": "id,name,access_token", "access_token": ll_token}
    )
    pages = accounts.get("data", [])
    if not pages:
        raise FBError(
            "this user has no Pages with a content role — check the account is an "
            "admin/editor of the Arnfar Page and that the app was granted "
            "pages_show_list"
        )

    print("\nPage tokens (these do not expire, as long as the user token was long-lived):\n")
    for page in pages:
        print(f"  {page.get('name')}")
        print(f"    FB_PAGE_ID={page.get('id')}")
        print(f"    FB_PAGE_ACCESS_TOKEN={page.get('access_token')}\n")
    print(f"Paste the pair for the Arnfar Page into {ENV_FILE}")
    print("Never commit that file.\n")


def check_token(env: Dict[str, str]) -> None:
    page_id, token = require(env, "FB_PAGE_ID", "FB_PAGE_ACCESS_TOKEN")
    page = graph_get(env, page_id, {"fields": "id,name,fan_count", "access_token": token})
    print(f"page:   {page.get('name')} (id {page.get('id')})")
    if page.get("fan_count") is not None:
        print(f"fans:   {page['fan_count']}")

    debug = graph_get(
        env, "debug_token", {"input_token": token, "access_token": token}
    ).get("data", {})
    expires = debug.get("expires_at", 0)
    print(f"type:   {debug.get('type')}")
    print(f"scopes: {', '.join(debug.get('scopes', [])) or '(none reported)'}")
    print("expiry: never" if not expires else f"expiry: {datetime.fromtimestamp(expires, ICT)} ICT")

    scopes = set(debug.get("scopes", []))
    needed = {"pages_manage_posts", "pages_read_engagement"}
    missing = needed - scopes
    if missing and scopes:
        print(f"\nWARNING: token is missing {', '.join(sorted(missing))} — posting will fail")
    print("\nOK" if not missing else "")


# --------------------------------------------------------------------------- #
# cli
# --------------------------------------------------------------------------- #


def cmd_post(args: argparse.Namespace, env: Dict[str, str]) -> int:
    md_path = Path(args.post)
    if not md_path.is_file():
        raise FBError(f"post file not found: {md_path}")

    body = extract_body(md_path)

    if args.image:
        images = [Path(p) for p in args.image]
    elif args.no_image:
        images = []
    else:
        images = guess_images(md_path)
    validate_images(images)

    mode = "draft"
    scheduled_ts: Optional[int] = None
    if args.publish and args.schedule:
        raise FBError("--publish and --schedule are mutually exclusive")
    if args.publish:
        mode = "publish"
    elif args.schedule:
        mode = "schedule"
        scheduled_ts = parse_schedule(args.schedule)

    print(f"post:   {md_path}")
    print(f"body:   {len(body)} chars")
    print(f"images: {', '.join(p.name for p in images) if images else '(none)'}")
    print(f"mode:   {mode}", end="")
    if scheduled_ts:
        print(f" -> {datetime.fromtimestamp(scheduled_ts, ICT):%Y-%m-%d %H:%M} ICT", end="")
    print()

    if args.dry_run:
        print("\n--- body ---\n")
        print(body)
        print("\n(dry run — nothing sent to Facebook)")
        return 0

    if mode == "publish" and not args.yes:
        answer = input("\nThis goes LIVE immediately. Type 'yes' to continue: ")
        if answer.strip().lower() != "yes":
            print("aborted")
            return 1

    result = create_post(env, body, images, mode, scheduled_ts, args.link)

    print(f"\npost_id:  {result.post_id}")
    if result.photo_ids:
        print(f"photos:   {', '.join(result.photo_ids)}")
    if result.permalink:
        print(f"live at:  {result.permalink}")
    elif mode == "draft":
        print(
            "\nDraft created (unpublished). Review and publish it in Meta Business "
            "Suite -> Content -> Posts -> Drafts."
        )
    elif mode == "schedule":
        print("\nScheduled. It appears under Business Suite -> Content -> Scheduled.")
    return 0


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="fb_post.py",
        description="Publish an Arnfar post file to a Facebook Page (draft by default).",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_post = sub.add_parser("post", help="create a Page post from a post .md file")
    p_post.add_argument("post", help="path to the post markdown file")
    p_post.add_argument(
        "--image",
        action="append",
        metavar="PATH",
        help="image to attach (repeatable, max 10). Default: auto-match posts/images/<slug>*",
    )
    p_post.add_argument("--no-image", action="store_true", help="text-only post")
    p_post.add_argument("--link", help="optional link to attach (omit when posting photos)")
    p_post.add_argument("--publish", action="store_true", help="go live now instead of drafting")
    p_post.add_argument(
        "--schedule", metavar="'YYYY-MM-DD HH:MM'", help="schedule (Vientiane time, ICT)"
    )
    p_post.add_argument("--dry-run", action="store_true", help="print what would be sent")
    p_post.add_argument("-y", "--yes", action="store_true", help="skip the --publish confirmation")

    p_token = sub.add_parser("token", help="exchange a short-lived user token for a Page token")
    p_token.add_argument("--user-token", required=True, help="short-lived user token from Graph Explorer")

    sub.add_parser("check", help="verify the configured Page token works")

    args = parser.parse_args(argv)
    env = load_env()

    try:
        if args.cmd == "post":
            return cmd_post(args, env)
        if args.cmd == "token":
            exchange_token(env, args.user_token)
            return 0
        if args.cmd == "check":
            check_token(env)
            return 0
    except FBError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\naborted", file=sys.stderr)
        return 130
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

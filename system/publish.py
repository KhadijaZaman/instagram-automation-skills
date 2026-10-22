#!/usr/bin/env python3
"""Publish approved posts and send approved replies through the official
Instagram API. Run by the hourly scheduled task, which reads the sheet,
hands the due rows to this script, and writes the results back.

    export IG_ACCESS_TOKEN=...
    python3 publish.py due.json --out results.json
    python3 publish.py due.json --dry-run          # check rows, call nothing

due.json:
    {"posts":   [{"id": "...", "format": "CAROUSEL|IMAGE|REEL", "caption": "...",
                  "media_urls": "https://..., https://..."}],
     "replies": [{"comment_id": "...", "draft_reply": "..."}]}

results.json, one entry per row:
    {"posts":   [{"id", "status": "posted|failed", "ig_media_id", "permalink", "error"}],
     "replies": [{"comment_id", "status": "sent|failed", "sent_at", "error"}]}

Only rows the caller already filtered to status=approved and due belong in
due.json. This script never decides what to post.
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

API = "https://graph.instagram.com/v23.0"
REEL_WAIT_S = 300
POLL_S = 10


class ApiError(Exception):
    pass


def call(method, path, token, **params):
    params["access_token"] = token
    data = urllib.parse.urlencode(params).encode()
    if method == "GET":
        req = urllib.request.Request(f"{API}/{path}?{data.decode()}")
    else:
        req = urllib.request.Request(f"{API}/{path}", data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        try:
            msg = json.loads(body)["error"].get("error_user_msg") or json.loads(body)["error"]["message"]
        except (ValueError, KeyError):
            msg = body[:300]
        raise ApiError(msg) from None


def urls_of(row):
    return [u.strip() for u in (row.get("media_urls") or "").split(",") if u.strip()]


def check(row):
    fmt = (row.get("format") or "").upper()
    urls = urls_of(row)
    if fmt not in ("IMAGE", "CAROUSEL", "REEL"):
        return f"format must be IMAGE, CAROUSEL or REEL, got '{fmt}'"
    if not row.get("caption", "").strip():
        return "caption is empty"
    if len(row["caption"]) > 2200:
        return f"caption is {len(row['caption'])} characters, limit is 2200"
    if not all(u.startswith("https://") for u in urls):
        return "media_urls must be public https links"
    if fmt == "CAROUSEL" and not 2 <= len(urls) <= 10:
        return f"carousel needs 2 to 10 media URLs, got {len(urls)}"
    if fmt in ("IMAGE", "REEL") and len(urls) != 1:
        return f"{fmt.lower()} needs exactly 1 media URL, got {len(urls)}"
    return None


def wait_ready(container, token):
    deadline = time.time() + REEL_WAIT_S
    while time.time() < deadline:
        status = call("GET", container, token, fields="status_code").get("status_code")
        if status == "FINISHED":
            return
        if status in ("ERROR", "EXPIRED"):
            raise ApiError(f"Instagram could not process the media (status {status})")
        time.sleep(POLL_S)
    raise ApiError("media still processing after 5 minutes; will retry next run")


def publish_post(row, token):
    fmt = row["format"].upper()
    urls = urls_of(row)
    caption = row["caption"]
    if fmt == "IMAGE":
        container = call("POST", "me/media", token, image_url=urls[0], caption=caption)["id"]
    elif fmt == "REEL":
        container = call("POST", "me/media", token, media_type="REELS", video_url=urls[0],
                         caption=caption, share_to_feed="true")["id"]
    else:
        children = []
        for u in urls:
            kind = {"video_url": u, "media_type": "VIDEO"} if u.lower().endswith((".mp4", ".mov")) \
                else {"image_url": u}
            children.append(call("POST", "me/media", token, is_carousel_item="true", **kind)["id"])
        for c in children:
            wait_ready(c, token)
        container = call("POST", "me/media", token, media_type="CAROUSEL",
                         children=",".join(children), caption=caption)["id"]
    wait_ready(container, token)
    media_id = call("POST", "me/media_publish", token, creation_id=container)["id"]
    permalink = call("GET", media_id, token, fields="permalink").get("permalink", "")
    return media_id, permalink


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("due", help="due.json")
    ap.add_argument("--out", default="results.json")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    due = json.load(open(args.due))
    token = os.environ.get("IG_ACCESS_TOKEN")
    if not token and not args.dry_run:
        sys.exit("Set IG_ACCESS_TOKEN first.")

    results = {"posts": [], "replies": []}
    for row in due.get("posts", []):
        res = {"id": row.get("id", ""), "status": "failed", "ig_media_id": "", "permalink": "", "error": ""}
        problem = check(row)
        if problem:
            res["error"] = problem
        elif args.dry_run:
            res.update(status="ok (dry run)")
        else:
            try:
                res["ig_media_id"], res["permalink"] = publish_post(row, token)
                res["status"] = "posted"
            except ApiError as e:
                res["error"] = str(e)
        results["posts"].append(res)
        print(f"POST   {res['id']:<24} {res['status']:<14} {res['permalink'] or res['error']}")

    for row in due.get("replies", []):
        res = {"comment_id": row.get("comment_id", ""), "status": "failed", "sent_at": "", "error": ""}
        text = (row.get("draft_reply") or "").strip()
        if not text:
            res["error"] = "draft_reply is empty"
        elif args.dry_run:
            res["status"] = "ok (dry run)"
        else:
            try:
                call("POST", f"{row['comment_id']}/replies", token, message=text)
                res.update(status="sent", sent_at=datetime.now(timezone.utc).isoformat(timespec="seconds"))
            except ApiError as e:
                res["error"] = str(e)
        results["replies"].append(res)
        print(f"REPLY  {res['comment_id']:<24} {res['status']:<14} {res['error']}")

    json.dump(results, open(args.out, "w"), indent=2)
    posted = sum(r["status"] == "posted" for r in results["posts"])
    sent = sum(r["status"] == "sent" for r in results["replies"])
    print(f"PUBLISH  {posted} posted, {sent} replies sent  -> {args.out}")


if __name__ == "__main__":
    main()

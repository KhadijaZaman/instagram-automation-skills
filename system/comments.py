#!/usr/bin/env python3
"""Fetch new comments on recent posts, for /ig-reply to draft answers.

    export IG_ACCESS_TOKEN=...
    python3 comments.py --posts 10 --skip known_ids.txt --out comments.tsv

--skip is a file of comment IDs already in the Replies tab (one per line), so
the same comment is never drafted twice. Read-only.
"""

import argparse
import csv
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://graph.instagram.com/v23.0"


def get(path, token, **params):
    params["access_token"] = token
    url = f"{API}/{path}?{urllib.parse.urlencode(params)}"
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        raise RuntimeError(e.read().decode(errors="replace")[:300]) from None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--posts", type=int, default=10)
    ap.add_argument("--skip", help="file of comment IDs to ignore")
    ap.add_argument("--out", default="comments.tsv")
    args = ap.parse_args()
    token = os.environ.get("IG_ACCESS_TOKEN") or sys.exit("Set IG_ACCESS_TOKEN first.")
    me = get("me", token, fields="id,username")
    skip = set(Path(args.skip).read_text().split()) if args.skip and Path(args.skip).exists() else set()

    rows = []
    media = get("me/media", token, fields="id,permalink,caption", limit=args.posts).get("data", [])
    for m in media:
        page = get(f"{m['id']}/comments", token, fields="id,text,username,timestamp,replies{username}", limit=50)
        for c in page.get("data", []):
            if c["id"] in skip or c.get("username") == me.get("username"):
                continue
            answered = any(r.get("username") == me.get("username") for r in c.get("replies", {}).get("data", []))
            if answered:
                continue
            rows.append({"comment_id": c["id"], "post_permalink": m.get("permalink", ""),
                         "username": c.get("username", ""), "comment": c.get("text", ""),
                         "timestamp": c.get("timestamp", "")})
    with open(args.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["comment_id", "post_permalink", "username", "comment", "timestamp"],
                           delimiter="\t")
        w.writeheader()
        w.writerows(rows)
    print(f"COMMENTS  {len(rows)} new, unanswered  -> {args.out}")


if __name__ == "__main__":
    main()

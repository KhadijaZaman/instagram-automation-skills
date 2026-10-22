#!/usr/bin/env python3
"""Pull post insights from the official Instagram API, so /ig-audit has real
numbers instead of screenshots.

Needs an Instagram professional account (Business or Creator) and a token
from a Meta app with instagram_business_basic and
instagram_business_manage_insights. Set them as environment variables, never
in a file that gets committed:

    export IG_ACCESS_TOKEN=...      # long-lived token
    export IG_USER_ID=...           # optional, defaults to "me"

Usage:
    python3 insights.py                       # last 30 posts -> insights.tsv
    python3 insights.py --limit 60 --out ~/.claude/instagram/insights.tsv
    python3 insights.py --host graph.facebook.com   # if your token is a Facebook Login token

Read-only. It never posts, edits or deletes anything.
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

API_VERSION = "v23.0"
FEED_METRICS = ["reach", "views", "saved", "shares", "total_interactions", "follows", "profile_visits"]
REEL_METRICS = ["reach", "views", "saved", "shares", "total_interactions",
                "ig_reels_avg_watch_time", "ig_reels_video_view_total_time"]
COLUMNS = ["date", "type", "reach", "views", "saved", "shares", "comments", "likes",
           "follows", "avg_watch_s", "save_rate", "share_rate", "first_line", "permalink", "id"]


def get(host, path, token, **params):
    params["access_token"] = token
    url = f"https://{host}/{API_VERSION}/{path}?{urllib.parse.urlencode(params)}"
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        try:
            message = json.loads(body)["error"]["message"]
        except (ValueError, KeyError):
            message = body[:200]
        raise RuntimeError(message) from None


def media_list(host, user, token, limit):
    fields = "id,caption,media_type,media_product_type,permalink,timestamp,like_count,comments_count"
    items, after = [], None
    while len(items) < limit:
        params = {"fields": fields, "limit": min(50, limit - len(items))}
        if after:
            params["after"] = after
        page = get(host, f"{user}/media", token, **params)
        items += page.get("data", [])
        after = page.get("paging", {}).get("cursors", {}).get("after")
        if not after or not page.get("data"):
            break
    return items[:limit]


def insights(host, media_id, metrics, token):
    """Ask for all metrics at once; if the API rejects one, fall back to one at a time."""
    def parse(resp):
        return {m["name"]: (m.get("values") or [{}])[0].get("value", m.get("total_value", {}).get("value"))
                for m in resp.get("data", [])}
    try:
        return parse(get(host, f"{media_id}/insights", token, metric=",".join(metrics)))
    except RuntimeError:
        out = {}
        for m in metrics:
            try:
                out.update(parse(get(host, f"{media_id}/insights", token, metric=m)))
            except RuntimeError:
                pass
        return out


def row(item, data):
    reach = data.get("reach") or 0
    is_reel = item.get("media_product_type") == "REELS"
    avg_ms = data.get("ig_reels_avg_watch_time")
    caption = (item.get("caption") or "").strip().splitlines()
    return {
        "date": item.get("timestamp", "")[:10],
        "type": "REEL" if is_reel else item.get("media_type", ""),
        "reach": reach,
        "views": data.get("views", ""),
        "saved": data.get("saved", 0),
        "shares": data.get("shares", 0),
        "comments": item.get("comments_count", 0),
        "likes": item.get("like_count", ""),
        "follows": data.get("follows", ""),
        "avg_watch_s": round(avg_ms / 1000, 1) if avg_ms else "",
        "save_rate": f"{100 * (data.get('saved') or 0) / reach:.2f}%" if reach else "",
        "share_rate": f"{100 * (data.get('shares') or 0) / reach:.2f}%" if reach else "",
        "first_line": caption[0][:90] if caption else "",
        "permalink": item.get("permalink", ""),
        "id": item["id"],
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--limit", type=int, default=30)
    ap.add_argument("--out", default="insights.tsv")
    ap.add_argument("--host", default="graph.instagram.com")
    args = ap.parse_args()

    token = os.environ.get("IG_ACCESS_TOKEN")
    if not token:
        sys.exit("Set IG_ACCESS_TOKEN first. See the setup section in ig-audit/SKILL.md.")
    user = os.environ.get("IG_USER_ID", "me")

    try:
        items = media_list(args.host, user, token, args.limit)
    except RuntimeError as e:
        sys.exit(f"Instagram API refused the request: {e}")

    rows = []
    for item in items:
        metrics = REEL_METRICS if item.get("media_product_type") == "REELS" else FEED_METRICS
        rows.append(row(item, insights(args.host, item["id"], metrics, token)))

    out = Path(args.out).expanduser()
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS, delimiter="\t")
        w.writeheader()
        w.writerows(rows)

    def score(r):
        return ((r["saved"] or 0) + (r["shares"] or 0)) / r["reach"] if r["reach"] else 0
    print(f"INSIGHTS PULLED  {len(rows)} posts  -> {out}")
    for r in sorted(rows, key=score, reverse=True)[:5]:
        print(f"  {r['date']}  {r['type']:<14} reach {r['reach']:>7}  saves {r['save_rate']:>6}  "
              f"shares {r['share_rate']:>6}  {r['first_line'][:50]}")


if __name__ == "__main__":
    main()

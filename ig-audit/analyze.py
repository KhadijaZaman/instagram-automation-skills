#!/usr/bin/env python3
"""What is working on your Instagram, and what isn't.

Reads the insights table (from insights.py, or typed up from screenshots),
joins it with your content calendar so each post knows its theme and hook
formula, then judges every post against YOUR OWN median, not someone else's
benchmark.

    python3 analyze.py insights.tsv
    python3 analyze.py insights.tsv --calendar ~/.claude/instagram/calendar.csv
    python3 analyze.py insights.tsv --md report.md      # also write a report file

Minimum columns: date, type, reach, saved, shares.
Used when present: views, follows, avg_watch_s, comments, first_line,
permalink, and from the calendar: theme, hook_formula, pov.
"""

import argparse
import csv
import statistics
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

MIN_GROUP = 3  # never call a pattern on fewer posts than this


def num(v):
    try:
        return float(str(v).replace(",", "").replace("%", ""))
    except (TypeError, ValueError):
        return None


def read_table(path):
    text = Path(path).expanduser().read_text()
    delim = "\t" if "\t" in text.splitlines()[0] else ","
    return list(csv.DictReader(text.splitlines(), delimiter=delim))


def join_calendar(posts, cal_path):
    if not cal_path or not Path(cal_path).expanduser().exists():
        return
    cal = read_table(cal_path)
    by_key = {(r.get("date", ""), (r.get("format") or "").upper()): r for r in cal}
    by_date = defaultdict(list)
    for r in cal:
        by_date[r.get("date", "")].append(r)
    for p in posts:
        fmt = "REEL" if p["type"].upper().startswith("REEL") else (
            "CAROUSEL" if "CAROUSEL" in p["type"].upper() else p["type"].upper())
        match = by_key.get((p["date"], fmt)) or (by_date[p["date"]][0] if len(by_date[p["date"]]) == 1 else None)
        if match:
            for c in ("theme", "hook_formula", "pov"):
                if match.get(c) and not p.get(c):
                    p[c] = match[c]


def prepare(rows):
    posts = []
    for r in rows:
        reach = num(r.get("reach"))
        if not reach:
            continue
        p = dict(r)
        p["reach"] = reach
        p["saves"] = num(r.get("saved")) or 0
        p["shares"] = num(r.get("shares")) or 0
        p["follows"] = num(r.get("follows"))
        p["watch"] = num(r.get("avg_watch_s"))
        p["type"] = (r.get("type") or "?").upper()
        p["date"] = (r.get("date") or "")[:10]
        p["save_rate"] = p["saves"] / reach
        p["share_rate"] = p["shares"] / reach
        p["value_rate"] = (p["saves"] + p["shares"]) / reach
        posts.append(p)
    return posts


def judge(posts):
    med_reach = statistics.median(p["reach"] for p in posts)
    med_value = statistics.median(p["value_rate"] for p in posts) or 1e-9
    for p in posts:
        p["reach_x"] = p["reach"] / med_reach
        p["value_x"] = p["value_rate"] / med_value
        # Reach says the hook and the topic travelled. Saves and shares say the
        # content was worth keeping. A post needs one of them well above normal.
        if p["reach_x"] >= 1.5 or p["value_x"] >= 1.5:
            p["verdict"] = "WORKING"
        elif p["reach_x"] <= 0.6 and p["value_x"] <= 0.6:
            p["verdict"] = "NOT WORKING"
        else:
            p["verdict"] = "AVERAGE"
        p["why"] = reason(p)
    return med_reach, med_value


def reason(p):
    r, v = p["reach_x"], p["value_x"]
    if r >= 1.5 and v >= 1.5:
        return "travelled and got kept: repeat the topic, hook and format"
    if r >= 1.5 and v >= 0.9:
        return "travelled, kept at your normal rate: repeat the hook and topic"
    if r >= 1.5:
        return "hook travelled, content not kept: same hook, more useful body"
    if v >= 1.5 and r >= 0.9:
        return "kept well above normal: repeat the content, test a stronger hook"
    if v >= 1.5:
        return "kept but not seen: same content, stronger hook"
    if r <= 0.6 and v <= 0.6:
        return "neither seen nor kept: check the first 2 seconds and the topic"
    return ""


def groups(posts, field):
    g = defaultdict(list)
    for p in posts:
        val = p.get(field)
        if field == "weekday" and p["date"]:
            try:
                val = date.fromisoformat(p["date"]).strftime("%a")
            except ValueError:
                val = None
        if val:
            g[val].append(p)
    out = []
    for name, ps in g.items():
        score = statistics.mean((q["reach_x"] + q["value_x"]) / 2 for q in ps)
        out.append((name, len(ps), score,
                    statistics.mean(q["reach_x"] for q in ps),
                    statistics.mean(q["value_x"] for q in ps)))
    return sorted(out, key=lambda x: x[2], reverse=True)


def verdict_for(rx, vx, n):
    if n < MIN_GROUP:
        return f"too few posts ({n}), keep testing"
    if (rx >= 1.3 and vx >= 0.9) or (vx >= 1.3 and rx >= 0.9):
        return "DO MORE"
    if rx <= 0.7 and vx <= 0.9:
        return "STOP or rework"
    if rx >= 1.3:
        return "reaches, not kept: add substance"
    if vx >= 1.3:
        return "kept, not reached: stronger hooks"
    if rx <= 0.7:
        return "low reach: hook or topic"
    if vx <= 0.7:
        return "low saves/shares: thin content"
    return "keep, not a lever"


def report(posts, med_reach, med_value):
    lines = []
    w = lines.append
    working = sorted([p for p in posts if p["verdict"] == "WORKING"],
                     key=lambda p: p["reach_x"] + p["value_x"], reverse=True)
    failing = sorted([p for p in posts if p["verdict"] == "NOT WORKING"],
                     key=lambda p: p["reach_x"] + p["value_x"])
    w(f"INSTAGRAM ANALYSIS  {len(posts)} posts  "
      f"{min(p['date'] for p in posts)} to {max(p['date'] for p in posts)}")
    w(f"your normal: reach {med_reach:,.0f}, saves+shares {100 * med_value:.2f}% of reach")
    w(f"working {len(working)}  average {len(posts) - len(working) - len(failing)}  not working {len(failing)}")
    w("")

    def post_line(p):
        label = (p.get("first_line") or p.get("pov") or p.get("permalink") or "")[:48]
        return (f"  {p['date']}  {p['type'][:8]:<8} reach {p['reach_x']:>4.1f}x  kept {p['value_x']:>4.1f}x  "
                f"{label}\n      -> {p['why']}")

    w("WHAT'S WORKING")
    w("\n".join(post_line(p) for p in working[:5]) or "  nothing above 1.5x yet")
    w("")
    w("WHAT ISN'T")
    w("\n".join(post_line(p) for p in failing[:5]) or "  nothing below 0.6x on both")
    w("")
    w("PATTERNS  (1.0x = your normal; reach x / kept x)")
    for field, title in [("type", "format"), ("theme", "theme"), ("hook_formula", "hook formula"),
                         ("weekday", "day")]:
        g = groups(posts, field)
        if not g:
            continue
        w(f"  by {title}")
        for name, n, score, rx, vx in g:
            w(f"    {name[:26]:<26} n={n:<3} {rx:>4.1f}x / {vx:>4.1f}x   {verdict_for(rx, vx, n)}")
    reels = [p for p in posts if p["watch"]]
    if len(reels) >= MIN_GROUP:
        top = sorted(reels, key=lambda p: p["reach_x"], reverse=True)
        half = max(1, len(top) // 2)
        w("")
        w(f"  reels: avg watch {statistics.mean(p['watch'] for p in top[:half]):.1f}s on the top half "
          f"vs {statistics.mean(p['watch'] for p in top[half:]):.1f}s on the bottom half")
    w("")
    w("Patterns on fewer than 3 posts are not called. Correlation, not proof:")
    w("a theme can look strong because of one lucky post. Check the posts behind it.")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("insights", help="insights.tsv from insights.py, or a CSV with the same columns")
    ap.add_argument("--calendar", default="~/.claude/instagram/calendar.csv")
    ap.add_argument("--md", help="also write the report to this file")
    args = ap.parse_args()

    posts = prepare(read_table(args.insights))
    if len(posts) < 5:
        sys.exit(f"Only {len(posts)} posts with reach. Need at least 5 to say anything useful.")
    join_calendar(posts, args.calendar)
    med_reach, med_value = judge(posts)
    text = report(posts, med_reach, med_value)
    print(text)
    if args.md:
        Path(args.md).expanduser().write_text("```\n" + text + "\n```\n")


if __name__ == "__main__":
    main()

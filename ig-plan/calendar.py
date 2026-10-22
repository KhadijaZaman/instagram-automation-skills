#!/usr/bin/env python3
"""Keep the content calendar as one CSV that opens in Google Sheets or Excel.

/ig-plan writes the week as rows; this script merges them into the calendar
without duplicating a date+format that is already there, and moves statuses
forward without moving them back.

    python3 calendar.py add week.tsv                 # merge a planned week
    python3 calendar.py status 2026-10-28 REEL shot  # idea -> scripted -> shot -> posted
    python3 calendar.py show                         # what's next, what's stuck

Default file: ~/.claude/instagram/calendar.csv  (override with --file)
"""

import argparse
import csv
import sys
from datetime import date
from pathlib import Path

COLUMNS = ["date", "time", "format", "theme", "pov", "hook_formula", "hook_line",
           "example", "ask", "status", "link", "notes"]
STATUSES = ["idea", "scripted", "shot", "posted"]


def load(path):
    if not path.exists():
        return []
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def save(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    rows.sort(key=lambda r: (r["date"], r["time"]))
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def key(r):
    return (r["date"], r["format"].upper())


def cmd_add(path, source):
    rows = load(path)
    existing = {key(r): r for r in rows}
    with open(source, newline="") as f:
        incoming = list(csv.DictReader(f, delimiter="\t"))
    added = updated = 0
    for r in incoming:
        r = {c: (r.get(c) or "").strip() for c in COLUMNS}
        r["status"] = r["status"] or "idea"
        if key(r) in existing:
            old = existing[key(r)]
            for c in COLUMNS:
                if c != "status" and r[c]:
                    old[c] = r[c]
            updated += 1
        else:
            rows.append(r)
            existing[key(r)] = r
            added += 1
    save(path, rows)
    print(f"CALENDAR  +{added} new  {updated} updated  -> {path}")


def cmd_status(path, day, fmt, status):
    if status not in STATUSES:
        sys.exit(f"Status must be one of: {', '.join(STATUSES)}")
    rows = load(path)
    for r in rows:
        if key(r) == (day, fmt.upper()):
            if STATUSES.index(status) < STATUSES.index(r["status"] or "idea"):
                sys.exit(f"{day} {fmt} is already '{r['status']}'. Not moving it back.")
            r["status"] = status
            save(path, rows)
            print(f"{day} {fmt.upper()} -> {status}")
            return
    sys.exit(f"No {fmt} on {day} in the calendar.")


def cmd_show(path):
    rows = load(path)
    today = date.today().isoformat()
    upcoming = [r for r in rows if r["date"] >= today and r["status"] != "posted"][:7]
    stuck = [r for r in rows if r["date"] < today and r["status"] != "posted"]
    print(f"NEXT UP  ({len(upcoming)})")
    for r in upcoming:
        print(f"  {r['date']} {r['time']:<6} {r['format']:<9} {r['status']:<9} {r['pov'][:60]}")
    if stuck:
        print(f"\nPAST DATE, NOT POSTED  ({len(stuck)})")
        for r in stuck:
            print(f"  {r['date']} {r['format']:<9} {r['status']:<9} {r['pov'][:60]}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", default="~/.claude/instagram/calendar.csv")
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add")
    a.add_argument("source", help="TSV with the calendar columns as a header row")
    s = sub.add_parser("status")
    s.add_argument("date")
    s.add_argument("format")
    s.add_argument("status")
    sub.add_parser("show")
    args = ap.parse_args()
    path = Path(args.file).expanduser()
    if args.cmd == "add":
        cmd_add(path, args.source)
    elif args.cmd == "status":
        cmd_status(path, args.date, args.format, args.status)
    else:
        cmd_show(path)


if __name__ == "__main__":
    main()

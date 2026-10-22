#!/usr/bin/env python3
"""Render carousel slide copy into 1080x1350 PNGs, ready to upload.

No Python packages needed. It writes one HTML file per slide and screenshots
each with a headless Chrome or Chromium that is already on the machine.

Slide file format (slides.md): slides are separated by a line of ---.
The first line of a slide is its headline. Everything after is body text.
A line starting with "- " becomes a list item. The first slide is the cover.

    Stop buying GEO.
    Fix your SEO first.
    ---
    AI answers start in search
    Google's AI Overviews pull from Google's index.
    ---
    The recap
    - Answer in sentence one
    - Put a real number in it

Usage:
    python3 render.py slides.md --out ./carousel
    python3 render.py slides.md --out ./carousel --handle @khadijazaman
    python3 render.py slides.md --html-only        # skip the screenshots
"""

import argparse
import html
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

W, H = 1080, 1350

# Neutral default. Override with ~/.claude/instagram/brand.json or --theme.
DEFAULT_THEME = {
    "background": "#F7F5F0",
    "text": "#1A1A1A",
    "muted": "#5C5C5C",
    "accent": "#2B59C3",
    "cover_background": "#1A1A1A",
    "cover_text": "#F7F5F0",
    "font_heading": "'Inter', 'Helvetica Neue', Arial, sans-serif",
    "font_body": "'Inter', 'Helvetica Neue', Arial, sans-serif",
    "google_font": "Inter:wght@400;600;800",
    "handle": "",
}

CHROME_CANDIDATES = [
    os.environ.get("CHROME", ""),
    "google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
]


def load_theme(path):
    theme = dict(DEFAULT_THEME)
    for candidate in [Path.home() / ".claude/instagram/brand.json", path]:
        if candidate and Path(candidate).is_file():
            theme.update(json.loads(Path(candidate).read_text()))
    return theme


def parse_slides(text):
    slides = []
    for block in text.split("\n---"):
        lines = [l.rstrip() for l in block.strip("-\n").splitlines() if l.strip()]
        if lines:
            slides.append({"headline": lines[0], "body": lines[1:]})
    return slides


def body_html(lines):
    out, items = [], []
    for line in lines:
        if line.lstrip().startswith("- "):
            items.append(f"<li>{html.escape(line.lstrip()[2:])}</li>")
            continue
        if items:
            out.append("<ul>" + "".join(items) + "</ul>")
            items = []
        out.append(f"<p>{html.escape(line)}</p>")
    if items:
        out.append("<ul>" + "".join(items) + "</ul>")
    return "\n".join(out)


def slide_html(slide, index, total, theme):
    cover = index == 0
    bg = theme["cover_background"] if cover else theme["background"]
    fg = theme["cover_text"] if cover else theme["text"]
    head_size = 104 if cover else 72
    font_link = ""
    if theme.get("google_font"):
        font_link = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family='
                     f'{theme["google_font"]}&display=swap">')
    counter = "" if cover else f'<div class="count">{index + 1}/{total}</div>'
    handle = html.escape(theme.get("handle") or "")
    return f"""<!doctype html><html><head><meta charset="utf-8">{font_link}
<style>
  html, body {{ margin:0; width:{W}px; height:{H}px; overflow:hidden; }}
  body {{ background:{bg}; color:{fg}; font-family:{theme["font_body"]}; }}
  .safe {{ position:absolute; inset:120px; display:flex; flex-direction:column;
           justify-content:{"center" if cover else "flex-start"}; }}
  h1 {{ font-family:{theme["font_heading"]}; font-size:{head_size}px; line-height:1.05;
        font-weight:800; margin:0 0 40px; letter-spacing:-1px; }}
  h1::after {{ content:""; display:block; width:96px; height:10px; margin-top:36px;
               background:{theme["accent"]}; }}
  p, li {{ font-size:40px; line-height:1.35; margin:0 0 24px; }}
  p {{ color:{fg if cover else theme["muted"]}; }}
  ul {{ margin:0; padding-left:44px; }}
  li::marker {{ color:{theme["accent"]}; }}
  .count {{ position:absolute; top:56px; right:64px; font-size:32px; color:{theme["muted"]}; }}
  .handle {{ position:absolute; bottom:56px; left:64px; font-size:30px; opacity:.7; }}
</style></head><body>
{counter}
<div class="safe"><h1>{html.escape(slide["headline"])}</h1>{body_html(slide["body"])}</div>
<div class="handle">{handle}</div>
</body></html>"""


def find_chrome():
    for c in CHROME_CANDIDATES:
        if not c:
            continue
        found = shutil.which(c) or (c if Path(c).is_file() else None)
        if found:
            return found
    return None


def screenshot(chrome, html_path, png_path):
    cmd = [chrome, "--headless=new", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
           "--force-device-scale-factor=1", f"--window-size={W},{H}",
           "--virtual-time-budget=3000", f"--screenshot={png_path}", html_path.resolve().as_uri()]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=60)


def lint(slides):
    warnings = []
    if not 5 <= len(slides) <= 10:
        warnings.append(f"{len(slides)} slides. The working range is 6 to 10.")
    if len(slides[0]["headline"].split()) > 6:
        warnings.append("Cover headline is over 6 words. It has to read at thumbnail size.")
    for i, s in enumerate(slides[1:], start=2):
        words = sum(len(l.split()) for l in s["body"])
        if words > 25:
            warnings.append(f"Slide {i} has {words} words of body. Over 25 means it is two slides.")
        if "\u2014" in s["headline"] + " ".join(s["body"]):
            warnings.append(f"Slide {i} has an em dash. Use a comma, colon or full stop.")
    return warnings


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("slides", help="slide file, slides separated by ---")
    ap.add_argument("--out", default="carousel", help="output folder")
    ap.add_argument("--theme", help="JSON file overriding colours and fonts")
    ap.add_argument("--handle", help="handle shown small on every slide")
    ap.add_argument("--html-only", action="store_true", help="write HTML, skip PNGs")
    args = ap.parse_args()

    theme = load_theme(args.theme)
    if args.handle:
        theme["handle"] = args.handle
    slides = parse_slides(Path(args.slides).read_text())
    if not slides:
        sys.exit("No slides found. Separate slides with a line of ---.")

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    chrome = None if args.html_only else find_chrome()
    if not args.html_only and not chrome:
        print("No Chrome or Chromium found. Set CHROME=/path/to/chrome, or use --html-only.")

    for i, slide in enumerate(slides):
        page = out / f"slide-{i + 1:02d}.html"
        page.write_text(slide_html(slide, i, len(slides), theme))
        if chrome:
            screenshot(chrome, page, out / f"slide-{i + 1:02d}.png")

    print(f"CAROUSEL RENDERED  {len(slides)} slides  {W}x{H}  -> {out}/")
    print("files:      " + ("PNG + HTML" if chrome else "HTML only"))
    for w in lint(slides):
        print("  WARN  " + w)


if __name__ == "__main__":
    main()

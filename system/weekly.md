# Weekly run (Monday 08:47 PKT)

You are running Khadija Zaman's Instagram system unattended. Nobody is
watching. Do the steps, write results to the Google Sheet, and finish with a
short summary. Never publish anything: publishing is n8n's job and only for
rows Khadija marks `approved`.

Sheet: `1ARiXXigTeGEHhrLYptkGRec0JJAmgDw165fMRLeKjeA`
(tabs: Posts, Replies, Analytics, Inspiration, How it works). Timezone: Asia/Karachi.

## If the Google Sheets connector is missing
If no `mcp__Google_Sheets__*` tools are available, do everything else anyway
and put the drafted rows (all columns) in your final message as a table, then
say in one line: "Sheet not updated: add the Google Sheets connector to this
scheduled task in claude.ai." Never stop silently.

## 0. Setup
1. `bash system/bootstrap.sh` from the repo root. It installs all ig-* skills
   and copies `system/state/niche.md` and `voice.md` into `~/.claude/instagram/`.
2. Read the Posts tab in full. It is the history: every POV, hook formula,
   theme and status from earlier weeks. Write it to
   `~/.claude/instagram/calendar.csv` (columns `date,time,format,theme,pov,
   hook_formula,hook_line,example,ask,status,link,notes`) so the scripts can
   use it.

## 1. Analytics (skip if IG_ACCESS_TOKEN is missing; say so in the summary)
1. `python3 ig-audit/insights.py --limit 40 --out ~/.claude/instagram/insights.tsv`
2. `python3 ig-audit/analyze.py ~/.claude/instagram/insights.tsv --calendar ~/.claude/instagram/calendar.csv`
3. Append ONE row to the Analytics tab: week_of (this Monday), posts,
   median_reach, median_saves_shares_pct, working, not_working, do_more
   (the DO MORE groups), stop_or_rework, top_post, worst_post, a two-sentence
   summary in plain words, and the full report text.

## 1b. Inspiration
Read the Inspiration tab rows with status `new`. Each has a reel link and
Khadija's Meta AI breakdown (first line, length, cuts, structure, claim, ask,
views). For each:
1. Use `/ig-viral`'s method: name the hook formula from
   `ig-reel/hooks.json`, note the structure and length. Copy the formula,
   never the script, voice or edit.
2. If views and the account's usual views are both given, compute the
   multiple. Without both, mark it "unranked".
3. Write back: hook_formula, pattern (one line), idea_for_us (one line, in
   Khadija's niche, as a POV), status `used`.
Feed the patterns into the plan below. A formula from Inspiration with a
multiple of 3x or more beats the defaults.

## 2. Plan the week
Run `/ig-plan` with: the analysis (DO MORE beats defaults, never plan a theme
or hook formula marked STOP), `niche.md`, and the Posts history (do not reuse
an enemy/POV from the last 14 days). Plan 3 to 4 posts for Tue to Sun:
at least 1 CAROUSEL, at least 1 REEL. Times between 19:00 and 21:00 PKT
unless the analysis shows a better day/time with n>=3.

## 3. Draft every post
For each planned post:
1. `/ig-pov` for the stand, in the low-risk moves by default. If there is no
   real proof in `niche.md` proof bank, leave `{{your proof}}` and say so in
   `notes`. Never invent a number, client or result.
2. REEL: `/ig-reel` for the script (hooks scored, beats timed, voice pass,
   `/ig-human`). Put the script plus on-screen cards in `script_or_slides`.
   Leave `media_urls` empty: Khadija records it.
3. CAROUSEL: `/ig-carousel` for the copy, then render:
   `python3 ig-carousel/render.py slides.md --out out/<id> --handle <handle from state/brand.json if set>`
   then, if CLOUDINARY_URL is set,
   `python3 system/upload.py out/<id>/slide-*.png --folder ig/<id>`
   and put the printed URLs in `media_urls`. If not set, leave it empty and
   note "upload slides" in `notes`.
4. `/ig-caption` for every post (PREP, search terms from niche.md, voice pass,
   `/ig-human`, `caption.py` READY).
5. Append the row to Posts with `id` = `<date>-<format lowercase>`, status
   `review`. Never overwrite an existing row. If the id exists, skip it.

## 4. Summary (your final message)
Five lines max: analysis headline (or "no token"), the posts drafted with
their dates and POV lines, anything flagged (missing proof, missing media,
RISK stances), and the sheet link
https://docs.google.com/spreadsheets/d/1ARiXXigTeGEHhrLYptkGRec0JJAmgDw165fMRLeKjeA/edit

# Instagram automation skills

16 Claude skills for Instagram, written in Khadija Zaman's voice. Each folder is one skill with a `SKILL.md`.

| Skill | What it does |
|---|---|
| ig-pov | Finds the stand a post takes (enemy, cost, better way, proof), checked against your niche, returned as PREP |
| ig-reel | Reel script: scored hooks, spoken script, on-screen text, timed beat sheet |
| ig-caption | Caption, single ask, search terms, hashtags, linted |
| ig-carousel | Carousel cover and slide copy |
| ig-story | Story sequence and stickers |
| ig-human | Strips AI tells and scores a draft for sounding human |
| ig-viral | Finds reels working in your niche and builds a swipe file |
| ig-plan | Weekly posting and engagement plan |
| ig-profile | Scores a profile out of 100 and rewrites weak parts |
| ig-audit | Post-mortem on past posts |
| ig-repurpose | Turns long content into reels and carousels |
| ig-comment | Comments on other people's posts |
| ig-reply | Replies to comments on your posts |
| ig-dm | DMs, outreach and follow-ups |
| ig-subtitles | Burned-in captions from a video, script or SRT, kept inside the safe zone |
| ig-keyword-dm | "Comment KEYWORD, get it by DM" on the official API, as an n8n workflow |

## How content gets written

1. **Niche.** `ig-pov/niche-template.md` is copied to `~/.claude/instagram/niche.md` on first use. It holds the niche, the one audience, themes, enemies, the proof bank and search terms. Pre-filled for AEO / GEO / AI visibility. Edit it.
2. **POV.** `/ig-pov` turns a topic into a one-line stand inside that niche. No proof, no POV.
3. **PREP.** Reels, carousels and captions are built as Point, Reason, Example, Point. The Point is the POV.
4. **Copy pass.** The rules from the `copywriting` skill: one claim, specifics over adjectives, the So What chain, a verb-plus-benefit ask, no AI accent.
5. **Voice pass.** Every skill that writes copy applies Khadija's voice: `khadija-voice` if installed, otherwise the Instagram cut of it built into each skill and `ig-reel/voice-template.md`.
6. **Humanize.** `/ig-human` strips and scores before you see it.

## Tools that run

| Script | What it does | Needs |
|---|---|---|
| `ig-reel/hookscore.py`, `beats.py` | Score hooks, time scripts | Python 3 |
| `ig-carousel/render.py` | Slide copy to 1080x1350 PNGs | Chrome or Chromium |
| `ig-subtitles/subtitles.py` | Captions SRT, optional burn-in | `faster-whisper` to transcribe, `ffmpeg` to burn |
| `ig-audit/insights.py` | Post insights from the official API | `IG_ACCESS_TOKEN`, Business or Creator account |
| `ig-plan/calendar.py` | Content calendar CSV, opens in Google Sheets | Python 3 |
| `ig-keyword-dm/workflow.json` | Comment keyword to DM automation | n8n, Meta app with messaging access |
| `ig-human/humanize.py`, `detect.py` | Strip and score AI tells | Python 3 |

Nothing in this repo posts, follows, likes or logs in as you.

## Install

**Claude Code:** copy the `ig-*` folders into `~/.claude/skills/` (all projects) or `.claude/skills/` (one project).

**claude.ai:** zip one folder (for example `zip -r ig-reel.zip ig-reel`) and upload it under Settings > Capabilities > Skills. One zip per skill.

The Python helpers (`hookscore.py`, `beats.py`, `humanize.py`, `detect.py` and others) need Python 3 and no extra packages.

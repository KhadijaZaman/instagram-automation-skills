# Instagram automation skills

13 Claude skills for Instagram. Each folder is one skill with a `SKILL.md`.

| Skill | What it does |
|---|---|
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

## Install

**Claude Code:** copy the `ig-*` folders into `~/.claude/skills/` (all projects) or `.claude/skills/` (one project).

**claude.ai:** zip one folder (for example `zip -r ig-reel.zip ig-reel`) and upload it under Settings > Capabilities > Skills. One zip per skill.

The Python helpers (`hookscore.py`, `beats.py`, `humanize.py`, `detect.py` and others) need Python 3 and no extra packages.

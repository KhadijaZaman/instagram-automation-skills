# Instagram automation skills

14 Claude skills for Instagram. Each folder is one skill with a `SKILL.md`.

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

## How content gets written

1. **Niche.** `ig-pov/niche-template.md` is copied to `~/.claude/instagram/niche.md` on first use. It holds the niche, the one audience, themes, enemies, the proof bank and search terms. Pre-filled for AEO / GEO / AI visibility. Edit it.
2. **POV.** `/ig-pov` turns a topic into a one-line stand inside that niche. No proof, no POV.
3. **PREP.** Reels, carousels and captions are built as Point, Reason, Example, Point. The Point is the POV.
4. **Copy pass.** The rules from the `copywriting` skill: one claim, specifics over adjectives, the So What chain, a verb-plus-benefit ask, no AI accent.
5. **Humanize.** `/ig-human` strips and scores before you see it.

## Install

**Claude Code:** copy the `ig-*` folders into `~/.claude/skills/` (all projects) or `.claude/skills/` (one project).

**claude.ai:** zip one folder (for example `zip -r ig-reel.zip ig-reel`) and upload it under Settings > Capabilities > Skills. One zip per skill.

The Python helpers (`hookscore.py`, `beats.py`, `humanize.py`, `detect.py` and others) need Python 3 and no extra packages.

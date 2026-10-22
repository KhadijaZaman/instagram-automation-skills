---
name: ig-carousel
description: >-
  Build an Instagram carousel - the cover that earns the swipe, slide-by-slide
  copy, and the 1080x1350 files to upload. Use when the user says "carousel",
  "slides", "swipe post", "turn this into a carousel", or has a list-shaped or
  step-shaped idea that would die as a single image.
---

# ig-carousel

Carousels are the highest-dwell format on the grid, because a swipe is an
interaction and a scroll is not. They also get a second chance: Instagram can
show a carousel again starting from a later slide to someone who did not engage
the first time, so slide two has to stand on its own as well.

The format rewards one idea broken into steps. It punishes a caption cut into
pieces.

## When to use it instead of a Reel

Use a carousel when the idea has **sequence and needs to be re-read**: steps, a
framework with parts, a before and after, a list worth screenshotting. Use a
Reel when the idea has motion, a face, or a payoff that has to be seen
happening.

If the idea is one claim, it is neither. Hand it to `/ig-reel` and say so.

## Structure: PREP across the swipe

Read `~/.claude/instagram/niche.md` first. If the idea is a topic rather than
a claim, run `/ig-pov` and build on the PREP block it returns.

| PREP | Slides |
|---|---|
| **P** Point | Cover: the POV in 6 words or fewer |
| **R** Reason | Slide 2: what the enemy costs the reader |
| **E** Example | Slides 3 to N: the proof and the steps, one per slide |
| **P** Point | Recap and CTA: the Point restated, then one ask |

6 to 10 slides. The cap is 20 and 20 is almost always a book nobody finishes.
Under 5 and the swipe never starts.

```
1         COVER     the hook. 6 words or fewer, at a size that is legible in
                    the grid at thumbnail. One line of promise under it.
2         THE STAKE why this matters, in one sentence. This slide is also a
                    second cover, so it cannot be setup.
3 to N    ONE IDEA PER SLIDE. A headline of 3 to 7 words, at most 25 words
                    under it. If a slide needs a paragraph, it is two slides.
N+1       RECAP     the whole thing as a list. This is the screenshot slide.
LAST      CTA       one action. Save, comment a keyword, or follow. One.
```

## Slide copy rules

- **The cover is 80% of the result.** Six words. Big. Nothing on the deck saves
  a cover nobody swipes.
- **Design for the grid crop.** The profile grid crops to a portrait rectangle
  that is taller than it is wide, and the exact ratio has moved more than once.
  Build at 1080x1350 and keep the cover text well inside the middle, clear of
  the outer 120 pixels on every side, and the crop stops mattering.
- **Number the slides** (3/8). Completion goes up when people can see the end.
- **No slide is a paragraph.** If it cannot be said in 25 words, split it.
- **The recap slide is the one people screenshot and send.** Sends are the
  strongest signal you can earn. Make it standalone and readable with no
  context.
- **The handle on every slide**, small, bottom corner. Screenshots travel
  without you.
- **Alt text on the cover at minimum.** It is read by screen readers and by
  Instagram.

## Voice pass (Khadija's voice)

If the `khadija-voice` skill is installed, run it in polish mode on every line
the user will say or post, after the draft and before `/ig-human`. If it is
not, or if `~/.claude/instagram/voice.md` exists, apply these. They are the
Instagram cut of `khadija-voice`, Appendix A.

- **The voice:** a measured technical practitioner walking a peer through what
  she has been looking at. A coffee chat with someone who knows the field, not
  a guru, not a hype reel.
- **Open with something real:** a specific scene ("I spent last Tuesday inside
  our citation data"), a specific finding with its sample ("Across 1,200 SaaS
  pages we tracked..."), a named source and their concept, or a tension (two
  things that can't both be true). Never a topic opener, "it's no secret",
  "most people don't realize", or "3 years ago I was X".
- **Vary the rhythm.** Mix one long, flowing sentence with short ones. Never
  three short punchy lines in a row when spoken; that is the guru cadence.
  On-screen text cards can stay short.
- **Name the source.** "Koray Gubur calls this topical borders", not "experts
  say". Numbers are hers or marked `{{verify}}`.
- **Honest hedges are fine, weasel hedges are not.** "From what we're seeing",
  "across our dataset" yes. "Could potentially", "it's worth noting" no.
- **Close with substance.** "If you're seeing something different in your
  data, tell me" beats "Agree?". An ask is allowed when it delivers something
  real (comment a keyword, get the checklist). Never bare engagement bait.
- **No decorative emojis, no hype words** (game-changer, unlock, leverage,
  supercharge, seamless).
- **Default to low-risk stances** (methodological, observational,
  definitional). A direct contradiction like "Stop buying GEO" gets
  `[RISK: strong public stance, confirm before posting]`.

## Copy pass (from the copywriting skill)

If the `copywriting` skill is installed, run its edit mode on the draft:
message first, then structure, then lines. If it is not, apply these:

- **One claim.** The Point is the claim. Anything that argues a second one gets
  cut or becomes its own post.
- **Specific beats adjectives.** "$4,200" beats "a lot", "top 10" beats "high".
  No number? Ask for one or leave `{{your number}}`.
- **So What chain to the end.** Tactic, then result, then what the viewer gains
  in time, money or risk.
- **The ask is verb plus what they get.** "Comment AUDIT for the checklist",
  never "let me know your thoughts".
- **Kill the AI accent.** No em dashes, no "it's not X, it's Y", no "whether
  you're A or B", no tacked-on ", ensuring ...". `/ig-human` catches the rest.

## Building the files

Instagram wants 1080x1350 (4:5), JPEG or PNG, up to 20 items. `render.py` in
this folder builds them. It needs no Python packages, only a Chrome or
Chromium already on the machine (set `CHROME=/path/to/chrome` if it is not
found).

1. Write the approved copy to `slides.md`: one slide per block, blocks
   separated by a line of `---`, first line is the headline, lines starting
   with `- ` become list items. The first block is the cover.
2. Run it:

```bash
python3 render.py slides.md --out ./carousel --handle @yourhandle
```

3. Fix every WARN it prints (cover over 6 words, a slide over 25 words, an em
   dash) and re-run.

Colours and fonts come from `~/.claude/instagram/brand.json` if it exists:

```json
{"background": "#F7F5F0", "text": "#1A1A1A", "accent": "#2B59C3",
 "cover_background": "#1A1A1A", "cover_text": "#F7F5F0",
 "google_font": "Inter:wght@400;600;800", "handle": "@yourhandle"}
```

Type is 40px body, 72px headlines, 104px cover, all inside a 120px margin, so
the grid crop never cuts text. If the user has a brand skill, copy its colours
into `brand.json` rather than inventing a palette.

## Output

The slide-by-slide copy first, as a numbered list the user can read in ten
seconds and edit before anything is rendered. Then the **caption**, which for a
carousel is Job B in `/ig-caption`: the caption is doing work here, because the
cover has already used its six words.

Run both through `/ig-human`. Build the files only after the user approves the
copy.

```
CAROUSEL  ·  8 slides

1  COVER   THE $18,000 CLAUSE
           One line I now put in every contract.
2  STAKE   I approved the work. They asked for the money back nine days later.
3          WHAT IT SAYS
           Payment on delivery, not on approval.
...
7  RECAP   All four lines, in order.
8  CTA     Comment CONTRACT and I will send the full clause.

Caption: Job B, hook in line 1, one ask, 3 tags.
```

Nothing is uploaded. The user posts it.

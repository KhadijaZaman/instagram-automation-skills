---
name: ig-pov
description: >-
  Find the stand an Instagram post takes before anything gets written - the
  enemy, the cost, the better way and the proof - and lock it to the user's
  niche so every reel, carousel and caption argues one point of view. Use when
  the user has a topic but no angle, says "what's my take", "POV", "angle",
  "make this less generic", "niche this down", or before /ig-reel,
  /ig-carousel or /ig-caption when the idea is a topic rather than a claim.
---

# ig-pov

A topic is not a post. "SEO vs GEO" is a topic. "Stop buying GEO, fix your SEO
first" is a post, because it takes a side. This skill turns the first into the
second, inside the user's niche, before a single line of script is written.

It is the Instagram version of the POV framework in `khadija-voice`
(Appendix G). Same four steps, cut down to what fits in a 30-second Reel or an
8-slide carousel.

## Before you start: the niche file

Read `~/.claude/instagram/niche.md`. It holds the niche, the one audience, the
enemies already in play, the proof the user is allowed to use, and the words
the audience types into search. Every POV is checked against it.

If it does not exist, copy `niche-template.md` from this folder to
`~/.claude/instagram/niche.md`, show it to the user, and ask them to correct
it. It ships pre-filled for AEO, GEO and AI search visibility. Do not write a
POV until the user has confirmed the niche, because a POV for the wrong
audience is wasted work.

## The four steps

Ask only for what is missing. One batched question, not four rounds.

**1. Name the enemy.** A specific belief, habit or tactic the audience already
holds that the user thinks is wrong. Not a competitor by name. Not "bad
content". Pull from the enemy list in `niche.md` first; add new ones there when
they turn up.

**2. Show the cost.** What the enemy costs the audience in time, money, traffic
or trust. One concrete sentence. "They add FAQ schema to 200 pages and the
citation count doesn't move" beats "it wastes effort".

**3. Show the better way.** A two-column contrast where both sides are
concrete:

| What most people do | What to do instead |
|---|---|
| {enemy, as an action} | {better way, as an action} |

**4. Back it with proof.** One real thing from the proof bank in `niche.md`: a
number from the user's own data, a named brand observably cited in an AI
engine, a client result they are allowed to share, or a public source they can
name on camera. **No proof, no POV.** If there is none, say so, and either
downgrade to a Predictive or Methodological POV (below) or leave
`{{your proof}}` in place and flag it. Never invent one.

## Then compress it

Fill the formula, then cut it to one line:

> The root of {cost} is {enemy}. Most {audience} chase {outcome} through
> {enemy}. The better move is {better way}, because {reason}. That gets
> {outcome}, not {cost}.

One line, under 12 words, is the POV. It becomes the Point in PREP for
every format downstream.

## How hard to push

Default to the lower-risk moves. They still take a side.

| Move | Shape | Risk |
|---|---|---|
| Methodological | "Here's how we test X, and why most teams don't." | low |
| Observational | "In our data, the thing that predicts X isn't what people think." | low |
| Definitional | "What most people call X isn't X. Here's the difference." | low |
| Predictive | "X becomes the default within 18 months. Here's the signal." | low |
| Direct contradiction | "Most advice about X is wrong." | high |
| Industry critique | "Rebranding SEO as GEO is misleading clients." | high |

Mark anything high-risk with `[RISK: public stance, confirm before posting]`.
A strong POV filters the audience. It is not trying to win everyone.

## The PREP handoff

Every POV leaves this skill already shaped as PREP, so `/ig-reel`,
`/ig-carousel` and `/ig-caption` can build on it directly:

```
P  POINT     the one-line POV. This is the hook.
R  REASON    the cost, step 2. Why the audience should care.
E  EXAMPLE   the proof, step 4. One specific, checkable thing.
P  POINT     the POV again, in fewer words, plus the single ask.
```

## Niche checks before it ships

- **One audience.** The POV names or clearly implies who it is for, taken from
  `niche.md`. "Marketers" fails. "B2B SaaS content leads" passes.
- **In-lane.** It sits inside one of the 3 or 4 themes in `niche.md`. If not,
  say it is off-niche and ask whether to post it anyway.
- **Search words.** At least one phrase from the search-terms list in
  `niche.md` appears in the POV or the Reason, so `/ig-caption` and Instagram
  search have something to match.
- **Not repeated.** Check `~/.claude/instagram/pov.md`. If the same enemy was
  used in the last 14 days, pick another or change the angle.

## Copy rules (from the copywriting skill)

If the `copywriting` skill is installed, apply its line-level rules to the POV.
If not, these are the ones that matter here:

- One claim. Two claims is two posts.
- Specific beats adjectives. A number or a name in every POV that has one.
- Run the So What chain to the end: tactic, then result, then what the reader
  gains in time, money or risk.
- No em dashes, no "it's not X, it's Y", no "whether you're A or B".

## Output

```
POV READY
niche:      AEO / GEO for B2B SaaS marketing teams
enemy:      treating GEO as a separate channel from SEO
move:       Methodological (low risk)
POV:        "Stop buying GEO. Fix your SEO first."

P  Stop buying GEO. Fix your SEO first.
R  AI answers pull from pages search already trusts. Not findable, not quoted.
E  {{your proof: e.g. how many cited pages already ranked top 10}}
P  Fix the SEO. The citations follow. Comment AUDIT for the checklist.

proof:      MISSING - flagged, not invented
next:       /ig-reel or /ig-carousel with this PREP block
```

On "yes", append the date, enemy, move and POV line to
`~/.claude/instagram/pov.md` so the next run does not repeat it.

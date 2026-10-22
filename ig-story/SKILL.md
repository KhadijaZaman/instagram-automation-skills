---
name: ig-story
description: >-
  Write the day's Instagram Stories - the frame-by-frame sequence, which
  stickers to use where, and the one that moves people into the DMs. Use when
  the user says "stories", "what do I post on my story", "story sequence",
  "poll idea", "I have nothing to story about", or wants to sell something
  without making a post about it.
---

# ig-story

Stories are not a smaller feed. The feed is how strangers find you. Stories are
how the people who already follow you decide whether you are a person worth
buying from, and they are the only surface on Instagram where a tap turns into
a conversation in one move.

Nobody outside your followers sees these, so the job is completely different:
depth, not reach.

## The daily shape

Three to seven frames a day. Beyond about seven, the tap-forward rate climbs
and the last frames play to nobody, which is exactly where people put the ask.

```
1       THE OPEN     something happening today, with a face or a hand in it.
2-3     THE MIDDLE   the actual content: the process, the result, the mistake.
4       THE ASK      one sticker. Poll, question box, quiz or link.
5       THE CLOSE    the answer, the outcome, or tomorrow's setup.
```

Put the ask at frame 4, not frame 7. Completion drops with every tap and the
ask should be seen by the people who are still there.

## The stickers, and what each is actually for

| sticker | job | use when |
| --- | --- | --- |
| **Poll** | the cheapest tap there is | you want volume of response, not information |
| **Question box** | harvesting the exact words people use | you need content ideas or objections, verbatim |
| **Quiz** | teaching by letting them be wrong | there is a common misconception in the niche |
| **Slider** | vibe check | nothing important. Fun, low value |
| **Link** | the only clickable surface besides the bio | there is somewhere real to go |
| **Countdown** | a deadline people can subscribe to | a launch, a live, a close date |
| **Add yours** | reach beyond your followers, occasionally | the prompt is one anyone in the niche can answer |

The question box is the most undervalued one in the list. Every answer is a
caption, a Reel hook or a DM opener written in the audience's own words. Feed
them to `/ig-reel` as formula #16.

## Rules

- **A face or a hand in the first frame.** Text on a coloured background gets
  tapped through, and the first frame decides whether the rest get watched.
- **One idea per frame.** Reading a paragraph on a story is not a thing anyone
  does.
- **Keep text inside the middle.** On 1080x1920, nothing above y=250 or below
  y=1600. The profile row sits on top and the reply bar sits underneath.
- **Talk to one person.** "You" singular. Stories are the closest thing to a
  DM that is not one.
- **Do not repost your own feed post to stories with no comment.** It is the
  single most ignored frame on the platform. If you are pointing at a post, say
  what happened in the comments and why it is worth going back for.
- **Sell on stories, not in posts.** Three frames of context, one frame of
  offer, one frame of proof. That sequence sells more than a feed post about
  the same thing and costs you no reach.

## The DM funnel, done honestly

The sequence that works: a story that names a problem, a question box or a poll
that lets people say "that's me", and then a reply to each person who answered.
The conversation starts because they spoke first.

Automated keyword DM replies are a real, supported feature for professional
accounts, through Instagram's own tools and approved partners. Bulk DMing
people who did not interact is not, and it is what gets accounts restricted.
The rule is simple: **they act first, then you reply.**

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

## Output

The frames in order, each with what is on screen, what is said, and which
sticker, plus what to do with the answers:

```
STORIES  ·  Tuesday  ·  5 frames

1  [selfie, walking]      "Third refund request this year. Same reason."
2  [screen recording]     the clause, highlighted
3  [talking]              "Approval is a feeling. Delivery is a date."
4  [poll]                 "Have you been burned by a late approval?"  Yes / Not yet
5  [text on photo]        "Reply and I will send you the clause."

After: everyone who votes Yes gets a reply. That is the whole funnel.
```

Nothing is posted. The user posts it.

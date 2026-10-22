---
name: ig-repurpose
description: >-
  Turn one long asset - a YouTube video, podcast, livestream, newsletter, blog
  post or client call - into a week of reels and carousels. Use when the user
  says "repurpose this", "turn this into reels", "I have a video/podcast/
  transcript", "cut this up", or pastes something long and wants it on
  Instagram.
---

# ig-repurpose

One good long asset contains four to six posts. Most people extract one and
throw the rest away.

## Input

A transcript, an article, a newsletter, a script, a call summary, a livestream.
If the user gives a URL and this session has a transcript tool, use it;
otherwise ask them to paste. Read the whole thing before extracting anything.

If the source is a video the user owns, ask for the file too. A Reel built on
their own footage beats one built on their own words read again.

## Extract, do not summarise

A summary of a video is not a Reel. Nobody wants the summary. Go through the
asset and pull out the things that stand alone:

| pull | what it is |
| --- | --- |
| **Claims** | every sentence that would start an argument |
| **Numbers** | every figure, cost, duration, percentage |
| **Stories** | every moment with a person, a scene and a cost |
| **Mechanisms** | every "the way this actually works is..." |
| **Mistakes** | every admission of something that went wrong |
| **Lines** | every sentence already quotable as-is |

List what you found, with counts, before writing anything. If the asset yields
fewer than four items, it is thin, and four posts squeezed out of it will be
thin too. Say that.

## Then pick the format per extract

Not everything is a Reel.

- **Claim, mistake, story** to a Reel. They need a voice and a face.
- **Mechanism, numbered list** to a carousel. They need to be re-read.
- **A quotable line** to a story frame, not a post.

## Then build the week

Each extract becomes one post and each post stands completely on its own. The
viewer has not seen the source and never will. Never write "as I said in my
latest video". The post is the thing.

Assign a hook formula from `ig-reel/hooks.json` to each and vary them. Five
posts from one source with the same hook shape reads as a content mill, because
it is one.

If the source is the user's own video, **use the actual footage**. The clip
where they said the thing, with the real reaction in it, beats a re-record
every time. Cut on the sentence, not on the breath.

Order across the week so the strongest claim goes first, the story lands
midweek, and the mechanism goes last, when the people who liked the earlier
ones are watching for it.

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

```
SOURCE: "Why we killed discovery calls" (42 min podcast, 8,900 words)

FOUND  5 claims, 9 numbers, 3 stories, 4 mechanisms, 2 mistakes, 7 quotable lines

WEEK
TUE  REEL      #2  Negative Command  Stop running discovery calls
                                     use the 14:20 clip, he laughs at the end
WED  CAROUSEL  Job B caption         The 4-question form that replaced the call
FRI  REEL      #21 Mid-Sentence      "...and he asked for a refund nine days later"
SUN  REEL      #5  Time Collapse     Six hours a week back, one deleted link

Say "write Tuesday" and I will draft it.
```

Then draft on request, one at a time, each through `/ig-reel` and `/ig-human`.
Do not dump four finished scripts at once. They will all sound the same and the
user will shoot none of them.

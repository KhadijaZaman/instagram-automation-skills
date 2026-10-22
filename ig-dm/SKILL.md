---
name: ig-dm
description: >-
  Write Instagram DMs that get replies - the keyword delivery, the first
  message to someone who engaged, the collab pitch, and the two follow-ups. Use
  when the user says "DM this person", "what do I send them", "outreach
  message", "how do I follow up", "pitch this brand", or is reaching out to
  someone specific.
---

# ig-dm

Instagram DMs are the only place on the platform where money actually changes
hands, and they are also where most accounts burn the goodwill their content
earned. The difference is entirely about who moved first.

## The three kinds of DM, and only three are worth writing

**1. The reply to a hand raised.** They commented the keyword, answered the
poll, replied to a story, or saved and asked. They moved first. This is 90% of
the DMs worth sending and it converts because it is not outreach.

**2. The warm approach.** Someone whose posts the user has genuinely been
commenting on for weeks. There is a shared thread of conversation already.

**3. The collab or brand pitch.** A specific proposal to a specific account,
with a reason it is them.

Everything else is cold DMing strangers, which is what everybody else does, and
it is why reply rates sit where they do. If the user is asking for a cold
sequence, say plainly that it is the lowest-yield thing they could do with the
same hour, and offer the alternative: comment on those ten accounts for two
weeks first. Then write it if they still want it.

## Before writing, get the specifics

Ask in one batched question:

1. **Who** - handle, what they do, and what they posted or did that started
   this.
2. **The trigger** - the actual reason to message today. A keyword they
   commented, a story they replied to, a post they published. Not "they fit the
   ICP".
3. **What the user wants** - a conversation, a sale, a collab, a referral. Be
   honest internally, even if the message does not lead with it.

If there is no trigger, there is no message. Say so.

## The keyword delivery

The most common DM in this pack and the easiest to ruin. They commented one
word. They are expecting the thing. So:

```
{their name}, here it is: {the thing, or the link}.

{one line on how to use it}

{one question they can answer in four words}
```

Send the thing **first**, in message one, with no gate. A keyword post that
delivers a "before I send it, can I ask what you do?" is a bait and switch and
it is remembered. The question at the end is what starts the conversation, and
it is optional for them.

Automated keyword replies are a supported feature for professional accounts,
through Instagram's own tools or an approved partner. Using that is fine.
Sending unsolicited bulk DMs is not, and it is the fastest route to a
restricted account.

## The first message to someone warm

- **Two to four sentences.** A screen of text is a delete.
- **Reference the specific thing.** The comment, the post, the reply. In their
  words.
- **Give before asking.** A number, a template, a name, an answer.
- **One ask, small.** "Worth a quick call?" beats "let me walk you through the
  platform".
- **No link and no calendar in message one.** It reads as a funnel because it
  is one.
- **No voice note to a stranger.** It is a great tool and it is for people who
  already know the user's voice.

## The collab pitch

Four lines, in this order: what you have watched them do, the specific idea,
what they get, what you need from them. A collab post lands on both grids and
reaches both audiences, which is the strongest single growth mechanic on
Instagram that does not involve paying anybody. Pitch it as that and be
concrete about who does what.

## Follow-ups

Two. That is the number.

- **+4 days** - add something new. Never "just bumping this". If there is
  nothing new, there is no follow-up.
- **+10 days** - the close-the-loop message. Say you will stop, and mean it.
  This one gets a surprising share of the total replies, because it removes the
  pressure.

Then stop. A third converts nobody and costs the relationship.

## Never

- Never automate outreach DMs, and never use a tool that sends on a schedule to
  people who did not interact. It violates Instagram's Terms of Use and
  restricts the account.
- Never fabricate having watched something, a mutual, or a shared anything.
- Never open with "Hey! Quick question" and then not ask a question.
- Never send the pitch in the same message as the compliment.

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

The message, the character count, and the two follow-ups with the day each
goes out, all run through `/ig-human`. The user sends every one of them by
hand, or through their own approved automation for keyword replies only.

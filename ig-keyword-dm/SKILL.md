---
name: ig-keyword-dm
description: >-
  Set up the "comment KEYWORD and I'll DM it to you" automation on the user's
  own Instagram account, through Meta's official API and an n8n workflow - the
  keyword map, the DM written in the user's voice, the public reply, and the
  setup steps. Use when the user says "auto DM", "comment to DM", "ManyChat",
  "send the link when people comment", "keyword automation", or ends a Reel
  with "comment X".
---

# ig-keyword-dm

A Reel that ends "comment AUDIT for the checklist" makes a promise. If the DM
arrives three days later, the promise is broken. This sets up the delivery so
it lands in seconds, on the official API, with words the user would actually
send.

It only ever answers people who commented on the user's own posts. It never
messages anyone cold, never follows, never likes, never logs in as the user.

## Two ways to run it

**ManyChat (default, recommended).** ManyChat is an official Meta partner, so
there is no Meta app, no App Review and no webhook to host. The skill's job is
the keyword map and the words; ManyChat delivers them.

**n8n (`workflow.json`).** Only if the user wants no third-party tool. Needs
a Meta app with messaging Advanced Access. Never run both: Instagram allows
one private reply per comment, and two systems answering the same comment
means one of them fails or the person gets two DMs.

## ManyChat setup (about 20 minutes per keyword)

1. manychat.com, sign up with the Facebook login that manages the Instagram
   account, connect Instagram (Business or Creator). Allow message access in
   the Instagram app: Settings > Messages and story replies > Message
   controls > Connected tools > Allow access to messages.
2. Automation > New automation > trigger **"User comments on your Post or
   Reel"**. Choose "any post" or the specific Reel, and set **keyword
   contains** `AUDIT` (add lowercase and common typos as extra keywords).
3. Turn on **public reply to the comment** with 2 or 3 variations of the
   short reply below, so Instagram does not see one sentence repeated.
4. Add a **Send Message** step with the DM below. Put the link on a button
   or in line one.
5. Optional follow-up 24 hours later only if they clicked nothing: one line,
   not a sales pitch.
6. Test from a second account. Then set it live.

Do not add an "ask for a follow before sending" gate unless the user asks
for one. It reads as engagement bait in this voice, and it delays the thing
the Reel promised.

## What is in this folder (n8n alternative)

- `workflow.json` - an n8n workflow. Import it, edit one block, connect one
  credential, activate.
  - **GET webhook** answers Meta's one-time verification.
  - **POST webhook** receives each new comment.
  - **Match keyword** checks the first word against the keyword map and skips
    the user's own comments.
  - **Send private reply** DMs the commenter through `POST /me/messages` with
    `recipient.comment_id`.
  - **Public reply** answers under the comment so others see it was sent.

## Write the messages first

Before touching n8n, write the DM and the public reply for each keyword.

1. Run `/ig-dm` in keyword-delivery mode for the thing being sent.
2. Apply the voice pass (below). Then `/ig-human`.
3. ManyChat: paste the DM into the Send Message step and the replies into
   the public reply variations. n8n: paste into the `KEYWORDS` block in the
   **Match keyword** node.

**The voice pass for an automated DM.** It is still the user talking:
- Deliver first. The link is in line one, not after a greeting.
- One sentence on what it is and where it came from, in the user's own terms
  ("the same list we work through at Wellows").
- Close with a substantive invitation, not bait: "If something in it doesn't
  match what you're seeing in your data, reply here." Never "Let me know if you
  have any questions!" and never a sales pitch in the first message.
- No emojis, no exclamation marks, no "Hey there!".
- The public reply is 3 to 6 words. Give ManyChat 2 or 3 variations:
  "Sent it to your DMs.", "Check your DMs.", "Just sent it over."
- ManyChat buttons: label them with what they get ("Open the checklist"),
  never "Click here".

## n8n setup (about an hour, once)

1. **Professional account.** The Instagram account must be Business or Creator.
2. **Meta app.** At developers.facebook.com create an app, add the Instagram
   product with **Instagram Login**, and request
   `instagram_business_basic`, `instagram_business_manage_comments` and
   `instagram_business_manage_messages`. Generate a long-lived token.
   - While the app is in development mode it only reaches people who have a
     role on the app. To DM real commenters it needs **Advanced Access**
     through Meta's App Review. Plan for that.
3. **n8n.** Import `workflow.json`. Create a **Header Auth** credential named
   `Instagram token` with header `Authorization` and value `Bearer <token>`,
   and select it on both HTTP nodes.
4. **Edit two code nodes.** In **Check verify token**, set `VERIFY_TOKEN` to a
   long random string. In **Match keyword**, set `MY_IG_USER_ID` and the
   `KEYWORDS` map.
5. **Activate**, copy the production webhook URL, and in the Meta app's
   Webhooks settings subscribe that URL to the `comments` field with the same
   verify token.
6. **Test** from a second account that has a role on the app: comment the
   keyword, check the DM arrives, check the public reply.

## Limits that come from Instagram, not from the workflow

- One private reply per comment, and only within 7 days of the comment.
- After a private reply, the conversation only continues if the person
  replies. That is the point: the next message is a real conversation, handled
  by `/ig-dm`, by hand.
- Messaging rate limits apply per account. A Reel that gets thousands of
  keyword comments in an hour will queue; nothing to do about that.

## Output

```
KEYWORD DM READY
keywords:   AUDIT -> GEO checklist link
dm:         312 characters, link in line 1, voice pass done, human 81 PASS
reply:      "Sent it to your DMs."
runs on:    ManyChat, trigger "comments on Post or Reel", keyword contains AUDIT
public:     3 reply variations
next:       paste into ManyChat, test from a second account, set live
```

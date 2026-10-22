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

## What is in this folder

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
3. Paste the result into the `KEYWORDS` block in the **Match keyword** node.

**The voice pass for an automated DM.** It is still the user talking:
- Deliver first. The link is in line one, not after a greeting.
- One sentence on what it is and where it came from, in the user's own terms
  ("the same list we work through at Wellows").
- Close with a substantive invitation, not bait: "If something in it doesn't
  match what you're seeing in your data, reply here." Never "Let me know if you
  have any questions!" and never a sales pitch in the first message.
- No emojis, no exclamation marks, no "Hey there!".
- The public reply is 3 to 6 words. "Sent it to your DMs." is enough.

## Setup (about an hour, once)

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
workflow:   workflow.json, edit 2 code nodes, 1 credential
blocked on: Meta Advanced Access for instagram_business_manage_messages
```

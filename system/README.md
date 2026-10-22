# The Instagram system

The skills in this repo, wired together so the account runs itself, with one
human gate: nothing posts until Khadija marks it `approved`.

## How it runs

| When (PKT) | Who | What |
|---|---|---|
| Monday 08:47 | Claude scheduled task (`weekly.md`) | Pull insights, analyse, plan the week, draft every post into the sheet as `review`. Carousels are rendered and uploaded. |
| Monday, 15 min | Khadija | Read the Posts tab, edit, set `approved`. Record Reels and paste the video link. |
| Every 15 min | n8n "IG Publisher" | Posts every `approved` row whose date and time have passed. Sends `approved` replies. Writes back `posted` / `failed`. |
| Daily 17:52 | Claude scheduled task (`daily-replies.md`) | Drafts replies to new comments into the Replies tab as `draft`. |
| Always | n8n "IG Comment keyword to DM" | Comment the keyword, get the DM, in seconds. |

The control panel is one Google Sheet:
[Instagram content calendar](https://docs.google.com/spreadsheets/d/1ARiXXigTeGEHhrLYptkGRec0JJAmgDw165fMRLeKjeA/edit)
with tabs Posts, Replies, Analytics and How it works.

## Files

| File | Job |
|---|---|
| `weekly.md` | Instructions for the Monday scheduled run |
| `daily-replies.md` | Instructions for the daily reply-drafting run |
| `bootstrap.sh` | Installs the skills and state into a fresh session |
| `upload.py` | Uploads slides or a Reel to Cloudinary, prints public URLs |
| `comments.py` | Fetches new, unanswered comments (read-only) |
| `state/niche.md`, `state/voice.md` | Niche profile and on-camera voice. Edit these here; every run reads them. |
| `n8n/` | Source of the two n8n workflows |

## Setup checklist (once)

1. **Meta app.** Instagram professional account (Business or Creator).
   developers.facebook.com: create an app, add Instagram with Instagram
   Login, permissions `instagram_business_basic`,
   `instagram_business_content_publish`,
   `instagram_business_manage_insights`,
   `instagram_business_manage_comments`,
   `instagram_business_manage_messages`. Generate a long-lived token.
   Messaging people outside the app's roles needs Advanced Access (App Review).
2. **Cloudinary.** Free account. Copy the `CLOUDINARY_URL` from the dashboard.
3. **Claude cloud environment.** Add `IG_ACCESS_TOKEN` and `CLOUDINARY_URL`
   as secrets in the environment settings. Never paste them in chat or commit
   them.
4. **n8n.** Create a Header Auth credential "Instagram token"
   (`Authorization: Bearer <token>`). In both workflows, select it on the
   HTTP nodes and select your Google Sheets account on the sheet nodes. Edit
   the keyword map. Activate.
5. **Meta webhook.** Subscribe the keyword-DM workflow's production URL to the
   `comments` field.
6. **Proof bank.** Fill the `{{...}}` blanks in `state/niche.md` with numbers
   you are willing to say in public.

Long-lived Instagram tokens expire after 60 days. Refresh before then, or
the Monday run reports "no token" and n8n starts failing.

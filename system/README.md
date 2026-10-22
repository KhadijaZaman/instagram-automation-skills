# The Instagram system

The skills in this repo, wired together so the account runs itself, with one
human gate: nothing posts until Khadija marks it `approved`.

## How it runs

| When (PKT) | Who | What |
|---|---|---|
| Monday 08:47 | Claude scheduled task (`weekly.md`) | Pull insights, analyse, plan the week, draft every post into the sheet as `review`. Carousels are rendered and uploaded. |
| Monday, 15 min | Khadija | Read the Posts tab, edit, set `approved`. Record Reels and paste the video link. |
| Hourly 18:13 to 22:13 | Claude scheduled task (`publish-run.md`) | Posts every `approved` row whose date and time have passed, via `publish.py`. Sends `approved` replies. Writes back `posted` / `failed`. |
| Daily 17:52 | Claude scheduled task (`daily-replies.md`) | Drafts replies to new comments into the Replies tab as `draft`. |
| Any time | Khadija + Meta AI | See a reel worth learning from, get Meta AI's breakdown, paste it into the Inspiration tab. Monday's run turns it into ideas. |
| Always | ManyChat | Comment the keyword, get the DM, in seconds. Copy written with `/ig-keyword-dm`. |

The control panel is one Google Sheet:
[Instagram content calendar](https://docs.google.com/spreadsheets/d/1ARiXXigTeGEHhrLYptkGRec0JJAmgDw165fMRLeKjeA/edit)
with tabs Posts, Replies, Analytics, Inspiration and How it works. No n8n.

## Files

| File | Job |
|---|---|
| `weekly.md` | Instructions for the Monday scheduled run |
| `daily-replies.md` | Instructions for the daily reply-drafting run |
| `bootstrap.sh` | Installs the skills and state into a fresh session |
| `upload.py` | Uploads slides or a Reel to Cloudinary, prints public URLs |
| `comments.py` | Fetches new, unanswered comments (read-only) |
| `state/niche.md`, `state/voice.md` | Niche profile and on-camera voice. Edit these here; every run reads them. |
| `publish-run.md` | Instructions for the hourly publish run |
| `publish.py` | Publishes approved posts and replies through the official API |

## Setup checklist (once)

1. **Meta app.** Instagram professional account (Business or Creator).
   developers.facebook.com: create an app, add Instagram with Instagram
   Login, permissions `instagram_business_basic`,
   `instagram_business_content_publish`,
   `instagram_business_manage_insights`,
   `instagram_business_manage_comments`. Generate a long-lived token.
   (No messaging permission needed: ManyChat sends the DMs.)
2. **Cloudinary.** Free account. Copy the `CLOUDINARY_URL` from the dashboard.
3. **Claude cloud environment.** Add `IG_ACCESS_TOKEN` and `CLOUDINARY_URL`
   as secrets in the environment settings. Never paste them in chat or commit
   them.
4. **Scheduled tasks.** In claude.ai, add the Google Sheets connector to all
   three scheduled tasks (weekly, publish, daily replies), then turn on the
   publish and daily ones.
5. **ManyChat.** Connect Instagram, build one automation per keyword with
   the copy from `/ig-keyword-dm`. Do not also run the n8n keyword workflow in `ig-keyword-dm`.
6. **Proof bank.** Fill the `{{...}}` blanks in `state/niche.md` with numbers
   you are willing to say in public.

Long-lived Instagram tokens expire after 60 days. Refresh before then, or
the Monday run reports "no token" and publishing stops.

## Meta AI prompt for the Inspiration tab

Ask Meta AI inside Instagram, on any reel, then paste the answer with the link:

```
Break down this reel:
1. The exact first line spoken, and the on-screen text in the first 2 seconds
2. Length in seconds and number of cuts
3. Structure, one line per section
4. The single claim it makes
5. The ask at the end
6. Views, likes and comments shown
```

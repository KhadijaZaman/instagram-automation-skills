# Hourly publish run (18:13 to 22:13 PKT)

Unattended. Publish only rows Khadija marked `approved`. Never approve,
edit, or write a caption yourself.

Sheet: `1ARiXXigTeGEHhrLYptkGRec0JJAmgDw165fMRLeKjeA`. Timezone Asia/Karachi.

1. If IG_ACCESS_TOKEN is not set, stop: "No token, nothing published."
2. If no `mcp__Google_Sheets__*` tools are available, stop: "Sheets
   connector missing on this scheduled task, nothing published." Never
   publish without being able to mark the row afterwards, or it would post
   twice next hour.
3. Read Posts. Due = status `approved` AND media_urls not empty AND date+time
   (PKT) is now or earlier. Read Replies. Due = status `approved` AND bucket
   is not KEYWORD.
4. If nothing is due, stop: "Nothing due." (This is the normal case.)
5. BEFORE publishing, set each due Posts row's status to `publishing` so a
   parallel or retried run can't post it twice.
6. Write `due.json` (see `system/publish.py --help`) with each due post's id,
   format, caption, media_urls, and each due reply's comment_id, draft_reply.
   Run `python3 system/publish.py due.json --out results.json`.
7. Write results back by id / comment_id:
   - Posts: status `posted` + ig_media_id + permalink, or `failed` + error.
     If the error says "still processing", set status back to `approved` so
     the next hour retries.
   - Replies: status `sent` + sent_at, or `failed` + error.
8. Final message, 3 lines max: what posted (with permalinks), what failed and
   why.

# Daily reply drafts (17:52 PKT)

Unattended run. Draft replies only. Never send anything: n8n sends rows that
Khadija marks `approved` in the Replies tab.

Sheet: `1ARiXXigTeGEHhrLYptkGRec0JJAmgDw165fMRLeKjeA`, tab Replies.

1. `bash system/bootstrap.sh`. If IG_ACCESS_TOKEN is missing, stop and say so
   in one line.
2. Read the Replies tab. Write every existing comment_id to `known.txt`.
3. `python3 system/comments.py --posts 10 --skip known.txt --out comments.tsv`
   If 0 new comments, stop: "No new comments."
4. Run `/ig-reply` on the new comments. It sorts them into KEYWORD, LEAD,
   SUBSTANCE, QUESTION, SUPPORT, NOISE and drafts replies in Khadija's voice
   (voice pass, then `/ig-human`).
   - KEYWORD: no draft (the keyword DM automation handles it). status `skip`,
     note "keyword, handled by n8n".
   - NOISE: no draft, status `skip`.
   - QUESTION: draft the reply AND add "reel idea: <question>" to notes.
5. Append one row per comment to Replies: comment_id, post_permalink,
   username, comment, bucket, draft_reply, status `draft` (or `skip`).
6. Final message, 3 lines max: how many drafted, any LEAD worth a DM by hand,
   any reel ideas.

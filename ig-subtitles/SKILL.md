---
name: ig-subtitles
description: >-
  Turn a Reel's audio, script or rough SRT into burned-in captions - short
  cards of 3 to 5 words, timed, kept inside the safe zone - and optionally burn
  them into the video with ffmpeg. Use when the user says "captions",
  "subtitles", "SRT", "add text to my reel", "people watch on mute", or has a
  recorded Reel and needs the words on screen.
---

# ig-subtitles

Most people watch a Reel muted first. If the words are not on screen, the
body of the Reel does not exist for them. This skill puts the user's own words
on screen, in short readable cards, without covering anything the interface
covers.

```bash
python3 subtitles.py --video reel.mp4 --clean --burn reel.mp4   # transcribe, tidy, burn in
python3 subtitles.py --script script.txt --wpm 165              # before shooting: time the script
python3 subtitles.py --srt capcut.srt --words 4                 # re-chunk someone else's SRT
```

Transcribing needs `pip install faster-whisper`. Burning needs `ffmpeg`. With
neither, use `--script` or `--srt` and import the SRT into CapCut, Edits or
Instagram's own editor.

## The voice rule

**Captions are the user's words, verbatim.** This is the one skill in the pack
that does not rewrite. Do not polish, do not apply the voice pass, do not
"improve" a line. `--clean` only removes um, uh, erm and doubled words. If a
line was said badly, the fix is a re-take or a script edit, not a caption that
disagrees with the audio.

The only exceptions, which the script handles:
- an em dash in the transcript becomes a comma
- a technical term the transcriber got wrong (Gemini, Perplexity, GEO, AEO,
  schema, SERP) gets corrected by hand. Check every one against
  `~/.claude/instagram/niche.md`, search terms list, before burning.

## Card rules

- **3 to 5 words per card.** Default is 4. Cards break early at a full stop so
  one card never carries the end of one sentence and the start of the next.
- **Inside the safe zone.** On 1080x1920 the cards sit above y=1440 and clear
  of the right 230px, so the caption, the action rail and the audio strip
  never cover them. The burned style is white, bold, black outline.
- **Do not double up.** If the Reel already has on-screen text cards from
  `/ig-reel`, burned captions go below them, never on top.
- **Hook card stays separate.** The hook's on-screen line from `/ig-reel` is
  its own card at frame 1. Captions start with the second sentence.

## Loop

1. Get the source: video, script or SRT.
2. Run `subtitles.py`. Use `--clean` on any transcription.
3. Read the SRT. Fix niche terms the transcriber misheard. Nothing else.
4. Burn with `--burn`, or hand the SRT over for the user's editor.
5. Print the receipt:

```
CAPTIONS READY
source:     reel.mp4, transcribed
cards:      26 at max 4 words, 34.3s
fixed:      "jim and eye" -> "Gemini" (line 14)
burned:     reel-captioned.mp4
```

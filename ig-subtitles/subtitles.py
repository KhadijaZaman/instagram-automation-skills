#!/usr/bin/env python3
"""Make burned-in captions for a Reel: short cards, timed, inside the safe zone.

Three ways in:
    python3 subtitles.py --video reel.mp4                 # transcribe the audio (needs faster-whisper)
    python3 subtitles.py --script script.txt --wpm 165    # no audio yet: time the script itself
    python3 subtitles.py --srt raw.srt                    # re-chunk an SRT from CapCut, Descript, etc.

Options:
    --words 4          words per caption card (3 to 5 reads best on a phone)
    --clean            drop um, uh, erm and doubled words from a transcript
    --out reel.srt     where to write the SRT (default: captions.srt)
    --burn reel.mp4    also burn the captions into a copy of the video with ffmpeg

The captions keep the speaker's own words. Nothing is rewritten.
"""

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

FILLERS = {"um", "uh", "erm", "er", "ah", "hmm", "mm"}

# 1080x1920 safe zone: keep clear of the bottom 480px (caption + audio strip)
# and the right 230px (action rail). MarginV is measured in a 288-high
# script space by libass, so 480/1920*288 = 72, plus breathing room.
FORCE_STYLE = ("FontName=Inter,FontSize=13,Bold=1,PrimaryColour=&H00FFFFFF,"
               "OutlineColour=&H00000000,BorderStyle=1,Outline=2,Shadow=0,"
               "Alignment=2,MarginV=90,MarginL=20,MarginR=40")


def ts(seconds):
    ms = int(round(seconds * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def parse_ts(text):
    h, m, rest = text.strip().split(":")
    s, ms = rest.replace(".", ",").split(",")
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000


def words_from_video(path):
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        sys.exit("Transcribing needs faster-whisper: pip install faster-whisper\n"
                 "Or export an SRT from CapCut / Descript and use --srt.")
    model = WhisperModel("small", compute_type="int8")
    segments, _ = model.transcribe(str(path), word_timestamps=True, vad_filter=True)
    return [(w.word.strip(), w.start, w.end) for seg in segments for w in seg.words]


def words_from_script(path, wpm):
    per_word = 60.0 / wpm
    words, t = [], 0.0
    for line in Path(path).read_text().splitlines():
        for w in line.split():
            words.append((w, t, t + per_word))
            t += per_word
        t += per_word * 0.6  # a breath between lines
    return words


def words_from_srt(path):
    words = []
    blocks = re.split(r"\n\s*\n", Path(path).read_text().strip())
    for block in blocks:
        lines = block.strip().splitlines()
        timing = next((l for l in lines if "-->" in l), None)
        if not timing:
            continue
        start, end = (parse_ts(x) for x in timing.split("-->"))
        text = " ".join(lines[lines.index(timing) + 1:]).split()
        if not text:
            continue
        step = (end - start) / len(text)
        words += [(w, start + i * step, start + (i + 1) * step) for i, w in enumerate(text)]
    return words


def clean(words):
    out = []
    for w in words:
        bare = re.sub(r"[^\w']", "", w[0]).lower()
        if bare in FILLERS:
            continue
        if out and bare and bare == re.sub(r"[^\w']", "", out[-1][0]).lower():
            continue
        out.append(w)
    return out


def chunk(words, size):
    cards, current = [], []
    for w in words:
        current.append(w)
        ends_sentence = w[0].endswith((".", "?", "!"))
        if len(current) >= size or ends_sentence:
            cards.append(current)
            current = []
    if current:
        cards.append(current)
    return cards


def to_srt(cards):
    out = []
    for i, card in enumerate(cards, start=1):
        text = " ".join(w[0] for w in card).replace("—", ",")
        out.append(f"{i}\n{ts(card[0][1])} --> {ts(card[-1][2])}\n{text}\n")
    return "\n".join(out)


def burn(video, srt):
    if not shutil.which("ffmpeg"):
        print("ffmpeg not found. Install it, or import the SRT into CapCut / Instagram's editor.")
        return
    out = Path(video).with_name(Path(video).stem + "-captioned.mp4")
    vf = f"subtitles={srt}:force_style='{FORCE_STYLE}'"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(video), "-vf", vf,
                    "-c:a", "copy", str(out)], check=True)
    print(f"burned:     {out}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--video", help="video or audio file to transcribe")
    src.add_argument("--script", help="script text file, timed by speaking rate")
    src.add_argument("--srt", help="existing SRT to re-chunk")
    ap.add_argument("--wpm", type=int, default=165)
    ap.add_argument("--words", type=int, default=4)
    ap.add_argument("--clean", action="store_true")
    ap.add_argument("--out", default="captions.srt")
    ap.add_argument("--burn", help="video to burn the captions into")
    args = ap.parse_args()

    if args.video:
        words = words_from_video(args.video)
    elif args.script:
        words = words_from_script(args.script, args.wpm)
    else:
        words = words_from_srt(args.srt)
    if args.clean:
        words = clean(words)
    if not words:
        sys.exit("No words found.")

    cards = chunk(words, args.words)
    Path(args.out).write_text(to_srt(cards))
    longest = max(len(c) for c in cards)
    print(f"CAPTIONS READY  {len(cards)} cards  {words[-1][2]:.1f}s  max {longest} words/card")
    print(f"srt:        {args.out}")
    if args.burn:
        burn(args.burn, args.out)


if __name__ == "__main__":
    main()

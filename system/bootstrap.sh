#!/usr/bin/env bash
# Install the skills and the user's state into a fresh session.
# Run from the repo root: bash system/bootstrap.sh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$HOME/.claude/skills" "$HOME/.claude/instagram"
cp -r "$ROOT"/ig-* "$HOME/.claude/skills/"
for f in niche voice; do
  cp "$ROOT/system/state/$f.md" "$HOME/.claude/instagram/$f.md"
done
[ -f "$ROOT/system/state/brand.json" ] && cp "$ROOT/system/state/brand.json" "$HOME/.claude/instagram/brand.json"
echo "skills: $(ls -d "$HOME"/.claude/skills/ig-* | wc -l)  state: niche.md voice.md"
echo "IG_ACCESS_TOKEN: $([ -n "${IG_ACCESS_TOKEN:-}" ] && echo set || echo MISSING)"
echo "CLOUDINARY_URL:  $([ -n "${CLOUDINARY_URL:-}" ] && echo set || echo MISSING)"

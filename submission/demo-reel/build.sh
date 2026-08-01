#!/usr/bin/env bash
# Rebuild Stage Manager demo reel (TTS + stills → mp4). Requires espeak-ng + ffmpeg + pillow.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
REEL="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT/skills/customer-success-voice-signal"
npm run signal -- --fixture stuck_support_acme.json --dry-run > "$REEL/dress-rehearsal.txt"
cd "$REEL"
python3 "$REEL/build_reel.py"
echo "Output: $REEL/stage-manager-demo.mp4"

#!/usr/bin/env bash
# Rebuild Stage Manager demo reel from the agent screen recording + TTS cards.
set -euo pipefail
REEL="$(cd "$(dirname "$0")" && pwd)"
python3 "$REEL/build_reel.py"
echo "Output: $REEL/stage-manager-demo.mp4"
echo "GIF:    $REEL/stage-manager-loop.gif"

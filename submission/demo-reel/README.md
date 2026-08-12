# Demo reel — Stage Manager

## What you get

- [`stage-manager-demo.mp4`](stage-manager-demo.mp4) — ~65s
- [`stage-manager-loop.gif`](stage-manager-loop.gif) — CLI loop for README + site

## What was recorded here (this machine)

1. **Real CLI screen recording** on the cloud desktop (`xfce4-terminal`, JetBrains Mono): `--last` (live prompt book, option 1), dress rehearsal, `--list`, `apply-action --dry-run`.
2. **Title / value / end cards** with espeak-ng VO from [`../video-script.md`](../video-script.md).
3. **Call beat** reconstructed from the **2026-08-12 live CALL-E transcript** (Assaf, stage code 4821, “1”). Caption on screen: handset audio lives on the owner’s phone.

Slack does not fire. Customer was never called.

## Honest limits

- Voice is **espeak-ng** (robotic). Swap in a human mic later if you want polish — the CLI take does not need to be re-shot.
- The physical phone ring / earpiece audio cannot be captured from this VM. The live call already happened; this reel uses that transcript instead of pretending we held the handset.
- No talking-head. Intentional.

## Rebuild

Needs: `espeak-ng`, `ffmpeg`, `python3-pillow`, plus the CLI recording at `/opt/cursor/artifacts/stage-manager-cli-demo.mp4` (or re-run `record_cli.sh` on a desktop with `DISPLAY`).

```bash
bash submission/demo-reel/build.sh
```

On-camera CLI (fullscreen terminal):

```bash
DISPLAY=:1 xfce4-terminal --fullscreen --hide-menubar --font="JetBrains Mono 18" \
  --color-bg="#0c0a08" --color-text="#f4efe6" \
  --command="bash submission/demo-reel/record_cli.sh"
```

## Pre-submit

Tick video + GIF on [`../PRE-SUBMIT.md`](../PRE-SUBMIT.md) **together with** the MVF survey. MVF is not part of the reel.

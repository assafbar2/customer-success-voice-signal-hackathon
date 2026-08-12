# Demo reel — Stage Manager

## What you get

- [`stage-manager-demo.mp4`](stage-manager-demo.mp4) — ~76s first-cut (TTS + stills, real CLI captures)
- [`stage-manager-loop.gif`](stage-manager-loop.gif) — README / site loop (`POST /cue` + dress rehearsal)

## Honest limits

- Voice is **espeak-ng** (robotic). Fine as a Devpost placeholder; re-record VO for polish.
- Curtain-up phone ring is **reconstructed in frames**. This environment has no `CALLE_API_KEY` / real CS phone / Slack webhook, so we cannot capture `curl → ring → one → Slack lands`.
- Live ladder (real rings, including voicemail/unclear) remains in [`../../research/calle-api-notes.md`](../../research/calle-api-notes.md).

## Rebuild

```bash
# deps: espeak-ng, ffmpeg, python3-pillow
sudo apt-get install -y espeak-ng ffmpeg
pip install pillow
bash submission/demo-reel/build.sh
```

## Winning take (operator — not this VM)

Needs: `CALLE_API_KEY`, `CS_OWNER_E164`, `SIGNAL_CONFIRM=PLACES`, `CUE_ALLOW_LIVE=1`, `SLACK_WEBHOOK_URL`, screen + call audio.

Spine: `curl POST /cue?live=1&confirm=PLACES` → phone rings → stage code → “one” → `apply-action --adapter slack`.

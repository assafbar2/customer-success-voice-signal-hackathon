# Demo reel — how we made a video without a human on camera

## What you get

[`stage-manager-demo.mp4`](stage-manager-demo.mp4) — ~70s Stage Manager walkthrough with TTS voiceover + still frames (CLI output, call beat, writeback).

## Honest limits

- Voice is **espeak-ng** (robotic). Fine for a temporary / placeholder Devpost video; re-record VO with a human mic for the final cut if you care about polish.
- Curtain-up phone ring is **recreated in frames** (we do not re-dial judges’ phones in the reel). Live calls were already proven separately.
- No talking-head. That’s intentional for “agent can ship a first cut.”

## Rebuild

```bash
# deps: espeak-ng, ffmpeg, python3-pillow
sudo apt-get install -y espeak-ng ffmpeg
pip install pillow
bash submission/demo-reel/build.sh
```

## Better VO later (optional)

1. Record human VO matching [`../video-script.md`](../video-script.md) as WAV segments `01.wav`…`07.wav` in `audio/`.  
2. Re-run `python3 submission/demo-reel/build_reel.py` (or splice with CapCut / Descript).  
3. Or screen-record the live [`site/`](../../site/) + real terminal with QuickTime / OBS and lay VO under.

## Pre-submit

When the final video ships, tick it on [`../PRE-SUBMIT.md`](../PRE-SUBMIT.md) **together with** the MVF survey ([`../mvf-feedback.md`](../mvf-feedback.md)), terminal GIF, and awesome-list PR. MVF is not part of the reel — it’s the Devpost feedback form filled the same day.

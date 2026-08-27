# Demo reel — Stage Manager

## What ships

- [`stage-manager-demo.mp4`](stage-manager-demo.mp4) — problem-first narrative (~2 min)
- YouTube (Devpost host): https://youtu.be/yvRq7P8F5-c
- [`stage-manager-loop.gif`](stage-manager-loop.gif) — dress-rehearsal CLI for README + site

## What you are looking at

1. **Editorial cards** — long holds, not slogan stacks. Problem is the first beat.
2. **Real CLI** — `xfce4-terminal` dress rehearsal (no key, no ring).
3. **Live call beat** — reconstructed from the **2026-08-12 CALL-E transcript** (stage code 4821, option 1). Caption: handset audio lives on the owner’s phone.
4. **Voice** — Microsoft neural TTS locked from the earlier-today take (`d9c3e82` audio, bit-identical). `bash build.sh` will **not** resynthesize unless `REGEN_TTS=1`. Video-only edits mux onto that track. GitHub’s file preview often looks silent; play the [judge site](https://assafbar2.github.io/customer-success-voice-signal-hackathon/#demo) or VLC/QuickTime with **sound on**. Human recut: [`vo/narration.md`](vo/narration.md).

Slack does not fire. Customer was never called.

## Rebuild

Needs: `ffmpeg`, `python3`, `pillow`, `edge-tts` (`pip install edge-tts pillow`), plus a CLI recording at `/opt/cursor/artifacts/stage-manager-cli-demo.mp4` (or re-run `record_cli.sh` on a desktop with `DISPLAY`).

```bash
bash submission/demo-reel/build.sh
```

Human VO (optional): drop wavs in `human-vo/` as named in `vo/narration.md`, then:

```bash
VO_DIR=human-vo bash submission/demo-reel/build.sh
```

## Upload

GitHub is not a valid Devpost video host. Public YouTube or Vimeo. Steps: [`../../notes/SUBMIT.md`](../../notes/SUBMIT.md).

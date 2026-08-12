#!/usr/bin/env python3
"""Build ≤3min Stage Manager demo reel from espeak VO + still frames.

First-cut for Devpost: real CLI captures + reconstructed call beat.
Does NOT include a live CALL-E ring (no key/phone in this environment).
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

REEL = Path(__file__).resolve().parent
FRAMES = REEL / "frames"
AUDIO = REEL / "audio"
PARTS = REEL / "parts"
W, H = 1920, 1080

# Winning spine, compressed: ring → why → curl → dress → decision → Slack → closer
LINES = [
    (
        "01",
        "Hi Maya. Stage Manager. You're up for Acme. That call happened because a support ticket looped twice.",
    ),
    (
        "02",
        "Customer Success owns the revenue relationship. Slack owns the noise. PagerDuty phones you to acknowledge an alert. Ack is not a decision.",
    ),
    (
        "03",
        "Judges: curl a cue into Stage Manager. No API key. Dress rehearsal — dry-run — by default. A webhook cannot arm a live call.",
    ),
    (
        "04",
        "Four cues, one engine. Stuck support, S L A risk, agent needs a decision, onboarding stall. CS owner only — never the customer.",
    ),
    (
        "05",
        "Curtain up. Stage code four eight two one. Line reading. One, two, or three. Maya says one. Take over in chat. Clear. Break a leg — or just open the ticket.",
    ),
    (
        "06",
        "Decision one lands as an action intent. Apply-action posts it to Slack. Phone rings, you say one, a message lands in the next system.",
    ),
    (
        "07",
        "When the account is on fire, we cue the firefighter — not the building. Stage Manager. Call E. No customers were called in the making of this demo.",
    ),
]


def font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for c in candidates:
        if Path(c).exists():
            return ImageFont.truetype(c, size)
    return ImageFont.load_default()


def bg() -> tuple[Image.Image, ImageDraw.ImageDraw]:
    img = Image.new("RGB", (W, H), (12, 10, 8))
    draw = ImageDraw.Draw(img)
    for r in range(700, 0, -8):
        a = int(40 * (1 - r / 700))
        color = (min(255, 30 + a * 2), min(255, 18 + a), min(255, 8 + a // 2))
        draw.ellipse([W // 2 - r, -r // 2, W // 2 + r, r], fill=color)
    draw.rectangle([0, 0, 140, H], fill=(42, 16, 14))
    draw.rectangle([W - 140, 0, W, H], fill=(42, 16, 14))
    return img, draw


def centered(draw, text, y, f, fill=(244, 239, 230)):
    bbox = draw.textbbox((0, 0), text, font=f)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) / 2, y), text, font=f, fill=fill)


def draw_term(d, lines, title):
    d.text((200, 100), title, font=font(48, True), fill=(255, 208, 137))
    y = 190
    for ln in lines[:18]:
        d.text((200, y), ln[:92], font=font(26), fill=(244, 239, 230))
        y += 40


def wav_duration(path: Path) -> float:
    return float(
        subprocess.check_output(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "csv=p=0",
                str(path),
            ],
            text=True,
        ).strip()
    )


def clean_lines(path: Path) -> list[str]:
    if not path.exists():
        return []
    out = []
    for ln in path.read_text().splitlines():
        if ln.startswith(">") or ln.startswith("npm "):
            continue
        ln = ln.replace("/workspace/skills/customer-success-voice-signal/", "")
        if ln.strip():
            out.append(ln)
    return out


def main() -> None:
    FRAMES.mkdir(parents=True, exist_ok=True)
    AUDIO.mkdir(parents=True, exist_ok=True)
    PARTS.mkdir(parents=True, exist_ok=True)

    for sid, text in LINES:
        wav = AUDIO / f"{sid}.wav"
        subprocess.check_call(
            ["espeak-ng", "-v", "en-us+m3", "-s", "142", "-p", "38", "-w", str(wav), text]
        )

    Fb, Fh, Fs = font(96, True), font(48, True), font(24)
    SPOT = (255, 208, 137)
    DIM = (183, 174, 160)

    img, d = bg()
    centered(d, "STAGE MANAGER", 300, Fb, SPOT)
    centered(d, "Hi Maya. You're up for Acme.", 450, Fh)
    centered(d, "Cold open · CS owner only · never the customer", 560, Fs, DIM)
    img.save(FRAMES / "01_open.png")

    img, d = bg()
    centered(d, "Ack is not a decision.", 380, Fb, SPOT)
    centered(d, "PagerDuty phones you to acknowledge.", 520, Fh)
    centered(d, "We capture a closed-set 1 / 2 / 3.", 600, Fs, DIM)
    img.save(FRAMES / "02_ack.png")

    curl = [
        "$ curl -X POST http://127.0.0.1:8787/cue \\",
        "    -H 'content-type: application/json' \\",
        "    -d @events/webhook_stuck_support.json",
        "",
        'exit: ok   mode: dress_rehearsal',
        "trigger: stuck_support   option: 1   take_over_chat",
        "intent_pending: true",
        "",
        "Live query without CUE_ALLOW_LIVE → HTTP 403 HOLD",
        "A webhook cannot arm a live call.",
    ]
    img, d = bg()
    draw_term(d, curl, "POST /cue · dress rehearsal")
    img.save(FRAMES / "03_curl.png")

    dress = clean_lines(REEL / "dress-rehearsal.txt")
    img, d = bg()
    draw_term(d, dress[:16] or [
        "Persona: Stage Manager",
        "Cue: stuck_support",
        "Call sheet: Maya Chen (CS only)",
        "Stage code: 4821",
        "1. Take over in chat now",
        "2. Assign to SE / specialist",
        "3. Not now — snooze 2 hours",
        "Simulated line reading: 1",
    ], "Dress rehearsal · no ring")
    img.save(FRAMES / "04_dress.png")

    img, d = bg()
    draw_term(
        d,
        [
            "Curtain up — live CALL-E  (reconstructed beat)",
            "",
            "Hi Maya. Stage Manager. You're up for Acme.",
            "Stage code — please repeat: 4 8 2 1.",
            "Ticket 4821 looping. Two bot handoffs.",
            "Line reading. Say 1, 2, or 3.",
            "",
            "Maya: Four eight two one. One.",
            "",
            "Confirming option 1 — take over in chat.",
            "Logging to the prompt book. Clear.",
            "Break a leg — or just open the ticket.",
        ],
        "Identity + line reading",
    )
    img.save(FRAMES / "05_call.png")

    slack = [
        "$ npm run apply-action -- --last --adapter slack",
        "",
        "Stage Manager — decision for Acme Corp",
        "Cue: stuck_support · Ticket 4821",
        "Line reading 1: Take over in chat now",
        "",
        "Phone rings → you say one → Slack gets the decision.",
        "That's the product. Not an ack. A handoff.",
    ]
    img, d = bg()
    draw_term(d, slack, "Action intent → Slack")
    img.save(FRAMES / "06_slack.png")

    img, d = bg()
    centered(d, "When the account is on fire,", 300, Fh)
    centered(d, "we cue the firefighter — not the building.", 380, Fh, SPOT)
    centered(d, "No customers were called in the making of this demo.", 500, Fs, DIM)
    centered(d, "Stage Manager · skills/customer-success-voice-signal/", 600, Fs, DIM)
    centered(
        d,
        "github.com/assafbar2/customer-success-voice-signal-hackathon",
        660,
        Fs,
        DIM,
    )
    img.save(FRAMES / "07_end.png")

    frame_names = [
        "01_open",
        "02_ack",
        "03_curl",
        "04_dress",
        "05_call",
        "06_slack",
        "07_end",
    ]

    parts: list[Path] = []
    segs = []
    for i, (sid, _) in enumerate(LINES):
        wav = AUDIO / f"{sid}.wav"
        frame = FRAMES / f"{frame_names[i]}.png"
        dur = wav_duration(wav)
        part = PARTS / f"{i:02d}.mp4"
        subprocess.check_call(
            [
                "ffmpeg",
                "-y",
                "-loop",
                "1",
                "-framerate",
                "30",
                "-i",
                str(frame),
                "-i",
                str(wav),
                "-c:v",
                "libx264",
                "-tune",
                "stillimage",
                "-pix_fmt",
                "yuv420p",
                "-c:a",
                "aac",
                "-b:a",
                "192k",
                "-ar",
                "44100",
                "-ac",
                "2",
                "-shortest",
                "-movflags",
                "+faststart",
                str(part),
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        probe = subprocess.check_output(
            [
                "ffprobe",
                "-v",
                "error",
                "-select_streams",
                "a",
                "-show_entries",
                "stream=codec_type",
                "-of",
                "csv=p=0",
                str(part),
            ],
            text=True,
        ).strip()
        if "audio" not in probe:
            raise RuntimeError(f"No audio in {part}")
        parts.append(part)
        segs.append({"id": sid, "frame": frame_names[i], "approx_seconds": round(dur, 1)})
        print(f"part {part.name} audio={probe} dur={dur:.1f}s")

    lst = REEL / "parts.txt"
    lst.write_text("".join(f"file '{p}'\n" for p in parts))
    out = REEL / "stage-manager-demo.mp4"
    artifact = Path("/opt/cursor/artifacts/demo/stage-manager-demo.mp4")
    artifact.parent.mkdir(parents=True, exist_ok=True)

    subprocess.check_call(
        [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(lst),
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-movflags",
            "+faststart",
            str(out),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    artifact.write_bytes(out.read_bytes())
    (REEL / "timeline.json").write_text(json.dumps(segs, indent=2))
    total = sum(s["approx_seconds"] for s in segs)
    print(f"wrote {out} ({out.stat().st_size} bytes) ~{total:.1f}s")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Build ≤3min Stage Manager demo reel from espeak VO + still frames (with audio)."""
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

# Approved script VO (submission/video-script.md)
LINES = [
    (
        "01",
        "Customer Success owns the revenue relationship. Slack owns the noise. When a named account is stuck — looping support, red S L A, agent blocked, health going quiet — the alert hides under everything else.",
    ),
    (
        "02",
        "Phone still cuts through. We don't dial the customer. We cue the firefighter. Stage Manager. Headset on. Places, please — your account is on.",
    ),
    (
        "03",
        "Dress rehearsal first — default, no ring, no keys required for judges. Preview the cue. Update the prompt book without touching a phone.",
    ),
    (
        "04",
        "Four cues, one engine: stuck support, S L A risk, agent needs a decision, health or onboarding stall.",
    ),
    (
        "05",
        "Curtain up. Live gate: live and places. Hi Maya. Stage Manager. You're up for Acme. Line reading — one, two, or three. Maya says one. Take over in chat. Logging to the prompt book. Clear.",
    ),
    (
        "06",
        "Decision one — take over in chat. Structured writeback. Auditable. The kind of trail you can hand a manager, not another Slack shrug. Same path when an agent hits needs-human — we ran that live too.",
    ),
    (
        "07",
        "When the account is on fire, we cue the firefighter — not the building. Stage Manager. Call E.",
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
    d.text((200, 120), title, font=font(54, True), fill=(255, 208, 137))
    y = 220
    for ln in lines[:16]:
        d.text((200, y), ln[:90], font=font(28), fill=(244, 239, 230))
        y += 42


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


def main() -> None:
    FRAMES.mkdir(parents=True, exist_ok=True)
    AUDIO.mkdir(parents=True, exist_ok=True)
    PARTS.mkdir(parents=True, exist_ok=True)

    for sid, text in LINES:
        wav = AUDIO / f"{sid}.wav"
        subprocess.check_call(
            ["espeak-ng", "-v", "en-us+m3", "-s", "138", "-p", "38", "-w", str(wav), text]
        )

    Fb, Fh, Fs = font(96, True), font(54, True), font(24)
    SPOT = (255, 208, 137)
    DIM = (183, 174, 160)

    img, d = bg()
    centered(d, "STAGE MANAGER", 340, Fb, SPOT)
    centered(d, "The alert hides under Slack.", 470, Fh)
    centered(d, "Problem · phone interrupt · CS owner only", 560, Fs, DIM)
    img.save(FRAMES / "01_title.png")

    img, d = bg()
    centered(d, "Places, please —", 380, Fh)
    centered(d, "your account is on.", 460, Fh, SPOT)
    centered(d, "We cue the firefighter — not the building.", 560, Fs, DIM)
    img.save(FRAMES / "02_value.png")

    dress = (
        (REEL / "dress-rehearsal.txt").read_text().splitlines()
        if (REEL / "dress-rehearsal.txt").exists()
        else []
    )
    dress = [
        ln.replace("/workspace/skills/customer-success-voice-signal/", "") for ln in dress
    ]
    img, d = bg()
    draw_term(d, dress, "Dress rehearsal · no ring")
    img.save(FRAMES / "03_dress.png")

    img, d = bg()
    draw_term(
        d,
        [
            "Four cues · one engine",
            "",
            "  stuck_support",
            "  sla_risk",
            "  agent_needs_decision",
            "  health_onboarding",
            "",
            "Same pipeline. CS owner only.",
        ],
        "Cue sheet",
    )
    img.save(FRAMES / "04_cues.png")

    img, d = bg()
    draw_term(
        d,
        [
            "Curtain up — live CALL-E",
            "",
            "Hi Maya. Stage Manager. You're up for Acme.",
            "Ticket 4821 looping. Two bot handoffs.",
            "Line reading. Press or say 1, 2, or 3.",
            "",
            "Maya: One.",
            "",
            "Confirming option 1 — take over in chat.",
            "Logging to the prompt book. Clear.",
        ],
        "Live line reading",
    )
    img.save(FRAMES / "05_call.png")

    img, d = bg()
    draw_term(
        d,
        [
            "Business value — writeback",
            "",
            "stuck_support        → 1  Take over in chat",
            "agent_needs_decision → 1  Approve A (exception)",
            "",
            "Right person · faster decision · audit trail",
            "Safe by default · one engine",
        ],
        "Prompt book / show report",
    )
    img.save(FRAMES / "06_writeback.png")

    img, d = bg()
    centered(d, "When the account is on fire,", 340, Fh)
    centered(d, "we cue the firefighter — not the building.", 420, Fh, SPOT)
    centered(d, "Stage Manager · customer-success-voice-signal", 540, Fs, DIM)
    centered(
        d,
        "github.com/assafbar2/customer-success-voice-signal-hackathon",
        620,
        Fs,
        DIM,
    )
    img.save(FRAMES / "07_end.png")

    frame_names = [
        "01_title",
        "02_value",
        "03_dress",
        "04_cues",
        "05_call",
        "06_writeback",
        "07_end",
    ]

    parts: list[Path] = []
    segs = []
    for i, (sid, _) in enumerate(LINES):
        wav = AUDIO / f"{sid}.wav"
        frame = FRAMES / f"{frame_names[i]}.png"
        dur = wav_duration(wav)
        part = PARTS / f"{i:02d}.mp4"
        # Explicit AAC audio — previous -c copy concat dropped the track
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
        # verify audio present
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

    # Re-encode concat so audio survives
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

    astreams = subprocess.check_output(
        [
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            "a",
            "-show_entries",
            "stream=codec_name,channels,sample_rate",
            "-of",
            "json",
            str(out),
        ],
        text=True,
    )
    total = sum(s["approx_seconds"] for s in segs)
    print(f"wrote {out} ({out.stat().st_size} bytes) ~{total:.1f}s")
    print("audio streams:", astreams)


if __name__ == "__main__":
    main()

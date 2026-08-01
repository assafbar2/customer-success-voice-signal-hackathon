#!/usr/bin/env python3
"""Build ≤3min Stage Manager demo reel from espeak VO + still frames."""
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

LINES = [
    (
        "01",
        "Customer Success owns the account. Slack owns the noise. When Acme is stuck, we don't dial the customer. We cue the firefighter. Stage Manager. Headset on.",
    ),
    (
        "02",
        "Dress rehearsal first. Default. No ring. The call sheet prints. Line readings one, two, three. Prompt book updates without touching a phone.",
    ),
    (
        "03",
        "Four cues on the sheet. Stuck support. S L A risk. Agent needs a decision. Health stall. Same engine.",
    ),
    (
        "04",
        "Curtain up. Live gate: live and places. Stage Manager calls Maya for Acme. Line reading. She says one. Take over in chat. Logged.",
    ),
    (
        "05",
        "Decision one. Written to the prompt book and show report. Structured. Auditable.",
    ),
    (
        "06",
        "Same path when an agent hits needs human. We already ran that live. Option one: allow the exception.",
    ),
    (
        "07",
        "When the account is on fire, we cue the firefighter, not the building. Stage Manager. Call E.",
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
    centered(d, "STAGE MANAGER", 360, Fb, SPOT)
    centered(d, "Places, please — your account is on.", 480, Fh)
    centered(d, "CALL-E hackathon · CS owner only", 580, Fs, DIM)
    img.save(FRAMES / "01_title.png")

    dress = (REEL / "dress-rehearsal.txt").read_text().splitlines() if (REEL / "dress-rehearsal.txt").exists() else []
    dress = [ln.replace("/workspace/skills/customer-success-voice-signal/", "") for ln in dress]
    img, d = bg()
    draw_term(d, dress, "Dress rehearsal · no ring")
    img.save(FRAMES / "02_dress.png")

    img, d = bg()
    draw_term(
        d,
        [
            "Four cues on the call sheet",
            "",
            "  stuck_support",
            "  sla_risk",
            "  agent_needs_decision",
            "  health_onboarding",
            "",
            "Same engine. CS owner only.",
        ],
        "Cue sheet",
    )
    img.save(FRAMES / "03_cues.png")

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
    img.save(FRAMES / "04_call.png")

    img, d = bg()
    draw_term(
        d,
        [
            "Prompt book / show report",
            "",
            "stuck_support        → 1  Take over in chat",
            "agent_needs_decision → 1  Approve A (exception)",
            "",
            "Structured. Auditable. No CRM cosplay.",
        ],
        "Writeback",
    )
    img.save(FRAMES / "05_writeback.png")

    img, d = bg()
    centered(d, "Same engine.", 380, Fh, SPOT)
    centered(d, "agent_needs_decision — live option 1", 480, font(36))
    centered(d, "Approve A — allow the exception", 560, Fs, DIM)
    img.save(FRAMES / "06_second.png")

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
        "02_dress",
        "03_cues",
        "04_call",
        "05_writeback",
        "06_second",
        "07_end",
    ]
    segs = []
    for i, (sid, _) in enumerate(LINES):
        wav = AUDIO / f"{sid}.wav"
        frame = FRAMES / f"{frame_names[i]}.png"
        dur = float(
            subprocess.check_output(
                [
                    "ffprobe",
                    "-v",
                    "error",
                    "-show_entries",
                    "format=duration",
                    "-of",
                    "csv=p=0",
                    str(wav),
                ],
                text=True,
            ).strip()
        )
        part = PARTS / f"{i:02d}.mp4"
        subprocess.check_call(
            [
                "ffmpeg",
                "-y",
                "-loop",
                "1",
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
                "-shortest",
                "-vf",
                "scale=1920:1080",
                str(part),
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        segs.append({"wav": str(wav), "frame": str(frame), "dur": dur, "part": str(part)})

    (REEL / "timeline.json").write_text(json.dumps(segs, indent=2))
    lst = REEL / "parts.txt"
    lst.write_text("".join(f"file '{s['part']}'\n" for s in segs))
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
            "-c",
            "copy",
            str(out),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    artifact.write_bytes(out.read_bytes())
    print(f"wrote {out} ({out.stat().st_size} bytes), total ~{sum(s['dur'] for s in segs):.1f}s")


if __name__ == "__main__":
    main()

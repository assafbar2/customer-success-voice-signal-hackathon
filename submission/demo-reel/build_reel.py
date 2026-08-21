#!/usr/bin/env python3
"""Build Stage Manager demo reel: title cards + real CLI screen recording + live-transcript call beat."""
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
CLI_SRC = Path("/opt/cursor/artifacts/stage-manager-cli-demo.mp4")
SPOT = (255, 208, 137)
CREAM = (244, 239, 230)
DIM = (183, 174, 160)
BG = (12, 10, 8)

# Spoken lines (espeak). Call beat matches the 2026-08-12 live transcript, not a Maya script.
LINES = {
    "01": "Customer Success owns the revenue relationship. Slack owns the noise. When a named account is stuck, the alert hides under everything else.",
    "02": "Phone still cuts through. We don't dial the customer. We cue the firefighter. Stage Manager. Headset on.",
    "03": "Judges run dress rehearsal with no key. The prompt book already holds the live decision — option one, take over in chat. Slack does not fire.",
    "04": "Curtain up. The phone rings the C S owner only. Stage code — four eight two one. Line reading. One. Take over in chat. Logging to the prompt book. Clear. Break a leg — or just open the ticket.",
    "05": "When the account is on fire, we cue the firefighter — not the building. Stage Manager. Call E. No customers were called in the making of this demo.",
}


def font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    path = (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    )
    if Path(path).exists():
        return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def mono(size: int) -> ImageFont.ImageFont:
    path = "/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Regular.ttf"
    if Path(path).exists():
        return ImageFont.truetype(path, size)
    return font(size)


def run(cmd: list[str], quiet: bool = True) -> None:
    kwargs = {}
    if quiet:
        kwargs["stdout"] = subprocess.DEVNULL
        kwargs["stderr"] = subprocess.DEVNULL
    subprocess.check_call(cmd, **kwargs)


def probe_dur(path: Path) -> float:
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


def bg() -> tuple[Image.Image, ImageDraw.ImageDraw]:
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    for r in range(700, 0, -8):
        a = int(40 * (1 - r / 700))
        color = (min(255, 30 + a * 2), min(255, 18 + a), min(255, 8 + a // 2))
        draw.ellipse([W // 2 - r, -r // 2, W // 2 + r, r], fill=color)
    draw.rectangle([0, 0, 140, H], fill=(42, 16, 14))
    draw.rectangle([W - 140, 0, W, H], fill=(42, 16, 14))
    return img, draw


def centered(draw: ImageDraw.ImageDraw, text: str, y: int, f, fill=CREAM) -> None:
    bbox = draw.textbbox((0, 0), text, font=f)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) / 2, y), text, font=f, fill=fill)


def still_to_mp4(png: Path, wav: Path | None, out: Path, min_dur: float = 0) -> None:
    dur = probe_dur(wav) if wav else min_dur
    if min_dur:
        dur = max(dur, min_dur)
    cmd = [
        "ffmpeg",
        "-y",
        "-loop",
        "1",
        "-framerate",
        "30",
        "-i",
        str(png),
    ]
    if wav:
        cmd += ["-i", str(wav)]
    cmd += [
        "-c:v",
        "libx264",
        "-tune",
        "stillimage",
        "-pix_fmt",
        "yuv420p",
        "-t",
        f"{dur:.3f}",
        "-r",
        "30",
    ]
    if wav:
        cmd += ["-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2", "-shortest"]
    else:
        cmd += ["-an"]
    cmd += ["-movflags", "+faststart", str(out)]
    run(cmd)


def speak(sid: str, text: str) -> Path:
    wav = AUDIO / f"{sid}.wav"
    run(["espeak-ng", "-v", "en-us+m3", "-s", "142", "-p", "38", "-w", str(wav), text], quiet=False)
    return wav


def make_ring(path: Path) -> None:
    # Dual-tone US-ish ring, two bursts.
    run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "lavfi",
            "-i",
            "sine=frequency=440:duration=1.8",
            "-f",
            "lavfi",
            "-i",
            "sine=frequency=480:duration=1.8",
            "-filter_complex",
            "[0][1]amix=inputs=2:duration=first,atrim=0:1.8,adelay=0|0[a];"
            "sine=frequency=440:duration=1.8[b1];sine=frequency=480:duration=1.8[b2];"
            "[b1][b2]amix=inputs=2:duration=first[b];"
            "[b]adelay=2800|2800[bd];"
            "[a][bd]amix=inputs=2:duration=longest,volume=0.35",
            "-t",
            "6",
            str(path),
        ]
    )


def trim_cli(out: Path) -> None:
    # Reviewer: usable CLI is ~00:01–00:19 on 1920x1200. Crop to 1080p.
    run(
        [
            "ffmpeg",
            "-y",
            "-ss",
            "1.0",
            "-t",
            "18.2",
            "-i",
            str(CLI_SRC),
            "-vf",
            "crop=1920:1080:0:60,scale=1920:1080",
            "-r",
            "30",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-an",
            "-movflags",
            "+faststart",
            str(out),
        ]
    )


def mix_vo_under(video: Path, wav: Path, out: Path) -> None:
    vdur = probe_dur(video)
    adur = probe_dur(wav)
    # If VO is longer, freeze last frame; if shorter, pad audio.
    run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(video),
            "-i",
            str(wav),
            "-filter_complex",
            f"[0:v]tpad=stop_mode=clone:stop_duration={max(0, adur - vdur):.3f}[v];"
            f"[1:a]apad=pad_dur={max(0, vdur - adur):.3f},volume=1.0[a]",
            "-map",
            "[v]",
            "-map",
            "[a]",
            "-c:v",
            "libx264",
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
            str(out),
        ]
    )


def concat(parts: list[Path], out: Path) -> None:
    lst = REEL / "parts.txt"
    lst.write_text("".join(f"file '{p}'\n" for p in parts))
    run(
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
            "-ar",
            "44100",
            "-movflags",
            "+faststart",
            str(out),
        ]
    )


def gif_from(video: Path, out: Path) -> None:
    pal = PARTS / "palette.png"
    run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(video),
            "-vf",
            "fps=8,scale=960:-1:flags=lanczos,palettegen",
            str(pal),
        ]
    )
    run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(video),
            "-i",
            str(pal),
            "-lavfi",
            "fps=8,scale=960:-1:flags=lanczos[x];[x][1:v]paletteuse",
            str(out),
        ]
    )


def main() -> None:
    for d in (FRAMES, AUDIO, PARTS):
        d.mkdir(parents=True, exist_ok=True)
    if not CLI_SRC.exists():
        raise SystemExit(f"missing CLI recording: {CLI_SRC}")

    wavs = {sid: speak(sid, text) for sid, text in LINES.items()}

    Fb, Fh, Fs = font(92, True), font(48, True), font(26)
    Fm = mono(32)

    img, d = bg()
    centered(d, "STAGE MANAGER", 340, Fb, SPOT)
    centered(d, "The alert hides under Slack.", 470, Fh)
    centered(d, "Ack is not a decision.", 560, Fs, DIM)
    img.save(FRAMES / "01_title.png")

    img, d = bg()
    centered(d, "We don’t dial the customer.", 360, Fh)
    centered(d, "We cue the firefighter.", 450, Fh, SPOT)
    centered(d, "CS owner only  ·  dress rehearsal default  ·  live needs PLACES", 560, Fs, DIM)
    img.save(FRAMES / "02_value.png")

    img, d = bg()
    d.text((200, 140), "Live CALL-E transcript  ·  2026-08-12", font=font(36, True), fill=SPOT)
    lines = [
        "Curtain up — CS owner only. Never the customer.",
        "",
        "Hi Assaf. Stage Manager. You’re up for Acme Corp.",
        "Stage code — please repeat: 4 8 2 1.",
        "Assaf: 4 8 2 1.",
        "Line reading. Say 1, 2, or 3.",
        "Assaf: 1.",
        "",
        "Logging takeover in the prompt book.",
        "Clear. Break a leg — or just open the ticket.",
    ]
    y = 220
    for ln in lines:
        d.text((200, y), ln, font=Fm, fill=CREAM)
        y += 58
    d.text(
        (200, 980),
        "Reconstructed from the live CALL-E transcript. Handset audio lives on the owner’s phone.",
        font=font(22),
        fill=DIM,
    )
    img.save(FRAMES / "04_call.png")

    img, d = bg()
    centered(d, "When the account is on fire,", 320, Fh)
    centered(d, "we cue the firefighter — not the building.", 400, Fh, SPOT)
    centered(d, "Stage Manager  ·  skills/customer-success-voice-signal", 530, Fs, DIM)
    centered(d, "github.com/assafbar2/customer-success-voice-signal-hackathon", 590, Fs, DIM)
    centered(d, "No customers were called in the making of this demo.", 700, Fs, SPOT)
    img.save(FRAMES / "05_end.png")

    p01 = PARTS / "01_title.mp4"
    p02 = PARTS / "02_value.mp4"
    p03 = PARTS / "03_cli.mp4"
    p04 = PARTS / "04_call.mp4"
    p05 = PARTS / "05_end.mp4"
    cli_trim = PARTS / "cli-trim.mp4"

    still_to_mp4(FRAMES / "01_title.png", wavs["01"], p01)
    still_to_mp4(FRAMES / "02_value.png", wavs["02"], p02)
    trim_cli(cli_trim)
    mix_vo_under(cli_trim, wavs["03"], p03)
    still_to_mp4(FRAMES / "04_call.png", wavs["04"], p04)
    still_to_mp4(FRAMES / "05_end.png", wavs["05"], p05)

    out = REEL / "stage-manager-demo.mp4"
    concat([p01, p02, p03, p04, p05], out)
    gif = REEL / "stage-manager-loop.gif"
    gif_from(cli_trim, gif)

    site_assets = REEL.parent.parent / "site" / "assets"
    site_assets.mkdir(parents=True, exist_ok=True)
    (site_assets / "stage-manager-loop.gif").write_bytes(gif.read_bytes())
    (site_assets / "stage-manager-demo.mp4").write_bytes(out.read_bytes())

    artifact_dir = Path("/opt/cursor/artifacts/demo")
    artifact_dir.mkdir(parents=True, exist_ok=True)
    (artifact_dir / "stage-manager-demo.mp4").write_bytes(out.read_bytes())
    (artifact_dir / "stage-manager-loop.gif").write_bytes(gif.read_bytes())

    segs = []
    for p, name in [
        (p01, "title"),
        (p02, "value"),
        (p03, "cli"),
        (p04, "call"),
        (p05, "end"),
    ]:
        segs.append({"part": name, "seconds": round(probe_dur(p), 1)})
    total = sum(s["seconds"] for s in segs)
    (REEL / "timeline.json").write_text(json.dumps({"total_seconds": total, "parts": segs}, indent=2))
    print(f"wrote {out} ({out.stat().st_size} bytes) ~{total:.1f}s")
    print(f"gif {gif} ({gif.stat().st_size} bytes)")
    astreams = subprocess.check_output(
        [
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            "a",
            "-show_entries",
            "stream=codec_name",
            "-of",
            "csv=p=0",
            str(out),
        ],
        text=True,
    ).strip()
    print("audio:", astreams or "MISSING")
    if "aac" not in astreams:
        raise SystemExit("final mp4 has no AAC audio")


if __name__ == "__main__":
    main()

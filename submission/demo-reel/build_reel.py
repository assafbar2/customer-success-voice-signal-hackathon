#!/usr/bin/env python3
"""Build a problem-first Stage Manager demo reel (neural TTS, long holds)."""
from __future__ import annotations

import asyncio
import json
import os
import subprocess
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

REEL = Path(__file__).resolve().parent
FRAMES = REEL / "frames"
AUDIO = REEL / "audio"
PARTS = REEL / "parts"
W, H = 1920, 1080
CLI_SRC = Path("/opt/cursor/artifacts/stage-manager-cli-demo.mp4")
OLD_REEL = REEL / "stage-manager-demo.mp4"
SPOT = (255, 208, 137)
CREAM = (244, 239, 230)
DIM = (183, 174, 160)
BG = (12, 10, 8)
CURTAIN = (42, 16, 14)

NARRATOR = "en-US-AndrewMultilingualNeural"
SM_VOICE = "en-US-GuyNeural"
OWNER_VOICE = "en-US-BrianNeural"
RATE = "-10%"
PITCH = "-2Hz"

VO_DIR = Path(os.environ.get("VO_DIR", ""))
if VO_DIR and not VO_DIR.is_absolute():
    VO_DIR = REEL / VO_DIR


def font(size: int, bold: bool = False, serif: bool = False) -> ImageFont.ImageFont:
    candidates = []
    if serif:
        candidates += [
            "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        ]
    candidates += [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def mono(size: int) -> ImageFont.ImageFont:
    path = "/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Regular.ttf"
    if Path(path).exists():
        return ImageFont.truetype(path, size)
    return font(size)


def run(cmd: list[str], quiet: bool = True) -> None:
    kwargs: dict = {}
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
    for r in range(820, 0, -10):
        a = int(36 * (1 - r / 820))
        color = (min(255, 28 + a * 2), min(255, 16 + a), min(255, 8 + a // 2))
        draw.ellipse([W // 2 - r, -r // 2 - 80, W // 2 + r, r - 40], fill=color)
    draw.rectangle([0, 0, 96, H], fill=CURTAIN)
    draw.rectangle([W - 96, 0, W, H], fill=CURTAIN)
    return img, draw


def wrap_draw(draw: ImageDraw.ImageDraw, text: str, y: int, f, fill=CREAM, width: int = 28, gap: int = 58) -> int:
    for line in textwrap.wrap(text, width=width):
        bbox = draw.textbbox((0, 0), line, font=f)
        tw = bbox[2] - bbox[0]
        draw.text(((W - tw) / 2, y), line, font=f, fill=fill)
        y += gap
    return y


def centered(draw: ImageDraw.ImageDraw, text: str, y: int, f, fill=CREAM) -> None:
    bbox = draw.textbbox((0, 0), text, font=f)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) / 2, y), text, font=f, fill=fill)


def mean_volume_db(path: Path) -> float:
    out = subprocess.check_output(
        ["ffmpeg", "-i", str(path), "-af", "volumedetect", "-f", "null", "-"],
        stderr=subprocess.STDOUT,
        text=True,
    )
    for line in out.splitlines():
        if "mean_volume:" in line:
            return float(line.split("mean_volume:")[1].split("dB")[0].strip())
    return -99.0


def loudnorm_wav(src: Path, dst: Path | None = None) -> Path:
    dst = dst or src
    tmp = src.with_name(src.stem + ".__ln.wav")
    run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(src),
            "-af",
            "loudnorm=I=-16:TP=-1.5:LRA=11",
            "-ar",
            "44100",
            "-ac",
            "2",
            str(tmp),
        ]
    )
    tmp.replace(dst)
    return dst


def to_wav(src: Path, dst: Path) -> None:
    run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(src),
            "-ar",
            "44100",
            "-ac",
            "2",
            str(dst),
        ]
    )


def speak_edge(text: str, dst: Path, voice: str) -> None:
    mp3 = dst.with_suffix(".mp3")

    async def _go() -> None:
        comm = __import__("edge_tts").Communicate(text, voice=voice, rate=RATE, pitch=PITCH)
        await comm.save(str(mp3))

    asyncio.run(_go())
    to_wav(mp3, dst)
    loudnorm_wav(dst)
    db = mean_volume_db(dst)
    if db < -45:
        raise SystemExit(f"TTS produced near-silence for {dst.name} ({db:.1f} dB)")


def speak(name: str, text: str, voice: str = NARRATOR) -> Path:
    wav = AUDIO / f"{name}.wav"
    human = None
    if VO_DIR:
        for ext in (".wav", ".mp3"):
            cand = VO_DIR / f"{name}{ext}"
            if cand.exists():
                human = cand
                break
    if human:
        if human.suffix.lower() == ".wav":
            to_wav(human, wav) if human.resolve() != wav.resolve() else None
            if human.resolve() != wav.resolve():
                to_wav(human, wav)
        else:
            to_wav(human, wav)
        loudnorm_wav(wav)
        return wav
    speak_edge(text, wav, voice)
    return wav


def silence(path: Path, seconds: float) -> None:
    run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "lavfi",
            "-i",
            f"anullsrc=r=44100:cl=stereo",
            "-t",
            f"{seconds:.3f}",
            str(path),
        ]
    )


def concat_wavs(parts: list[Path], out: Path) -> None:
    lst = AUDIO / "_concat.txt"
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
            "-c",
            "pcm_s16le",
            str(out),
        ]
    )


def still_to_mp4(png: Path, wav: Path | None, out: Path, min_dur: float = 0) -> None:
    dur = probe_dur(wav) if wav else min_dur
    if min_dur:
        dur = max(dur, min_dur)
    fade_out = max(0.05, dur - 0.45)
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
    else:
        cmd += ["-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo"]
    vf = f"fade=t=in:st=0:d=0.6,fade=t=out:st={fade_out:.3f}:d=0.4,format=yuv420p"
    cmd += [
        "-vf",
        vf,
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
    run(cmd)


def make_ring(path: Path) -> None:
    run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "lavfi",
            "-i",
            "sine=frequency=440:duration=1.6",
            "-f",
            "lavfi",
            "-i",
            "sine=frequency=480:duration=1.6",
            "-filter_complex",
            "[0][1]amix=inputs=2:duration=first,atrim=0:1.6,volume=0.28[a];"
            "sine=frequency=440:duration=1.6[b1];sine=frequency=480:duration=1.6[b2];"
            "[b1][b2]amix=inputs=2:duration=first,volume=0.28[b];"
            "[b]adelay=2600|2600[bd];"
            "[a][bd]amix=inputs=2:duration=longest,apad=pad_dur=1.2",
            "-t",
            "5.2",
            str(path),
        ]
    )


def extract_cli_from_old(out: Path) -> bool:
    if not OLD_REEL.exists():
        return False
    # Previous reel: title 10.1 + value 8.8 = CLI starts ~18.9s for ~18.3s
    run(
        [
            "ffmpeg",
            "-y",
            "-ss",
            "19.0",
            "-t",
            "18.0",
            "-i",
            str(OLD_REEL),
            "-vf",
            "scale=1920:1080,setsar=1",
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
    return out.exists()


def trim_cli(out: Path) -> None:
    if CLI_SRC.exists():
        run(
            [
                "ffmpeg",
                "-y",
                "-ss",
                "0.4",
                "-i",
                str(CLI_SRC),
                "-vf",
                "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setsar=1",
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
        return
    if not extract_cli_from_old(out):
        raise SystemExit("missing CLI recording and no prior reel to extract from")


def mix_vo_under(video: Path, wav: Path, out: Path, overlay: str | None = None) -> None:
    vdur = probe_dur(video)
    adur = probe_dur(wav)
    vf = f"[0:v]tpad=stop_mode=clone:stop_duration={max(0, adur - vdur):.3f}"
    if overlay:
        fontfile = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        vf += (
            f",drawtext=fontfile={fontfile}:text='{overlay}':x=110:y=h-90:"
            "fontsize=28:fontcolor=0xFFD089:shadowcolor=0x0c0a08:shadowx=2:shadowy=2"
        )
    vf += "[v]"
    run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(video),
            "-i",
            str(wav),
            "-filter_complex",
            f"{vf};[1:a]apad=pad_dur={max(0, vdur - adur):.3f},loudnorm=I=-16:TP=-1.5:LRA=11[a]",
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
    run(["ffmpeg", "-y", "-i", str(video), "-vf", "fps=8,scale=960:-1:flags=lanczos,palettegen", str(pal)])
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


def draw_problem() -> Path:
    img, d = bg()
    centered(d, "THE PROBLEM", 150, font(22, True), SPOT)
    wrap_draw(
        d,
        "Every company pages an engineer when a server goes down.",
        250,
        font(46, True, serif=True),
        CREAM,
        width=32,
        gap=62,
    )
    wrap_draw(
        d,
        "Almost nobody pages the human who owns the renewal when the account goes quiet.",
        420,
        font(38, False, serif=True),
        SPOT,
        width=36,
        gap=56,
    )
    wrap_draw(
        d,
        "Customer Success owns the revenue. Slack owns the noise. The alert hides until churn is already expensive.",
        620,
        font(28),
        DIM,
        width=52,
        gap=42,
    )
    centered(d, "Ack is not a decision.", 860, font(28, True), CREAM)
    path = FRAMES / "01_problem.png"
    img.save(path)
    return path


def draw_insight() -> Path:
    img, d = bg()
    centered(d, "STAGE MANAGER", 200, font(22, True), SPOT)
    wrap_draw(
        d,
        "We don’t dial the customer.",
        320,
        font(52, True, serif=True),
        CREAM,
        width=28,
        gap=70,
    )
    wrap_draw(
        d,
        "We cue the firefighter.",
        470,
        font(52, True, serif=True),
        SPOT,
        width=28,
        gap=70,
    )
    centered(d, "CS owner only   ·   sixty seconds   ·   say 1, 2, or 3", 680, font(26), DIM)
    centered(d, "Rare. Short. Structured. Then hang up.", 760, font(26), DIM)
    path = FRAMES / "02_insight.png"
    img.save(path)
    return path


def draw_phone(phase: str) -> Path:
    img, d = bg()
    # Phone bezel
    x0, y0, x1, y1 = 560, 80, 1360, 1000
    d.rounded_rectangle([x0, y0, x1, y1], radius=48, fill=(22, 18, 16), outline=SPOT, width=3)
    d.rounded_rectangle([x0 + 28, y0 + 36, x1 - 28, y1 - 36], radius=28, fill=(8, 7, 6))
    d.rounded_rectangle([920, 108, 1000, 122], radius=6, fill=(40, 36, 32))

    inner_x = x0 + 56
    Fm = mono(26)
    Fh = font(22, True)
    if phase == "ring":
        centered(d, "Incoming  ·  CS owner only", 220, Fh, SPOT)
        wrap_draw(d, "Stage Manager", 360, font(44, True, serif=True), CREAM, width=20, gap=60)
        centered(d, "Acme Corp  ·  stuck support", 500, font(26), DIM)
        centered(d, "Never the customer", 900, font(22), DIM)
    else:
        d.text((inner_x, 200), "Live CALL-E  ·  12 Aug 2026", font=Fh, fill=SPOT)
        lines = [
            ("SM", "You’re up for Acme. Stage code: 4 8 2 1."),
            ("Owner", "Four eight two one."),
            ("SM", "Line reading. One: take over in chat now."),
            ("Owner", "One."),
            ("SM", "Logging takeover. Clear."),
        ]
        y = 280
        for who, line in lines:
            color = SPOT if who == "SM" else CREAM
            d.text((inner_x, y), who, font=font(18, True), fill=DIM)
            y += 32
            for wrapped in textwrap.wrap(line, 36):
                d.text((inner_x, y), wrapped, font=Fm, fill=color)
                y += 38
            y += 18
        d.text((inner_x, 930), "Handset audio lives on the owner’s phone.", font=font(18), fill=DIM)
    path = FRAMES / f"04_{phase}.png"
    img.save(path)
    return path


def draw_close() -> Path:
    img, d = bg()
    wrap_draw(
        d,
        "When the account is on fire, we cue the firefighter — not the building.",
        280,
        font(42, True, serif=True),
        SPOT,
        width=30,
        gap=62,
    )
    centered(d, "Stage Manager  ·  skills/customer-success-voice-signal", 560, font(24), DIM)
    centered(d, "github.com/assafbar2/customer-success-voice-signal-hackathon", 620, font(24), DIM)
    centered(d, "No customers were called in the making of this demo.", 760, font(26, True), CREAM)
    path = FRAMES / "05_close.png"
    img.save(path)
    return path


def generate_og() -> None:
    ow, oh = 1280, 640
    img = Image.new("RGB", (ow, oh), BG)
    d = ImageDraw.Draw(img)
    for r in range(500, 0, -8):
        a = int(40 * (1 - r / 500))
        color = (min(255, 30 + a * 2), min(255, 18 + a), min(255, 8))
        d.ellipse([ow // 2 - r, -r // 2, ow // 2 + r, r], fill=color)
    d.rectangle([0, 0, 64, oh], fill=CURTAIN)
    d.rectangle([ow - 64, 0, ow, oh], fill=CURTAIN)
    title = font(52, True, serif=True)
    sub = font(26)
    t = "Stage Manager"
    bbox = d.textbbox((0, 0), t, font=title)
    d.text(((ow - (bbox[2] - bbox[0])) / 2, 200), t, font=title, fill=SPOT)
    line = "When the renewal goes quiet, page the owner — not the customer."
    y = 300
    for wrapped in textwrap.wrap(line, 42):
        bbox = d.textbbox((0, 0), wrapped, font=sub)
        d.text(((ow - (bbox[2] - bbox[0])) / 2, y), wrapped, font=sub, fill=CREAM)
        y += 40
    d.text((0, 0), "", font=sub)
    fine = font(18)
    cap = "CALL-E skill  ·  CS owner only  ·  never the customer"
    bbox = d.textbbox((0, 0), cap, font=fine)
    d.text(((ow - (bbox[2] - bbox[0])) / 2, 500), cap, font=fine, fill=DIM)
    site = REEL.parent.parent / "site"
    site.mkdir(parents=True, exist_ok=True)
    img.save(site / "og.png")


def crossfade_pair(a: Path, b: Path, out: Path, fade: float = 0.6) -> None:
    da, db = probe_dur(a), probe_dur(b)
    offset = max(0, da - fade)
    run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(a),
            "-i",
            str(b),
            "-filter_complex",
            f"[0:v][1:v]xfade=transition=fade:duration={fade}:offset={offset:.3f}[v];"
            f"[0:a][1:a]acrossfade=d={fade}[a]",
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
            "-movflags",
            "+faststart",
            str(out),
        ]
    )


def main() -> None:
    for d in (FRAMES, AUDIO, PARTS):
        d.mkdir(parents=True, exist_ok=True)
    generate_og()

    w_problem = speak(
        "01_problem",
        "Every company pages an engineer when a server goes down. Almost nobody pages the human who owns the renewal when the account goes quiet. Customer Success owns the revenue relationship. Slack owns the noise. When a named account is looping in support — two bot handoffs, ticket still open, enterprise on the line — the alert is just another message in a river of messages. Until churn is already expensive. That is the problem.",
    )
    w_insight = speak(
        "02_insight",
        "Phone still cuts through. Not as a spam dialer to the customer. As a sixty-second interrupt for the C S owner. Rare. Short. Structured. One, two, or three. Then hang up. This is Stage Manager.",
    )
    w_cli = speak(
        "03_cli",
        "Judges run the whole loop with no A P I key. Dress rehearsal is the default: same call sheet, same line readings, same prompt book — no ring. Four cues, one engine: stuck support, S L A risk, agent needs a human, health or onboarding stall.",
    )
    w_host = speak(
        "04a_host",
        "When we took it live, Call E rang the C S owner only. Never the customer.",
    )
    gap = AUDIO / "gap.wav"
    silence(gap, 0.35)
    ring = AUDIO / "ring.wav"
    make_ring(ring)
    sm1 = speak(
        "04b_sm1",
        "Hi. Stage Manager. You are up for Acme. Stage code — please repeat: four eight two one.",
        SM_VOICE,
    )
    own1 = speak("04c_own1", "Four eight two one.", OWNER_VOICE)
    sm2 = speak(
        "04b_sm2",
        "Line reading. Say one, two, or three. One: take over in chat now.",
        SM_VOICE,
    )
    own2 = speak("04c_own2", "One.", OWNER_VOICE)
    sm3 = speak(
        "04b_sm3",
        "Logging takeover in the prompt book. Clear. Break a leg — or just open the ticket.",
        SM_VOICE,
    )
    w_call = AUDIO / "04_call.wav"
    concat_wavs([w_host, gap, ring, gap, sm1, gap, own1, gap, sm2, gap, own2, gap, sm3], w_call)
    loudnorm_wav(w_call)
    w_close = speak(
        "05_close",
        "That decision is state. Not a Slack shrug. An action intent for the next system. Ack is not a decision. This is. When the account is on fire, we cue the firefighter — not the building. Stage Manager. No customers were called in the making of this demo.",
    )

    p01 = PARTS / "01_problem.mp4"
    p02 = PARTS / "02_insight.mp4"
    p03 = PARTS / "03_cli.mp4"
    p04 = PARTS / "04_call.mp4"
    p05 = PARTS / "05_close.mp4"

    still_to_mp4(draw_problem(), w_problem, p01)
    still_to_mp4(draw_insight(), w_insight, p02)

    cli_trim = PARTS / "cli-trim.mp4"
    trim_cli(cli_trim)
    mix_vo_under(cli_trim, w_cli, p03, overlay="Dress rehearsal  ·  no API key  ·  no ring")

    # Call: ring frame then transcript frame, matched to audio.
    ring_png = draw_phone("ring")
    talk_png = draw_phone("talk")
    host_d = probe_dur(w_host) + 0.35
    ring_d = probe_dur(ring) + 0.35
    intro = host_d + ring_d
    talk_d = probe_dur(w_call) - intro
    p_ring = PARTS / "04a_ring.mp4"
    p_talk = PARTS / "04b_talk.mp4"
    still_to_mp4(ring_png, None, p_ring, min_dur=intro)
    still_to_mp4(talk_png, None, p_talk, min_dur=max(talk_d, 8))
    # Attach the full call audio under a concat of the two silent videos.
    call_silent = PARTS / "04_silent.mp4"
    concat([p_ring, p_talk], call_silent)
    mix_vo_under(call_silent, w_call, p04)

    still_to_mp4(draw_close(), w_close, p05)

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

    segs = [{"part": n, "seconds": round(probe_dur(p), 1)} for p, n in [
        (p01, "problem"),
        (p02, "insight"),
        (p03, "cli"),
        (p04, "call"),
        (p05, "close"),
    ]]
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
    db = mean_volume_db(out)
    print(f"mean_volume: {db:.1f} dB")
    if db < -40:
        raise SystemExit(f"final mp4 audio is too quiet / silent ({db:.1f} dB)")
    if total > 180:
        raise SystemExit(f"reel is {total:.1f}s — over the 3:00 Devpost cap")


if __name__ == "__main__":
    main()

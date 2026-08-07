#!/usr/bin/env python3
"""Raster preview of the support-volume bubble chart."""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent / "support-volume-bubbles-preview.png"

CHANNELS = [
    {"label": "Documentation", "value": 300_000, "display": "300,000"},
    {"label": "Help centers total articles views", "value": 152_000, "display": "152,000"},
    {"label": "Kapa", "value": 11_000, "display": "11,000"},
    {"label": "GitHub issues & discussions", "value": 2_700, "display": "2,700"},
    {"label": "Support", "value": 2_500, "display": "2,500", "highlight": True},
    {"label": "Social channels", "value": 600, "display": "600"},
    {"label": "Discord & community", "value": 200, "display": "200"},
    {"label": "Feedback systems", "value": 200, "display": "200"},
]

FOOTNOTE = "We redesigned one of the smallest, clearest surfaces first."
W, H = 1920, 1080
BG = (247, 245, 242)
INK = (26, 23, 20)
INK_MUTED = (92, 85, 76)
BUBBLE_FILL = (216, 207, 195)
BUBBLE_LINE = (185, 174, 160)
SUPPORT_FILL = (232, 165, 75)
SUPPORT_RING = (138, 59, 18)
SUPPORT_INK = (42, 20, 8)
CHIP_INK = (255, 251, 246)
LABEL_SIZE = 20
VALUE_SIZE = 24


@dataclass
class Bubble:
    channel: dict
    cx: float
    cy: float
    r: float


def font(size: int, bold: bool = False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines or [text]


def pack_bubbles(channels, origin_x, origin_y, width, height):
    max_v = max(c["value"] for c in channels)
    max_r = min(width, height) * 0.40
    ordered = sorted(channels, key=lambda c: c["value"], reverse=True)
    placed: list[Bubble] = []
    cx0 = origin_x + width * 0.36
    cy0 = origin_y + height * 0.50
    gap = 8.0

    for i, ch in enumerate(ordered):
        r = max_r * math.sqrt(ch["value"] / max_v)
        if i == 0:
            placed.append(Bubble(ch, cx0, cy0, r))
            continue
        best, best_score = None, float("inf")
        for host in placed:
            for ang_i in range(48):
                ang = (ang_i / 48) * 2 * math.pi
                dist = host.r + r + gap
                cx = host.cx + math.cos(ang) * dist
                cy = host.cy + math.sin(ang) * dist
                if cx - r < origin_x or cy - r < origin_y or cx + r > origin_x + width or cy + r > origin_y + height:
                    continue
                if any(math.hypot(cx - p.cx, cy - p.cy) < p.r + r + gap * 0.6 for p in placed):
                    continue
                score = math.hypot(cx - cx0, cy - cy0)
                if ch.get("highlight"):
                    score += (cy0 - cy) * 0.25
                    score -= (cx - cx0) * 0.05
                if score < best_score:
                    best_score = score
                    best = (cx, cy)
        if best is None:
            best = (origin_x + width * 0.78, origin_y + height * 0.78)
        placed.append(Bubble(ch, best[0], best[1], r))
    return placed


def draw_label(draw, cx, cy, r, channel, label_f, label_bold, value_f):
    highlight = bool(channel.get("highlight"))
    ink = SUPPORT_INK if highlight else INK
    lf = label_bold if highlight else label_f
    if r * 2 >= 140:
        lines = wrap(draw, channel["label"], lf, max(r * 1.6, 40))
        block = len(lines) * (LABEL_SIZE + 3) + VALUE_SIZE + 6
        ty = cy - block / 2
        for i, line in enumerate(lines):
            tw = draw.textlength(line, font=lf)
            draw.text((cx - tw / 2, ty + i * (LABEL_SIZE + 3)), line, font=lf, fill=ink)
        vw = draw.textlength(channel["display"], font=value_f)
        draw.text((cx - vw / 2, ty + len(lines) * (LABEL_SIZE + 3) + 4), channel["display"], font=value_f, fill=ink)
        return

    lx = cx + r + 10
    ly = cy - 28
    if lx > W - 280:
        lx = cx - r - 250
    draw.text((lx, ly), channel["label"], font=lf, fill=ink)
    draw.text((lx, ly + 24), channel["display"], font=value_f, fill=ink)


def main() -> None:
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    title_f, sub_f = font(40), font(22)
    label_f, label_bold = font(LABEL_SIZE), font(LABEL_SIZE, bold=True)
    value_f = font(VALUE_SIZE)
    value_bold = font(VALUE_SIZE, bold=True)
    note_f, foot_f, chip_f = font(18), font(26), font(22, bold=True)

    draw.text((80, 40), "Where attention already lives", font=title_f, fill=INK)
    draw.text(
        (80, 95),
        "Bubble area = volume. Same type everywhere — Support is bold, ringed, and called out.",
        font=sub_f,
        fill=INK_MUTED,
    )

    bubbles = pack_bubbles(CHANNELS, 70, 155, 1780, 700)

    for b in sorted(bubbles, key=lambda b: b.r, reverse=True):
        if b.channel.get("highlight"):
            continue
        x0, y0, x1, y1 = b.cx - b.r, b.cy - b.r, b.cx + b.r, b.cy + b.r
        draw.ellipse((x0, y0, x1, y1), fill=BUBBLE_FILL, outline=BUBBLE_LINE, width=2)
        draw_label(draw, b.cx, b.cy, b.r, b.channel, label_f, label_bold, value_f)

    support = next(b for b in bubbles if b.channel.get("highlight"))
    pad = 14
    draw.ellipse(
        (support.cx - support.r - pad, support.cy - support.r - pad, support.cx + support.r + pad, support.cy + support.r + pad),
        outline=SUPPORT_RING,
        width=3,
    )
    draw.ellipse(
        (support.cx - support.r, support.cy - support.r, support.cx + support.r, support.cy + support.r),
        fill=SUPPORT_FILL,
        outline=SUPPORT_RING,
        width=4,
    )
    draw_label(draw, support.cx, support.cy, support.r, support.channel, label_f, label_bold, value_bold)

    chip_w, chip_h = 220, 44
    chip = (
        support.cx - chip_w / 2,
        support.cy + support.r + 14,
        support.cx + chip_w / 2,
        support.cy + support.r + 14 + chip_h,
    )
    draw.rounded_rectangle(chip, radius=22, fill=SUPPORT_RING)
    tw = draw.textlength("Support   2,500", font=chip_f)
    draw.text((support.cx - tw / 2, chip[1] + 10), "Support   2,500", font=chip_f, fill=CHIP_INK)

    draw.text(
        (80, 890),
        "Area scales with volume (Documentation ≈ 1500× Feedback / Discord). GitHub = 2,700.",
        font=note_f,
        fill=INK_MUTED,
    )
    draw.text((80, 940), FOOTNOTE, font=foot_f, fill=INK)
    img.save(OUT, "PNG")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()

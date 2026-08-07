#!/usr/bin/env python3
"""Raster preview of the support-channel heat map (for review / walkthrough).

The editable source of truth is support-channel-heatmap.pptx — regenerate that
with build_heatmap.py. This PNG mirrors layout for quick visual checks.
"""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent / "support-channel-heatmap-preview.png"

CHANNELS = [
    {"label": "Documentation", "value": 300_000, "display": "300,000"},
    {"label": "Help centers total articles views", "value": 152_000, "display": "152,000"},
    {"label": "Kapa", "value": 11_000, "display": "11,000"},
    {"label": "GitHub issues & discussions", "value": 2_500, "display": "2500"},
    {"label": "Support", "value": 2_500, "display": "2500", "bold": True},
    {"label": "Social channels", "value": 600, "display": "600"},
    {"label": "Feedback systems", "value": 200, "display": "200"},
    {"label": "Discord & community", "value": None, "display": "[TBD]"},
]

FOOTNOTE = "We redesigned one of the smallest, clearest surfaces first."
W, H = 1920, 1080
BG = (247, 245, 242)
INK = (26, 23, 20)
INK_MUTED = (92, 85, 76)
TILE_UNKNOWN = (228, 224, 218)


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def heat_color(t: float) -> tuple[int, int, int]:
    t = max(0.0, min(1.0, t))
    stops = [
        (0.0, (0xF0, 0xE6, 0xD8)),
        (0.35, (0xF2, 0xC4, 0x7A)),
        (0.7, (0xE8, 0x8B, 0x4A)),
        (1.0, (0xC4, 0x45, 0x2D)),
    ]
    for i in range(len(stops) - 1):
        t0, c0 = stops[i]
        t1, c1 = stops[i + 1]
        if t <= t1:
            u = 0.0 if t1 == t0 else (t - t0) / (t1 - t0)
            return (
                int(lerp(c0[0], c1[0], u)),
                int(lerp(c0[1], c1[1], u)),
                int(lerp(c0[2], c1[2], u)),
            )
    return stops[-1][1]


def contrast_ink(fill: tuple[int, int, int]) -> tuple[int, int, int]:
    r, g, b = fill[0] / 255, fill[1] / 255, fill[2] / 255
    lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return (255, 251, 246) if lum < 0.55 else INK


def heats() -> list[float | None]:
    known = [c["value"] for c in CHANNELS if c["value"] is not None]
    lo, hi = math.log10(min(known)), math.log10(max(known))
    out: list[float | None] = []
    for c in CHANNELS:
        if c["value"] is None:
            out.append(None)
        else:
            out.append((math.log10(c["value"]) - lo) / (hi - lo) if hi > lo else 0.5)
    return out


def font(size: int, bold: bool = False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def wrap(draw: ImageDraw.ImageDraw, text: str, fnt, max_w: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    cur = ""
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


def rounded_rect(draw, box, radius, fill):
    draw.rounded_rectangle(box, radius=radius, fill=fill)


def main() -> None:
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    title_f = font(40)
    sub_f = font(22)
    label_f = font(22)
    label_bold = font(22, bold=True)
    value_f = font(30)
    foot_f = font(26)
    legend_f = font(18)

    draw.text((86, 50), "Where attention already lives", font=title_f, fill=INK)
    draw.text(
        (86, 110),
        "Heat = relative volume across support-adjacent surfaces. Same type everywhere — Support is bold.",
        font=sub_f,
        fill=INK_MUTED,
    )

    cols, rows = 4, 2
    margin_x, margin_y = 86, 190
    gap = 20
    usable_w = W - margin_x * 2 - gap * (cols - 1)
    usable_h = 580 - gap * (rows - 1)
    tile_w = usable_w // cols
    tile_h = usable_h // rows

    for idx, (channel, heat) in enumerate(zip(CHANNELS, heats())):
        r, c = divmod(idx, cols)
        x = margin_x + c * (tile_w + gap)
        y = margin_y + r * (tile_h + gap)
        fill = TILE_UNKNOWN if heat is None else heat_color(heat)
        ink = contrast_ink(fill)
        rounded_rect(draw, (x, y, x + tile_w, y + tile_h), 18, fill)

        lf = label_bold if channel.get("bold") else label_f
        lines = wrap(draw, channel["label"], lf, tile_w - 48)
        block_h = len(lines) * 28 + 40
        ty = y + (tile_h - block_h) // 2
        for i, line in enumerate(lines):
            tw = draw.textlength(line, font=lf)
            draw.text((x + (tile_w - tw) / 2, ty + i * 28), line, font=lf, fill=ink)
        vw = draw.textlength(channel["display"], font=value_f)
        draw.text(
            (x + (tile_w - vw) / 2, ty + len(lines) * 28 + 8),
            channel["display"],
            font=value_f,
            fill=ink,
        )

    # Legend
    lx, ly, lw, lh = 86, 820, 600, 28
    for i in range(lw):
        t = i / (lw - 1)
        draw.line([(lx + i, ly), (lx + i, ly + lh)], fill=heat_color(t))
    draw.text((lx, ly + lh + 10), "Lower volume", font=legend_f, fill=INK_MUTED)
    hw = draw.textlength("Higher volume", font=legend_f)
    draw.text((lx + lw - hw, ly + lh + 10), "Higher volume", font=legend_f, fill=INK_MUTED)

    draw.text((86, 940), FOOTNOTE, font=foot_f, fill=INK)
    img.save(OUT, "PNG")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()

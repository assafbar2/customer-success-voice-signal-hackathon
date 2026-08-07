#!/usr/bin/env python3
"""Raster preview of the sized (treemap) support-channel heat map."""

from __future__ import annotations

import math
from dataclasses import dataclass
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
]
DISCORD = {"label": "Discord & community", "value": None, "display": "[TBD]"}
FOOTNOTE = "We redesigned one of the smallest, clearest surfaces first."

W, H = 1920, 1080
BG = (247, 245, 242)
INK = (26, 23, 20)
INK_MUTED = (92, 85, 76)
TILE_UNKNOWN = (228, 224, 218)
GAP = 3
LABEL_SIZE = 20
VALUE_SIZE = 26


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


@dataclass
class Rect:
    x: float
    y: float
    w: float
    h: float


def sized_layout(channels, x, y, w, h):
    by_name = {c["label"]: c for c in channels}
    total = sum(c["value"] for c in channels)
    doc = by_name["Documentation"]
    help_ = by_name["Help centers total articles views"]
    small = sorted(
        [c for c in channels if c["label"] not in (doc["label"], help_["label"])],
        key=lambda c: c["value"],
        reverse=True,
    )

    doc_w = w * (doc["value"] / total)
    right_x, right_w = x + doc_w, w - doc_w
    right_total = total - doc["value"]
    help_h = h * (help_["value"] / right_total)
    small_y, small_h = y + help_h, h - help_h
    small_total = sum(c["value"] for c in small)

    out = [
        (doc, Rect(x, y, doc_w, h)),
        (help_, Rect(right_x, y, right_w, help_h)),
    ]
    cx = right_x
    for i, ch in enumerate(small):
        tw = right_w * (ch["value"] / small_total)
        if i == len(small) - 1:
            tw = right_x + right_w - cx
        out.append((ch, Rect(cx, small_y, tw, small_h)))
        cx += tw
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


def draw_tile(base: Image.Image, rect: Rect, channel, fill, label_f, label_bold, value_f):
    draw = ImageDraw.Draw(base)
    inset = min(GAP / 2, max(rect.w / 8, 0), max(rect.h / 8, 0))
    x0 = int(rect.x + inset)
    y0 = int(rect.y + inset)
    x1 = int(rect.x + rect.w - inset)
    y1 = int(rect.y + rect.h - inset)
    if x1 <= x0 or y1 <= y0:
        draw.rectangle(
            (int(rect.x), int(rect.y), int(rect.x + max(rect.w, 1)), int(rect.y + max(rect.h, 1))),
            fill=fill,
        )
        return

    # Paint + label inside a clipped tile buffer so text cannot spill.
    tw_box, th_box = max(x1 - x0, 1), max(y1 - y0, 1)
    tile = Image.new("RGB", (tw_box, th_box), fill)
    tdraw = ImageDraw.Draw(tile)
    ink = contrast_ink(fill)
    lf = label_bold if channel.get("bold") else label_f
    lines = wrap(tdraw, channel["label"], lf, max(tw_box - 8, 2))
    line_h = LABEL_SIZE + 3
    max_lines = max(int((th_box - VALUE_SIZE - 4) // line_h), 0)
    lines = lines[:max_lines]
    show_value = th_box >= VALUE_SIZE + 2 and tw_box >= 36
    block_h = len(lines) * line_h + (VALUE_SIZE + 4 if show_value else 0)
    ty = max((th_box - block_h) / 2, 1)
    for i, line in enumerate(lines):
        tw = tdraw.textlength(line, font=lf)
        tdraw.text(((tw_box - tw) / 2, ty + i * line_h), line, font=lf, fill=ink)
    if show_value:
        vw = tdraw.textlength(channel["display"], font=value_f)
        tdraw.text(
            ((tw_box - vw) / 2, ty + len(lines) * line_h + 2),
            channel["display"],
            font=value_f,
            fill=ink,
        )
    base.paste(tile, (x0, y0))


def main() -> None:
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    title_f, sub_f = font(40), font(22)
    label_f = font(LABEL_SIZE)
    label_bold = font(LABEL_SIZE, bold=True)
    value_f = font(VALUE_SIZE)
    note_f, foot_f = font(18), font(26)

    draw.text((80, 40), "Where attention already lives", font=title_f, fill=INK)
    draw.text(
        (80, 95),
        "Tile size = volume (linear). Color reinforces the same scale. Same type everywhere — Support is bold.",
        font=sub_f,
        fill=INK_MUTED,
    )

    origin_x, origin_y = 80.0, 160.0
    region_w, region_h = 1760.0, 700.0
    discord_w = 100.0
    tree_w = region_w - discord_w - GAP

    values = [c["value"] for c in CHANNELS]
    lo, hi = math.log10(min(values)), math.log10(max(values))

    for channel, rect in sized_layout(CHANNELS, origin_x, origin_y, tree_w, region_h):
        t = (math.log10(channel["value"]) - lo) / (hi - lo) if hi > lo else 0.5
        draw_tile(img, rect, channel, heat_color(t), label_f, label_bold, value_f)

    draw_tile(
        img,
        Rect(origin_x + tree_w + GAP, origin_y, discord_w, region_h),
        DISCORD,
        TILE_UNKNOWN,
        label_f,
        label_bold,
        value_f,
    )

    draw = ImageDraw.Draw(img)
    draw.text(
        (80, 890),
        "Area is linear with volume (Documentation ≈ 1500× Feedback). Discord is unmeasured — not on the size scale.",
        font=note_f,
        fill=INK_MUTED,
    )
    draw.text((80, 940), FOOTNOTE, font=foot_f, fill=INK)
    img.save(OUT, "PNG")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()

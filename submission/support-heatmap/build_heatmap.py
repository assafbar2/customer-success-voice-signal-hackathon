#!/usr/bin/env python3
"""Build an editable PowerPoint heat map of support-adjacent surfaces.

All channel labels use the same font and size; only "Support" is bold.
Cell fill encodes relative volume (heat). Native shapes + text so PowerPoint
users can edit colors, copy, and numbers without rebuilding.
"""

from __future__ import annotations

import math
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Emu, Inches, Pt

OUT = Path(__file__).resolve().parent / "support-channel-heatmap.pptx"

# Volume drives heat. Discord is TBD → treated as unknown (neutral tile).
CHANNELS: list[dict] = [
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

# Light slide + amber→deep-coral heat (classic heat map, PPT-friendly).
BG = RGBColor(0xF7, 0xF5, 0xF2)
INK = RGBColor(0x1A, 0x17, 0x14)
INK_MUTED = RGBColor(0x5C, 0x55, 0x4C)
TILE_UNKNOWN = RGBColor(0xE4, 0xE0, 0xDA)


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def heat_color(t: float) -> RGBColor:
    """Map 0..1 → pale sand → amber → deep coral."""
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
            r = int(lerp(c0[0], c1[0], u))
            g = int(lerp(c0[1], c1[1], u))
            b = int(lerp(c0[2], c1[2], u))
            return RGBColor(r, g, b)
    return RGBColor(*stops[-1][1])


def contrast_ink(fill: RGBColor) -> RGBColor:
    # Relative luminance; dark text on pale tiles, light text on hot tiles.
    r, g, b = fill[0] / 255, fill[1] / 255, fill[2] / 255
    lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return RGBColor(0xFF, 0xFB, 0xF6) if lum < 0.55 else INK


def normalized_heats(items: list[dict]) -> list[float | None]:
    known = [c["value"] for c in items if c["value"] is not None]
    # Log scale so Documentation does not flatten everything else.
    lo = math.log10(min(known))
    hi = math.log10(max(known))
    out: list[float | None] = []
    for c in items:
        if c["value"] is None:
            out.append(None)
        else:
            out.append((math.log10(c["value"]) - lo) / (hi - lo) if hi > lo else 0.5)
    return out


def set_run(paragraph, text: str, *, size_pt: float, bold: bool, color: RGBColor) -> None:
    run = paragraph.add_run()
    run.text = text
    run.font.name = "Calibri"
    run.font.size = Pt(size_pt)
    run.font.bold = bold
    run.font.color.rgb = color


def add_tile(slide, left, top, width, height, channel: dict, heat: float | None) -> None:
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.adjustments[0] = 0.08
    fill = shape.fill
    fill.solid()
    if heat is None:
        rgb = TILE_UNKNOWN
    else:
        rgb = heat_color(heat)
    fill.fore_color.rgb = rgb
    shape.line.fill.background()

    ink = contrast_ink(rgb)
    tf = shape.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.auto_size = None
    shape.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    tf.anchor = MSO_ANCHOR.MIDDLE

    # Same type treatment for every label; Support alone is bold.
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.space_after = Pt(4)
    set_run(
        p,
        channel["label"],
        size_pt=14,
        bold=bool(channel.get("bold")),
        color=ink,
    )

    p2 = tf.add_paragraph()
    p2.alignment = PP_ALIGN.CENTER
    set_run(p2, channel["display"], size_pt=18, bold=False, color=ink)


def add_legend(slide, left, top, width, height) -> None:
    # Continuous strip via thin adjacent rects (still native shapes → editable).
    n = 24
    cell_w = width // n
    for i in range(n):
        t = i / (n - 1)
        rect = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            left + cell_w * i,
            top,
            cell_w + Emu(2000),  # slight overlap to avoid hairline gaps
            height,
        )
        rect.fill.solid()
        rect.fill.fore_color.rgb = heat_color(t)
        rect.line.fill.background()

    label_w = Inches(1.5)
    low = slide.shapes.add_textbox(left, top + height + Inches(0.08), label_w, Inches(0.28))
    p = low.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT
    set_run(p, "Lower volume", size_pt=10, bold=False, color=INK_MUTED)

    high = slide.shapes.add_textbox(
        left + width - label_w, top + height + Inches(0.08), label_w, Inches(0.28)
    )
    p = high.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.RIGHT
    set_run(p, "Higher volume", size_pt=10, bold=False, color=INK_MUTED)


def build() -> Path:
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank

    # Background
    bg = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), prs.slide_width, prs.slide_height
    )
    bg.fill.solid()
    bg.fill.fore_color.rgb = BG
    bg.line.fill.background()

    # Title
    title = slide.shapes.add_textbox(Inches(0.6), Inches(0.35), Inches(12.1), Inches(0.45))
    p = title.text_frame.paragraphs[0]
    set_run(p, "Where attention already lives", size_pt=22, bold=False, color=INK)

    subtitle = slide.shapes.add_textbox(Inches(0.6), Inches(0.78), Inches(12.1), Inches(0.35))
    p = subtitle.text_frame.paragraphs[0]
    set_run(
        p,
        "Heat = relative volume across support-adjacent surfaces. Same type everywhere — Support is bold.",
        size_pt=12,
        bold=False,
        color=INK_MUTED,
    )

    heats = normalized_heats(CHANNELS)
    cols, rows = 4, 2
    margin_x = Inches(0.6)
    margin_y = Inches(1.35)
    gap = Inches(0.14)
    usable_w = prs.slide_width - margin_x * 2 - gap * (cols - 1)
    usable_h = Inches(4.15) - gap * (rows - 1)
    tile_w = usable_w // cols
    tile_h = usable_h // rows

    for idx, (channel, heat) in enumerate(zip(CHANNELS, heats)):
        r, c = divmod(idx, cols)
        left = margin_x + (tile_w + gap) * c
        top = margin_y + (tile_h + gap) * r
        add_tile(slide, left, top, tile_w, tile_h, channel, heat)

    add_legend(slide, Inches(0.6), Inches(5.75), Inches(4.2), Inches(0.22))

    foot = slide.shapes.add_textbox(Inches(0.6), Inches(6.55), Inches(12.1), Inches(0.45))
    p = foot.text_frame.paragraphs[0]
    set_run(p, FOOTNOTE, size_pt=14, bold=False, color=INK)

    prs.save(OUT)
    return OUT


if __name__ == "__main__":
    path = build()
    print(f"Wrote {path}")

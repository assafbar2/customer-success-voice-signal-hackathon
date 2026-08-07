# Support-channel heat map

Editable PowerPoint slide of relative volume across support-adjacent surfaces.

## Files

| File | Role |
|------|------|
| `support-channel-heatmap.pptx` | **Source of truth** — native shapes + text; open in PowerPoint and edit freely |
| `build_heatmap.py` | Regenerates the `.pptx` |
| `support-channel-heatmap-preview.png` | Quick visual preview (not the editable artifact) |
| `build_preview.py` | Regenerates the PNG preview |

## Design rules

- Every channel label uses the same font family and size
- Only **Support** is bold
- Tile color = log-scaled volume (Documentation hottest → Feedback coolest)
- Discord stays neutral (`[TBD]`)
- Footnote: *We redesigned one of the smallest, clearest surfaces first.*

## Regenerate

```bash
pip install python-pptx pillow
python3 build_heatmap.py
python3 build_preview.py
```

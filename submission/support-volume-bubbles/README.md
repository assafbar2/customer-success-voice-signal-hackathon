# Support-volume bubble chart

Editable PowerPoint slide — bubble **area** encodes volume across support-adjacent surfaces.

## Files

| File | Role |
|------|------|
| `support-volume-bubbles.pptx` | **Source of truth** — native ovals + text; edit in PowerPoint |
| `build_bubbles.py` | Regenerates the `.pptx` |
| `support-volume-bubbles-preview.png` | Quick visual preview |
| `build_bubbles_preview.py` | Regenerates the PNG preview |

## Data

| Channel | Volume |
|---------|-------:|
| Documentation | 300,000 |
| Help centers total articles views | 152,000 |
| Kapa | 11,000 |
| GitHub issues & discussions | 2,700 |
| Support | 2,500 |
| Social channels | 600 |
| Discord & community | 200 |
| Feedback systems | 200 |

## Design

- Bubble area ∝ volume (radius ∝ √value)
- Same type treatment on every label
- **Support** highlighted three ways: bold type, amber fill + ring, callout chip with **Support 2,500**
- Footnote: *We redesigned one of the smallest, clearest surfaces first.*

## Regenerate

```bash
pip install python-pptx pillow
python3 build_bubbles.py
python3 build_bubbles_preview.py
```

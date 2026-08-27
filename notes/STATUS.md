# Status (operator log — not the product pitch)

See [`SUBMIT.md`](SUBMIT.md) for Devpost / awesome-list / MVF / video upload.

| Field | Value |
| --- | --- |
| Last update | 2026-08-27 |
| Product | Stage Manager — `skills/customer-success-voice-signal/` |
| Judge site | https://assafbar2.github.io/customer-success-voice-signal-hackathon/ |
| Live ladder | `research/calle-api-notes.md` |
| Evidence | `submission/evidence/` (redacted) |

## Live outcomes

| Cue | Best curtain-up | Also observed |
| --- | --- | --- |
| `stuck_support` | Decision **1** take over in chat (2026-08-12: stage code 4821 + “1”) | Voicemail → `no_answer`; first map `unclear` (paraphrased `decision`) |
| `agent_needs_decision` | Decision **1** approve A | Prior `unclear` |

## Operator leftovers

- **YouTube/Vimeo:** upload `submission/demo-reel/stage-manager-demo.mp4` (2:08). GitHub file ≠ Devpost.
- **Awesome-list PR:** run `bash submission/awesome-list/open-pr.sh` on a laptop; paste URL into [`../submission/awesome-list/STATUS.md`](../submission/awesome-list/STATUS.md). Cloud cannot fork CALLE-AI.
- **Devpost form:** Join if needed, then paste from [`../submission/devpost.md`](../submission/devpost.md). You submit.
- **GitHub Social preview:** Settings → General → upload `site/og.png` (API 422; not admin). Pages `og.png` is already live.
- Slack/GitHub adapters remain a **stab** — do not fire

## Done this sitting (2026-08-27)

- PR #18 merged to `main` (judge package).
- MVF survey **submitted** — edit/confirm: see [`../submission/mvf-feedback.md`](../submission/mvf-feedback.md).
- Skill validated (93 tests, typecheck, dress rehearsal, `POST /cue`).
- Awesome-list packaging validated against upstream (`validate_repository.py` passed; skill `README.md` omitted).

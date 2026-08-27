# Stage Manager

**When the renewal goes quiet, page the owner — not the customer.**

Every company pages an engineer when a server goes down. Almost nobody pages the human who owns the account. Slack hides the signal. PagerDuty phones you to *acknowledge* an alert. **Ack is not a decision.**

[Live site](https://assafbar2.github.io/customer-success-voice-signal-hackathon/) · [Skill](skills/customer-success-voice-signal/) · [CALL-E hackathon](https://call-e.devpost.com/)

![Stage Manager dress rehearsal — no ring, no API key](site/assets/stage-manager-loop.gif)

Stage Manager is a CALL-E skill. When a named account hits a high-risk **cue**, it rings the **CS owner only** (never the customer) with a ~60s closed-set line reading — say **1 / 2 / 3**. The decision is written to a **prompt book** (audit log) and an **action intent** for the next system. Dress rehearsal is the default: judges run the full loop with no API key.

---

## Why this exists

| | Incident pager | Stage Manager |
| --- | --- | --- |
| Who | On-call engineer | **CS owner** of a named account |
| Output | Acknowledge / escalate | **Closed-set CS decision** + action intent |
| Audit | Incident timeline | Prompt book + show report |
| Default | Live page | **Dress rehearsal** — live needs `--live` + `PLACES` |

Phone still cuts through. Only if it is rare, short, structured, and aimed at the firefighter — not a spam dialer to the building.

## Four cues, one engine

1. **stuck_support** — take over in chat · assign SE · snooze 2 hours
2. **agent_needs_decision** — approve A · approve B · escalate
3. **sla_risk** — own the ticket · page backup · accept risk
4. **health_onboarding** — book SE · watchlist · flag churn

Cue in (fixture, stdin, or `POST /cue`) → call sheet (owned? quiet hours? owner budget?) → dress rehearsal or curtain-up → spoken **stage code** (identity) → 1/2/3 → prompt book + action intent.

## How judges run this

```bash
git clone https://github.com/assafbar2/customer-success-voice-signal-hackathon.git
cd customer-success-voice-signal-hackathon/skills/customer-success-voice-signal
npm install
npm test && npm run typecheck

# Dress rehearsal — default, no ring, no CALL-E key
npm run signal -- --fixture stuck_support_acme.json

# Same engine, webhook-shaped inbound
npm run signal -- --stdin < events/webhook_stuck_support.json

# HTTP listener (deployable)
npm run serve-cue &
curl -sS -X POST http://127.0.0.1:8787/cue \
  -H 'content-type: application/json' \
  -d @events/webhook_stuck_support.json

# Decision → local handoff (Slack/GitHub adapters are a stab — do not fire)
npm run apply-action -- --last --dry-run
```

| Exit | Meaning |
| --- | --- |
| 0 | Ok |
| 2 | HOLD (policy / live gate / quiet hours / owner budget) |
| 3 | Failure |

Curtain-up (operator only): copy `.env.example` → `.env`, set `CALLE_API_KEY`, `CS_OWNER_E164`, then `npm run signal -- --fixture stuck_support_acme.json --live PLACES`. Never commit `.env`.

**Safety:** CS owner only · dress rehearsal default · per-owner call budget · timezone-aware quiet hours · fixture phones never dialed live · identity stage-code before 1/2/3 · HOLD never poisons cue dedupe.

## Live, honestly

Real curtain-up against CALL-E — misses included.

| Cue | Best result | Also observed |
| --- | --- | --- |
| `stuck_support` | Line reading **1** — take over in chat | Voicemail → `no_answer`; paraphrased `decision` first mapped `unclear` |
| `agent_needs_decision` | Line reading **1** — approve A | Earlier `unclear` captures |

Redacted rows: [`submission/evidence/`](submission/evidence/). Full ladder: [`research/calle-api-notes.md`](research/calle-api-notes.md).

## Demo

[`submission/demo-reel/stage-manager-demo.mp4`](submission/demo-reel/stage-manager-demo.mp4) · on the [judge site](https://assafbar2.github.io/customer-success-voice-signal-hackathon/#demo)

CLI is a real screen recording. Call beat is the 2026-08-12 live transcript (handset audio lives on the CS owner’s phone). Slack does not fire.

## More

| | |
| --- | --- |
| Product | [`skills/customer-success-voice-signal/`](skills/customer-success-voice-signal/) · [`SKILL.md`](skills/customer-success-voice-signal/SKILL.md) |
| Architecture | [`docs/03-architecture-flow.md`](docs/03-architecture-flow.md) |
| PRD | [`docs/02-prd.md`](docs/02-prd.md) |
| License | [MIT](LICENSE) |

---

*No customers were called in the making of this demo.*

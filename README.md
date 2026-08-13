# customer-success-voice-signal-hackathon

**Product:** Stage Manager · skill id [`customer-success-voice-signal`](skills/customer-success-voice-signal/)  
**Hackathon:** [CALL-E: Your Code Is Calling](https://call-e.devpost.com/) · aiming **Most Practical**  
**Live site:** https://assafbar2.github.io/customer-success-voice-signal-hackathon/

> Every company pages an engineer when a server goes down. Nobody pages the human who owns the renewal when the account goes quiet.
>
> *PagerDuty phones you to acknowledge an alert. Ack is not a decision.*

When a named account hits a high-risk **cue** (trigger event), **Stage Manager** rings the **CS owner** (never the customer) with a ~60s closed-set line reading — a 1/2/3 decision menu. The decision is **state** in the prompt book (NDJSON audit log) — and an **action intent** for the next system (ticket / CRM / Slack), not a chat ack.

---

## Why this vs paging tools

| | PagerDuty / Opsgenie-style page | Stage Manager |
| --- | --- | --- |
| Who | On-call engineer | **CS owner** of a named account |
| Output | Acknowledge / escalate | **Closed-set CS decision** + **action intent** |
| Audit | Incident timeline | Prompt book + show report + `data/actions/` |
| Default | Live page | **Dress rehearsal** (dry-run) — live needs `--live` + `PLACES` |

Lane check: awesome-list phone agents already cover deploy approvals; **B2B customer success / renewal** is still open.

## Judge site

- Source: [`site/`](site/) via **GitHub Pages** (GitHub Actions)  
- URL: https://assafbar2.github.io/customer-success-voice-signal-hackathon/  
- Set the GitHub repo **Homepage** field to that URL (not the old Vercel 404)

## How judges run this

```bash
git clone https://github.com/assafbar2/customer-success-voice-signal-hackathon.git
cd customer-success-voice-signal-hackathon/skills/customer-success-voice-signal
npm install
npm test && npm run typecheck

# Inbound seam — webhook-shaped JSON (not fixtures-only)
npm run signal -- --stdin < events/webhook_stuck_support.json

# Or HTTP listener (deployable — same engine)
npm run serve-cue &
curl -sS -X POST http://127.0.0.1:8787/cue \
  -H 'content-type: application/json' \
  -d @events/webhook_stuck_support.json

# Decision → system handoff (local receipt by default)
npm run apply-action -- --last --dry-run
npm run apply-action -- --last

# Live adapters (env-gated; placeholder HOLDs — see .env.example)
npm run apply-action -- --last --adapter slack     # Slack-shaped webhook POST {text}
npm run apply-action -- --last --adapter github    # comment on GITHUB_REPO#GITHUB_ISSUE

# Curtain-up — operator only
# https://dashboard.heycall-e.com/account/api-keys
# cp .env.example .env → CALLE_API_KEY, CS_OWNER_E164, SIGNAL_CONFIRM=PLACES
# npm run signal -- --fixture stuck_support_acme.json --live PLACES
```

| Exit | Meaning |
| --- | --- |
| 0 | Ok |
| 2 | HOLD (policy / live gate / quiet hours / owner budget) |
| 3 | Failure |

**Seam:** `POST /cue` or stdin → phone decision → `data/actions/pending/*.json` → `apply-action` → receipt. **Live adapters:** Slack-shaped webhook (`--adapter slack`) · GitHub issue comment (`--adapter github`) — env-gated, placeholder values HOLD. Zendesk / Salesforce shapes documented at the seam. See [`references/action-intents.md`](skills/customer-success-voice-signal/references/action-intents.md).

**Safety:** CS owner only · dress rehearsal (dry-run) default · per-owner call budget · owner/env quiet-hours precedence · untrusted cue wrapping · concurrent dial lock · house dark (quiet hours) timezone-aware · HOLD/failure never poison cue dedupe · fixture phones never dialed live · SDK `failureCode`/`completionConfidence` preferred · identity stage-code read-back before 1/2/3.

Live ladder (including voicemail / unclear): [`research/calle-api-notes.md`](research/calle-api-notes.md) · redacted rows: [`submission/evidence/`](submission/evidence/) · SDK notes: [`skills/customer-success-voice-signal/references/calle-sdk.md`](skills/customer-success-voice-signal/references/calle-sdk.md) · MVF: [`submission/mvf-feedback.md`](submission/mvf-feedback.md)

## Docs map

| Path | Purpose |
| --- | --- |
| [skills/customer-success-voice-signal/](skills/customer-success-voice-signal/) | **Stage Manager skill** |
| [docs/02-prd.md](docs/02-prd.md) | Product decisions |
| [docs/03-architecture-flow.md](docs/03-architecture-flow.md) | As-built flow |
| [docs/06-the-house-design-brief.md](docs/06-the-house-design-brief.md) | **The House** — living swarm of Sentry customer agents (proposal; review before build) |
| [submission/awesome-list/PACKAGING.md](submission/awesome-list/PACKAGING.md) | Awesome-list PR packaging |
| [submission/PRE-SUBMIT.md](submission/PRE-SUBMIT.md) | Pre-submit: video · GIF · awesome-list · MVF · Devpost |
| [submission/mvf-feedback.md](submission/mvf-feedback.md) | Most Valuable Feedback survey draft |
| [submission/gif-notes.md](submission/gif-notes.md) | Terminal GIF capture notes |
| [skills/customer-success-voice-signal/references/calle-sdk.md](skills/customer-success-voice-signal/references/calle-sdk.md) | SDK fields + identity read-back |
| [notes/STATUS.md](notes/STATUS.md) | Operator status (not a pitch deck) |
| [LICENSE](LICENSE) | MIT |

## Official links

- Devpost: https://call-e.devpost.com/  
- Rules: https://call-e.devpost.com/rules  
- **CALL-E API keys:** https://dashboard.heycall-e.com/account/api-keys  
- **Submit list PR:** https://github.com/CALLE-AI/awesome-phone-call-agents  
- Extra calls form: https://forms.gle/EPQttEZ1rkW8iq9q6  

## Submit checklist

Master pre-submit (video · GIF · awesome-list · **MVF** · Devpost):  
[`submission/PRE-SUBMIT.md`](submission/PRE-SUBMIT.md)

- [x] Skill + dress rehearsal + curtain-up path
- [x] Judge site on GitHub Pages
- [ ] Terminal GIF — [`submission/gif-notes.md`](submission/gif-notes.md)
- [ ] Awesome-list PR — [`submission/awesome-list/PACKAGING.md`](submission/awesome-list/PACKAGING.md) (MVF is a gate)
- [ ] Demo video — [`submission/video-script.md`](submission/video-script.md)
- [ ] **MVF survey** — paste [`submission/mvf-feedback.md`](submission/mvf-feedback.md) on Devpost
- [ ] Devpost form — [`submission/devpost.md`](submission/devpost.md)

## Judging criteria (Devpost)

1. Real World Impact
2. Quality of the Idea
3. Technical Implementation (CALL-E at runtime)
4. Product Experience & Demo (≤3 min video)

Also submit **Most Valuable Feedback** (separate survey) — draft in repo.

---

*No customers were called in the making of this demo.*

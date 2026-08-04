# Action intents — decision → system handoff

Stage Manager captures a **closed-set CS decision** on the phone, then emits an **action intent**: the contract the next system executes.

PagerDuty-style tools often stop at **acknowledge**. We stop at a **decision**, then make the next system move **explicit and executable**. Two adapters are live (Slack-shaped webhook, GitHub issue comment); Zendesk / Salesforce shapes are documented at the seam — never claimed as wired.

## Seam (end-to-end, judge-visible)

```text
Webhook-shaped JSON / fixture / stdin / POST /cue
        ↓
  Stage Manager (policy → dress rehearsal | curtain-up)
        ↓
  Prompt book + show report
        ↓
  data/actions/pending/<intent_id>.json     ← action intent
        ↓
  npm run apply-action -- --last --dry-run  ← prove the handoff
        ↓
  data/actions/executed/<receipt>.json      ← receipt (local, or live-adapter send)
```

The **JSON shape is the product seam**. Live adapters ride it:

```bash
# Slack-shaped webhook — POST {text} to SLACK_WEBHOOK_URL
# (any {text}-accepting endpoint works; webhook.site is fine for a demo)
npm run apply-action -- --last --adapter slack

# GitHub issue comment — POST {body} to GITHUB_REPO#GITHUB_ISSUE (GITHUB_TOKEN)
npm run apply-action -- --last --adapter github

# Both honor --dry-run (prints exact payload, no network)
# Unset/placeholder env → HOLD (exit 2) — never a silent no-op
```

## Run it

```bash
cd skills/customer-success-voice-signal
npm install

# 1a) Inbound cue via stdin (webhook-shaped — not fixtures-only)
npm run signal -- --stdin < events/webhook_stuck_support.json

# 1b) Or inbound via HTTP listener (same engine — deployable)
npm run serve-cue &
curl -sS -X POST http://127.0.0.1:8787/cue \
  -H 'content-type: application/json' \
  -d @events/webhook_stuck_support.json

# 2) Inspect pending action intent
ls data/actions/pending/
npm run apply-action -- --last --dry-run

# 3) Local “execute” (no external call — writes a receipt)
npm run apply-action -- --last

# 4) Or send for real via a live adapter (env-gated)
npm run apply-action -- --last --adapter slack
```

### HTTP cue listener

`npm run serve-cue` binds `POST /cue` (and `GET /health`) with zero extra deps.

| Query / env | Effect |
| --- | --- |
| (none) | Dress rehearsal (default) |
| `?dry_run=1` | Force dress rehearsal |
| `?live=1&confirm=PLACES` | Curtain-up **only if** `CUE_ALLOW_LIVE=1` is set — otherwise **403 HOLD** (webhook cannot arm itself) |
| `CUE_WEBHOOK_SECRET` | Required for non-loopback bind; Bearer / `X-Cue-Secret` |
| `CUE_ALLOW_LIVE=1` | Operator arming switch for HTTP live |

Judge demo story: **curl → dress rehearsal → apply-action --adapter slack**. Live phone still needs a separate human arm (`CUE_ALLOW_LIVE` + CLI/`PLACES` semantics). See [safety.md](safety.md).
## What an intent contains

| Field | Meaning |
| --- | --- |
| `action` | Stable verb (`assign_owner_to_ticket_and_post_note`, …) |
| `adapter` | Primary target (`zendesk_ticket_note`, `salesforce_task`, `slack_webhook`, `internal_queue`) |
| `adapters_planned` | Full Monday-morning adapter family |
| `payload` | Account, ticket, owner, `call_run_id`, optional `follow_up_at` |
| `status` | `pending` → `dry_run_printed` / `executed_local` |

HOLD / failure / unclear / no_answer do **not** emit intents — only option `1` / `2` / `3`.

## Honesty

- `--dry-run` and local apply **never** call external APIs.
- Receipts say `effect: "local_receipt"` unless a live adapter actually posted —
  then `slack_webhook_posted` / `github_comment_posted` with the HTTP status.
- Unset or placeholder adapter env HOLDs (exit 2) instead of pretending.
- Zendesk / Salesforce remain documented shapes, not wired adapters.

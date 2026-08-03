# Action intents — decision → system handoff

Stage Manager captures a **closed-set CS decision** on the phone, then emits an **action intent**: the contract a Zendesk / Salesforce / Slack adapter would execute next.

PagerDuty-style tools often stop at **acknowledge**. We stop at a **decision**, then make the next system move **explicit and executable** — without pretending a live CRM write happened in this POC.

## Seam (end-to-end, judge-visible)

```text
Webhook-shaped JSON / fixture / stdin
        ↓
  Stage Manager (policy → dress rehearsal | curtain-up)
        ↓
  Prompt book + show report
        ↓
  data/actions/pending/<intent_id>.json     ← action intent
        ↓
  npm run apply-action -- --last --dry-run  ← prove the handoff
        ↓
  data/actions/executed/<receipt>.json      ← local POC receipt
```

Live CRM/ticket adapters are the next step. The **JSON shape is the product seam**.

## Run it

```bash
cd skills/customer-success-voice-signal
npm install

# 1) Inbound cue (webhook-shaped — not fixtures-only)
npm run signal -- --stdin < events/webhook_stuck_support.json

# 2) Inspect pending action intent
ls data/actions/pending/
npm run apply-action -- --last --dry-run

# 3) Local “execute” (still no Zendesk/Slack call — writes a receipt)
npm run apply-action -- --last
```

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
- Receipts say `effect: "local_receipt"`.
- Docs and CLI state that CRM writeback is an adapter away — not already wired.

---
name: customer-success-voice-signal
description: Stage Manager skill that cues CALL-E to ring the CS owner (never the customer) when a named account hits stuck support, SLA risk, agent-needs-decision, or health/onboarding stall — dress rehearsal by default, curtain-up only with --live and PLACES.
license: MIT
---

# customer-success-voice-signal (Stage Manager)

When a **named account** hits a high-risk moment, the **Stage Manager** cues CALL-E to ring the **CS owner only** with a short brief and closed-set line readings (1/2/3). The structured decision lands in the **prompt book** and **show report**.

**Not:** a customer dialer. **Never** call the customer in MVP.

## Glossary (hard vocabulary)

| Term | Meaning |
| --- | --- |
| **Dress rehearsal** | Dry-run. Default. No ring. Cue-history not appended. |
| **Curtain up** | Live CALL-E call. Requires `--live` **and** type/env `PLACES`. |
| **Cue** | A trigger event (`stuck_support`, `sla_risk`, `agent_needs_decision`, `health_onboarding`). |
| **Cue sheet / call sheet** | Who we may ring (CS owner E.164 allowlist). |
| **Line readings** | Closed-set options 1 / 2 / 3 spoken on the call. |
| **Prompt book** | NDJSON audit of cues and decisions (`data/prompt-book.ndjson`). |
| **Show report** | Markdown writeback summary (`data/show-report.md`). |
| **House dark** | Quiet hours. Enforced on curtain-up only. |
| **HOLD** | Policy stop — no live ring (exit code 2). |

## When to use

- Support/AI path stuck on a CS-owned account
- SLA breach imminent on a named account
- An agent emits `needs_human` with options
- Health or onboarding stall before renewal

## When not to use

- Calling the end customer
- Medical, emergency, legal, or harassment contexts
- Guessing phone numbers or skipping consent / opt-in
- Curtain-up without explicit `--live` + `PLACES`

## How to run

```bash
cd skills/customer-success-voice-signal
npm install

# Dress rehearsal (default — no secrets needed for dial)
npm run signal -- --fixture stuck_support_acme.json

# List cues
npm run signal -- --list

# Curtain-up (real ring) — parent/operator only
# Requires CALLE_API_KEY, CS_OWNER_E164, and PLACES
npm run signal -- --fixture stuck_support_acme.json --live PLACES
```

## Safety

Read [references/safety.md](references/safety.md) and [references/auth-and-keys.md](references/auth-and-keys.md).

- Callee is **CS owner only**
- Fixture phones are placeholders (`+15555550100`) — curtain-up rejects them
- `CS_OWNER_E164` from env overrides owner phone on curtain-up
- House dark enforced only when the curtain is up
- Dress rehearsal does **not** append cue-history (demos re-run cleanly)

## Exit codes

| Code | Meaning |
| --- | --- |
| 0 | Ok — dress rehearsal or curtain-up completed |
| 2 | HOLD — policy / live gate / house dark / placeholder |
| 3 | Failure — bad fixture, missing key, CALL-E error |

## Writeback

- Prompt book: `data/prompt-book.ndjson`
- Show report: `data/show-report.md`
- Cue history (curtain-up only): `data/cue-history.ndjson`

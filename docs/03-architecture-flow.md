# Architecture — Stage Manager

What was built. Theater language lives in call copy and the CLI; this page stays structural.

---

## 1. System context

```text
Cue (fixture | stdin | POST /cue)
        │
        ▼
┌───────────────────────────────────┐
│  customer-success-voice-signal    │
│  npm run signal  /  serve-cue     │
└───────────────┬───────────────────┘
                │
     ┌──────────┴──────────┐
     │ dress rehearsal     │ curtain-up (--live + PLACES)
     │ default, no ring    │ CALL-E: create → persist id → waitForResult
     └──────────┬──────────┘
                ▼
         CS owner phone only
                ▼
     prompt book + show report
     + action intent (local; Slack/GitHub stab — do not fire)
```

**Never in MVP:** CALL-E → customer. No required Slack. No DB. No demo UI app.

---

## 2. End-to-end flow

```text
normalize  →  AccountEvent
     │
shouldRing →  HOLD? ──yes──► writeback (hold) → exit 2
     │ no
buildCallIntent (task + line readings 1/2/3 + stage code)
     │
     ├─ dress rehearsal (simulate option 1)
     └─ curtainUp: calls.create → persist open-calls/<id>.json → waitForResult
              (--from-call remaps an existing id, no new ring)
     │
toDecision (option_id / structured / failureCode / transcript)
     │
writeback → prompt-book.ndjson · show-report.md · cue-history (live only)
     │
action intent → data/actions/pending/ → apply-action --dry-run
```

### Call beat (what the CS owner hears)

```text
Ring → "Hi {name}. Stage Manager. You're up for {account}."
     → Stage code read-back (binds the decision to the call-sheet owner)
     → Cue brief (no secrets dump)
     → "Line reading. Say 1, 2, or 3."
     → Confirm → prompt book → hang up
```

---

## 3. Source layout

```text
skills/customer-success-voice-signal/
├── src/
│   ├── cli.ts                 # npm run signal
│   ├── runSignal.ts           # orchestrator
│   ├── serveCli.ts / http/    # POST /cue
│   ├── applyActionCli.ts      # apply-action
│   ├── schemas.ts
│   ├── config/env.ts
│   ├── ingest/normalize.ts
│   ├── policy/                # shouldRing, house dark, options, cue lock
│   ├── calle/                 # intent, client, stage code, cue context
│   ├── map/                   # sdkOutcome, toDecision
│   ├── action/                # action intent + adapters (stab)
│   └── writeback/
├── fixtures/                  # four cues
├── events/                    # webhook-shaped inbound
└── data/                      # gitignored writeback
```

Crash-safe live dial is **create → persist `call.id` → waitForResult**, not `createAndWait`. `--from-call` remaps a stuck run without ringing again.

---

## 4. Trigger → line readings

| trigger_id | Demo fixture | Options (1 / 2 / 3) |
| --- | --- | --- |
| `stuck_support` | `stuck_support_acme.json` | take over chat · assign SE · snooze 2h |
| `agent_needs_decision` | `agent_needs_decision_acme.json` | approve A · approve B · reject/escalate |
| `sla_risk` | `sla_risk_globex.json` | own it · page backup · accept risk |
| `health_onboarding` | `health_onboarding_initech.json` | book SE · watchlist · flag churn |

Primary live path: **`stuck_support`**.

---

## 5. CLI

```bash
npm run signal -- --fixture stuck_support_acme.json
npm run signal -- --fixture stuck_support_acme.json --live PLACES
npm run signal -- --from-call call_xxx
npm run serve-cue
npm run apply-action -- --last --dry-run
```

Exit: `0` ok · `2` HOLD · `3` failure.

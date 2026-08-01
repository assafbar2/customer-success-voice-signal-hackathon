# Architecture & flow — `customer-success-voice-signal`

What was built. Stage Manager tone lives in call copy and CLI; this page stays structural.

---

## 1. System context

```text
┌─────────────┐   fixture / CLI   ┌──────────────────────────────────┐
│  Cue sheet  │ ─────────────────►│  customer-success-voice-signal   │
│  (4 JSON)   │                   │  npm run signal                  │
└─────────────┘                   └───────────┬──────────────────────┘
                                              │ curtain-up only
                                              ▼
                                     ┌─────────────────┐
                                     │     CALL-E      │
                                     │  createAndWait  │
                                     └────────┬────────┘
                                              │ rings CS owner only
                                              ▼
                                     ┌─────────────────┐
                                     │   Writeback     │
                                     │ prompt-book     │
                                     │ show-report     │
                                     │ cue-history*    │
                                     └─────────────────┘
* cue-history on curtain-up only
```

**Never in MVP:** CALL-E → customer. No Slack required. No DB. No demo UI app.

---

## 2. End-to-end flow

```text
CLI (--fixture | --trigger)
        │
        ▼
   normalize  →  AccountEvent
        │
        ▼
   shouldRing →  HOLD? ──yes──► writeback (hold) → exit 2
        │ no
        ▼
   buildCallIntent (Stage Manager task + line readings 1/2/3)
        │
   ┌────┴────────────────────────────┐
   │ dress rehearsal (default)       │ curtain-up
   │ no CALLE key needed             │ --live + PLACES
   │ simulate option 1               │ curtainUp(createAndWait)
   └────┬────────────────────────────┴────┬
        │                                 │
        ▼                                 ▼
   toDecision                        toDecision (structured /
                                     transcript / no_answer)
        │                                 │
        └────────────┬────────────────────┘
                     ▼
              writeback
              · prompt-book.ndjson
              · show-report.md
              · cue-history.ndjson (curtain-up only)
```

### Call beat (what CS hears)

```text
Ring → "Hi {name}. Stage Manager. You're up for {account}."
     → Short cue brief (no secrets dump)
     → "Line reading. Press or say 1, 2, or 3." [closed set]
     → Confirm → log to prompt book → hang up
```

**Modes:** dress rehearsal (default, no ring) · curtain up (`--live` + `PLACES`).

---

## 3. Source layout (as built)

```text
skills/customer-success-voice-signal/
├── src/
│   ├── cli.ts                 # npm run signal
│   ├── runSignal.ts           # orchestrator
│   ├── schemas.ts             # Zod: AccountEvent, CallIntent, DecisionResult
│   ├── config/env.ts          # .env + live gate
│   ├── ingest/normalize.ts    # raw fixture → AccountEvent
│   ├── policy/
│   │   ├── shouldRing.ts      # opt-in, severity, house dark, dedupe, placeholders
│   │   └── options.ts         # closed-set line readings per trigger
│   ├── calle/
│   │   ├── intent.ts          # buildCallIntent (Stage Manager task)
│   │   └── client.ts          # curtainUp → CalleClient.createAndWait
│   ├── map/toDecision.ts      # structured / transcript / no_answer → DecisionResult
│   └── writeback/index.ts     # prompt book · show report · cue-history
├── fixtures/                  # 4 cues (Acme / Globex / Initech)
└── data/                      # local writeback (gitignored)
```

| Module | Responsibility |
| --- | --- |
| `normalize` | One `AccountEvent` shape for all four triggers |
| `shouldRing` | Opt-in, severity ≥ high, house dark (live only), dedupe, placeholder reject |
| `buildCallIntent` | Stage Manager task + result schema |
| `curtainUp` | **Only** CALL-E invocation (`createAndWait`) |
| `toDecision` | Map structured result / transcript / voicemail → schema |
| `writeback` | Prompt book + show report; cue-history on curtain-up |

---

## 4. Entities

| Entity | Role |
| --- | --- |
| **Account** | Named customer org CS owns |
| **CsOwner** | Only person we call (`CS_OWNER_E164` overrides fixture on live) |
| **AccountEvent** | Normalized cue |
| **CallIntent** | Task + options + result schema for CALL-E |
| **DecisionResult** | Closed-set choice (or hold / no_answer / unclear) |

---

## 5. Trigger → line readings

| trigger_id | Demo fixture | Options (1 / 2 / 3) |
| --- | --- | --- |
| `stuck_support` | `stuck_support_acme.json` | take over chat · assign SE · snooze 2h |
| `agent_needs_decision` | `agent_needs_decision_acme.json` | approve A · approve B · reject/escalate |
| `sla_risk` | `sla_risk_globex.json` | own it · page backup · accept risk |
| `health_onboarding` | `health_onboarding_initech.json` | book SE · watchlist · flag churn |

Demo-ready live path: **`stuck_support`** (+ name-drop `agent_needs_decision`).

---

## 6. CLI

```bash
npm run signal -- --fixture stuck_support_acme.json          # dress rehearsal
npm run signal -- --fixture stuck_support_acme.json --live PLACES  # curtain-up
npm run signal -- --list | --last | --verbose | --help
```

Exit: `0` ok · `2` HOLD · `3` failure.

---

## 7. Done glance

```text
[Fixture] → [normalize] → [shouldRing] → [dress rehearsal | CALL-E → CS]
                                              → [toDecision] → [writeback]
```

**Shipped:** four fixtures, dress rehearsal, curtain-up client, writeback, vitest.  
**Not shipped:** demo UI, Slack writeback, DB.

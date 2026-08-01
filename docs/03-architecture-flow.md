# Architecture & flow — `customer-success-voice-signal`

One-page view of **what we are building**.  
Tone: serious ops problem, **light delivery** (see § Tone).

---

## 1. System context (who talks to whom)

```text
┌─────────────┐     events      ┌──────────────────────────────────┐
│  Triggers   │ ───────────────►│  customer-success-voice-signal   │
│  (fixtures  │                 │  (this product)                  │
│   / webhooks│                 └───────────┬──────────────────────┘
│   / agents) │                             │
└─────────────┘                             │ plan / run / get
                                            ▼
                                   ┌─────────────────┐
                                   │     CALL-E      │
                                   │  (real phone)   │
                                   └────────┬────────┘
                                            │ rings
                                            ▼
                                   ┌─────────────────┐
                                   │   CS Owner 📱   │
                                   │  (only callee)  │
                                   └────────┬────────┘
                                            │ decision
                                            ▼
                                   ┌─────────────────┐
                                   │   Writeback     │
                                   │ ticket · Slack  │
                                   │ · audit file    │
                                   └─────────────────┘
```

**Never in MVP:** CALL-E → customer.

---

## 2. End-to-end flow (happy path)

```text
                    ┌──────────────┐
                    │   TRIGGER    │  stuck_support | sla_risk |
                    │   arrives    │  agent_needs_decision |
                    └──────┬───────┘  health_onboarding
                           │
                           ▼
                    ┌──────────────┐
                    │  NORMALIZE   │  → AccountEvent
                    │  + POLICY    │  owned? severity? quiet hours?
                    └──────┬───────┘  already called? allowlist?
                           │
              ┌────────────┴────────────┐
              │ dress rehearsal?        │  (default; curtain-up = --live + PLACES)
              └────────────┬────────────┘
                     yes   │   no
              ┌────────────┘   └────────────┐
              ▼                             ▼
     ┌────────────────┐            ┌────────────────┐
     │ DRESS REHEARSAL│            │  curtain-up    │
     │ preview only   │            │  CalleClient   │──► CALL-E
     │ (no ring)      │            │  createAndWait │──► CS phone
     └────────────────┘            └───────┬────────┘
                                           │
                                           ▼
                                   ┌────────────────┐
                                   │ MAP → Decision │
                                   │ Result schema  │
                                   └───────┬────────┘
                                           │
                                           ▼
                                   ┌────────────────┐
                                   │ WRITEBACK      │
                                   │ prompt book    │
                                   │ show report    │
                                   └────────────────┘
```

### Call beat (what CS hears — Stage Manager)

```text
Ring → "Hi {name}, Stage Manager for {account}."
     → Cue type in plain language + 3–5 sentence brief
     → "Line readings — press or say 1, 2, or 3:" [closed set]
     → Confirm choice
     → "Logged in the prompt book. House to half." → hangup
```

**Modes:** dress rehearsal (default, no ring) · curtain up (`--live` + `PLACES`).

---

## 3. Entities

```text
┌──────────────────┐       owns        ┌──────────────────┐
│     Account      │◄──────────────────│     CsOwner      │
│ id, name, tier   │                   │ id, name, e164   │
│ health_flags     │                   │ quiet_hours      │
└────────┬─────────┘                   │ opt_in_phone     │
         │                             └──────────────────┘
         │ 1..n
         ▼
┌──────────────────┐       emits       ┌──────────────────┐
│     Ticket /     │                  │   AgentRuntime   │
│     Case         │                  │  (needs_human)   │
└────────┬─────────┘                  └────────┬─────────┘
         │                                     │
         └──────────────┬──────────────────────┘
                        ▼
              ┌──────────────────┐
              │  AccountEvent    │
              │  trigger_id      │
              │  severity        │
              │  summary         │
              │  option_set[]    │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐     ┌──────────────────┐
              │   CallIntent     │────►│   CallRun        │
              │   (to CALL-E)    │     │   (from CALL-E)  │
              └──────────────────┘     └────────┬─────────┘
                                                │
                                                ▼
                                       ┌──────────────────┐
                                       │ DecisionResult   │
                                       │ → writeback      │
                                       └──────────────────┘
```

| Entity | Role |
| --- | --- |
| **Account** | Named customer org CS owns |
| **CsOwner** | Only person we call |
| **AccountEvent** | Normalized trigger |
| **CallIntent** | What we ask CALL-E to do |
| **CallRun** | Transcript + metadata from CALL-E |
| **DecisionResult** | Closed-set choice + writeback payload |

---

## 4. Functions / modules

```text
customer-success-voice-signal/
│
├── ingest/
│   └── normalizeEvent(raw) → AccountEvent
│
├── policy/
│   ├── shouldRing(event, owner, now) → boolean
│   └── pickOptions(trigger_id) → Option[]
│
├── calle/
│   ├── planCall(intent)      → plan   // CALL-E
│   ├── runCall(plan)         → runId  // CALL-E
│   └── getCallRun(runId)     → run    // CALL-E
│
├── map/
│   └── toDecision(run, options) → DecisionResult
│
├── writeback/
│   ├── toTicketNote(result)
│   ├── toSlack(result)          // optional webhook
│   └── toAuditFile(result)
│
└── demo/
    ├── fixtures/*.json          // Acme tickets, fake health
    └── trigger-ui or CLI        // "fire stuck_support for Acme"
```

| Function | Responsibility |
| --- | --- |
| `normalizeEvent` | One shape for all four triggers |
| `shouldRing` | Quiet hours, severity, dedupe, allowlist |
| `planCall` / `runCall` / `getCallRun` | **Only** place CALL-E is invoked |
| `toDecision` | Parse spoken/DTMF choice → schema |
| `writeback.*` | Side effects after the call |
| `demo/*` | Judge-friendly fire button |

---

## 5. Sequence (one stuck_support call)

```text
Demo UI / CLI          Voice Signal           CALL-E              CS Owner
     │                      │                    │                    │
     │  fire(stuck_support) │                    │                    │
     │─────────────────────►│                    │                    │
     │                      │  plan_call         │                    │
     │                      │───────────────────►│                    │
     │                      │  run_call          │                    │
     │                      │───────────────────►│── ring ───────────►│
     │                      │                    │◄─ "2" ─────────────│
     │                      │  get_call_run      │                    │
     │                      │───────────────────►│                    │
     │                      │  DecisionResult    │                    │
     │                      │  writeback         │                    │
     │◄── show result ──────│                    │                    │
```

---

## 6. Trigger → options (quick map)

| trigger_id | CS hears options (examples) |
| --- | --- |
| `stuck_support` | 1 take over chat · 2 assign SE · 3 snooze 2h |
| `sla_risk` | 1 I own it · 2 page backup · 3 accept risk |
| `agent_needs_decision` | 1 approve A · 2 approve B · 3 reject / escalate |
| `health_onboarding` | 1 book SE session · 2 watchlist · 3 flag churn risk |

---

## 7. What “done” looks like in one glance

```text
[Event] → [Policy OK?] → [CALL-E → CS phone] → [Decision] → [Ticket/Slack/Audit]
                │ no
                └── log skip (no call)
```

**Built =** that path works for ≥2 triggers, dry-run mode, one real CALL-E call in the demo video, skill packaged for the awesome-list PR.

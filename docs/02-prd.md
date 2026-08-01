# PRD — customer-success-voice-signal

**Product / skill id:** `customer-success-voice-signal`  
**Persona:** **Stage Manager**  
**Hackathon:** CALL-E: Your Code Is Calling  
**Last updated:** 2026-08-01  
**Status:** MVP decisions locked · skill built under `skills/customer-success-voice-signal/`

**Related:** [03-architecture-flow.md](./03-architecture-flow.md) · [04-stack-hosting-tone.md](./04-stack-hosting-tone.md) · [05-dev-design-plan.md](./05-dev-design-plan.md)

## Decisions (Assaf)

| # | Decision | Choice |
| --- | --- | --- |
| 0 | Name | **`customer-success-voice-signal`** |
| 1 | MVP phone target | **CS only** — CALL-E rings the CS owner / TAM, not the customer |
| 2 | Triggers in scope | stuck support · SLA risk · agent needs decision · health/onboarding stall |
| 3 | Branding | **Sentry-shaped, not Sentry-branded** — fictional error-monitoring / technical SaaS |
| 4 | Persona | **Stage Manager** — dress rehearsal / curtain up / cue / prompt book / HOLD |

---

## One-liner

> When a **named account** hits a high-risk **cue**, the **Stage Manager** rings the **CS owner** via CALL-E with a short brief and **closed-set line readings** — then writes the decision to the **prompt book** and **show report**.

**Not:** a customer dialer, SDR tool, or generic “AI phone agent.”

---

## Problem

CS owns revenue and relationships but lives in noisy queues. High-signal moments get buried: support/AI loops on strategic accounts, SLA going red, an agent stuck on `needs_human`, onboarding/health stalling before renewal. Chat does not interrupt. Phone does — if the call is **rare, short, structured, and for the right person**.

---

## User

| Role | Description |
| --- | --- |
| **Primary** | CSM / TAM for technical B2B SaaS (error monitoring, infra, devtools — *shaped like Sentry, not named*) |
| **Secondary** | Support lead / SE who feeds context into the same account object |
| **Not in MVP** | End customer (no outbound to customer) |

---

## Triggers

All share: **named/CS-owned account** + **opt-in phone** + **severity ≥ high** + **house dark respected on curtain-up**.

| ID | Trigger | Call goal |
| --- | --- | --- |
| `stuck_support` | AI/support path stuck on open case | take over chat / assign SE / snooze |
| `sla_risk` | SLA breach imminent on owned account | own it / page backup / accept risk |
| `agent_needs_decision` | Agent emits `needs_human` with options | approve A / approve B / reject-escalate |
| `health_onboarding` | Health or onboarding stall | book SE / watchlist / flag churn |

**Demo cues:** `stuck_support` + `agent_needs_decision` (fixtures + live path for the first; second as first-class config / name-drop).

---

## Call experience (Stage Manager)

1. Phone rings (CS owner E.164 from env / call sheet).  
2. Identify: Stage Manager + account + cue.  
3. Short brief (no secrets dump).  
4. One decision — line readings **1 / 2 / 3**.  
5. Confirm → hang up.  
6. Structured result → **prompt book** + **show report**.

**Modes:** **Dress rehearsal** (default, no ring, no CALLE key) · **Curtain up** (`--live` + `PLACES`; needs `CALLE_API_KEY` + `CS_OWNER_E164`).

**Never in MVP:** call the customer; medical/emergency; auto-dial without policy match; long discovery interview.

---

## Structured result

```json
{
  "trigger_id": "stuck_support",
  "account_id": "acct_acme",
  "account_name": "Acme Corp",
  "cs_owner_id": "cs_maya",
  "call_run_id": "calle_…",
  "decision": "take_over_chat",
  "decision_label": "Take over in chat now",
  "option_id": "1",
  "notes_short": null,
  "follow_up_at": null,
  "completed_at": "ISO-8601",
  "mode": "curtain_up"
}
```

Options are trigger-specific, always closed set. Unmapped live outcomes may be `no_answer` or `unclear` — never a fake line reading.

---

## System flow (built)

```text
Cue (fixture via CLI)
  → normalize → AccountEvent
  → shouldRing (owned? severity? house dark? already cued?)
  → dress rehearsal preview (default)  OR  curtainUp(createAndWait)
  → toDecision → DecisionResult
  → writeback (prompt-book.ndjson + show-report.md; cue-history on live)
```

---

## Non-goals (hackathon)

- Customer outbound  
- Real Sentry production integrations  
- Full CRM OAuth / multi-tenant billing  
- Demo UI app (CLI is the surface)  
- Required Slack / DB  
- Sentiment inference · emergency / medical / legal advice  

---

## Branding

| OK | Not OK |
| --- | --- |
| “Error monitoring SaaS”, “devtools platform” | “Sentry”, internal codenames, real customers |
| Fictional orgs: Acme, Globex, Initech | Real logos/data |

---

## Success for judges

| Criterion | How we hit it |
| --- | --- |
| Real World Impact | Named-account CS interrupt is a real job |
| Quality of Idea | Phone as CS control plane; multi-trigger one engine; Stage Manager |
| Technical Implementation | CALL-E `createAndWait` at runtime; schema; dress rehearsal; writeback |
| Demo | ≤3 min: cue → dress rehearsal → curtain-up → prompt book |

**Prize target:** Most Practical first; Innovative secondary; always submit Most Valuable Feedback survey.

---

## Packaging

| Field | Value |
| --- | --- |
| Path | `skills/customer-success-voice-signal/` |
| PR (hackathon repo) | https://github.com/assafbar2/customer-success-voice-signal-hackathon/pull/1 |
| Awesome-list target | https://github.com/CALLE-AI/awesome-phone-call-agents |
| Blurb | Stage Manager cues CALL-E to ring the CS owner when support is stuck, SLA is at risk, an agent needs a decision, or health/onboarding stalls — closed-set writeback, dress rehearsal first. |

---

## Changelog

| Date | Change |
| --- | --- |
| 2026-07-31 | Locked: CS-only MVP; four trigger families; Sentry-shaped unbranded; named product |
| 2026-08-01 | Persona Stage Manager; skill scaffolded; dress rehearsal + curtain-up path |
| 2026-08-01 | Docs trimmed to match as-built (CLI, no demo UI / Slack / DB) |

# PRD — customer-success-voice-signal

**Product / skill id:** `customer-success-voice-signal`  
**Persona:** **Stage Manager** (theater vocabulary hard)  
**GitHub (private):** see repo `customer-success-voice-signal-hackathon`  
**Hackathon:** CALL-E: Your Code Is Calling  
**Last updated:** 2026-08-01  
**Status:** Decisions locked for MVP · name locked · persona locked  

**Related docs:** [03-architecture-flow.md](./03-architecture-flow.md) · [04-stack-hosting-tone.md](./04-stack-hosting-tone.md) · [05-dev-design-plan.md](./05-dev-design-plan.md)

## Decisions (Assaf)

| # | Decision | Choice |
| --- | --- | --- |
| 0 | Name | **`customer-success-voice-signal`** |
| 1 | MVP phone target | **CS only** — CALL-E calls the CS owner / TAM, not the customer |
| 2 | Triggers in scope | **All of:** stuck support · SLA risk · agent needs decision · health/onboarding stall |
| 3 | Branding | **Sentry-shaped, not Sentry-branded** — fictional “error-monitoring / technical SaaS” |
| 4 | Persona | **Stage Manager** — dress rehearsal / curtain up / cue / prompt book / HOLD |

---

## One-liner

> **customer-success-voice-signal** — when a **named account** hits a high-risk **cue**, the **Stage Manager** rings the **CS owner** via CALL-E with a 60-second brief and **closed-set line readings** — then writes the decision to the **prompt book** and **show report**.

**Not:** a customer dialer, SDR tool, or generic “AI phone agent.”

---

## Problem

CS owns revenue and relationships but lives in noisy queues and dashboards. High-signal moments get buried:

- Support/AI loops while a strategic account waits  
- SLA turns red  
- An automation/agent cannot proceed without a human  
- Onboarding or health silently stalls before renewal  

Chat and email do not interrupt. Phone does — if the call is **rare, short, structured, and for the right person**.

---

## User

| Role | Description |
| --- | --- |
| **Primary** | Customer Success Manager / TAM for technical B2B SaaS (error monitoring, infra, devtools — *shaped like Sentry, not named*) |
| **Secondary** | Support lead / SE who hands context into the same account object |
| **Not a user in MVP** | End customer (no outbound to customer in MVP) |

---

## When CS gets a phone call (trigger catalog)

All triggers share: **named/CS-owned account** + **opt-in phone** + **severity ≥ threshold** + **house dark respected on curtain-up**.

| ID | Trigger | Example (fictional) | Call goal |
| --- | --- | --- | --- |
| `stuck_support` | AI/support path stuck or customer looping on open case | Ticket #4821, 2 bot handoffs, no resolution | Decide: take over in chat / assign SE / schedule later |
| `sla_risk` | SLA breach imminent or breached on owned account | Enterprise Acme, P1, 15 min to breach | Decide: own it now / page backup / accept risk |
| `agent_needs_decision` | Agent emits `needs_human` with options | Agent cannot approve exception / missing policy | Speak a choice among 2–3 options |
| `health_onboarding` | Health or onboarding stall on named account | No first event in 14d, or usage −40% + renewal window | Decide: outreach plan / SE join / wait & watch |

**MVP demo** should show **at least two** triggers live (recommend: `stuck_support` + `agent_needs_decision`) and list the others as first-class config so judges see full coverage.

---

## Call experience (CS is callee — Stage Manager)

1. Phone rings (CS owner E.164 from the call sheet).  
2. Stage Manager identifies: persona + account + cue type.  
3. 3–5 sentence brief (no secrets dump).  
4. **One decision** with closed-set **line readings** 1 / 2 / 3 (plus honest “not now” where applicable).  
5. Confirm choice.  
6. Hang up.  
7. Structured result → **prompt book** + **show report**.

**Modes:** **Dress rehearsal** (default, no ring) · **Curtain up** (`--live` + type/env `PLACES`).

**Never in MVP:** call the customer; medical/emergency; auto-dial without policy match; long discovery interview.

---

## Structured result schema (draft)

```json
{
  "trigger_id": "stuck_support",
  "account_id": "acct_acme",
  "account_name": "Acme Corp",
  "cs_owner_id": "cs_maya",
  "call_run_id": "calle_…",
  "decision": "take_over_chat",
  "decision_label": "I'll take over in chat now",
  "option_id": "1",
  "notes_short": "optional free text if captured",
  "follow_up_at": null,
  "completed_at": "ISO-8601"
}
```

Options are **trigger-specific** but always closed set for the call.

### Example option sets (line readings)

**stuck_support**

1. Take over in chat now  
2. Assign to SE / specialist  
3. Not now — snooze 2 hours  

**sla_risk**

1. I own this ticket now  
2. Page backup CS/SE  
3. Acknowledge risk, no action  

**agent_needs_decision**

1. Approve option A  
2. Approve option B  
3. Reject — escalate to manager  

**health_onboarding**

1. Book SE technical session (I’ll follow up in product)  
2. Mark watchlist — no outreach yet  
3. Flag churn risk for manager  

---

## System flow

```text
Cue (fixture or webhook)
  → normalize → AccountEvent
  → policy: owned? severity? house dark? already cued?
  → dress rehearsal preview (default)
  → curtain-up: CalleClient.createAndWait  // CS only
  → map → DecisionResult
  → writeback (prompt book NDJSON + show report markdown)
```

---

## Non-goals (hackathon)

- Customer outbound calls  
- Real Sentry production integrations  
- Full CRM OAuth  
- Multi-tenant SaaS billing  
- Sentiment inference / diagnosis  
- Emergency / medical / legal advice calls  

---

## Branding rules

| OK | Not OK |
| --- | --- |
| “Error monitoring SaaS”, “devtools platform”, “performance product” | “Sentry”, internal codenames, real customer names |
| Fictional orgs: Acme, Globex, Initech | Real customer logos/data |
| Roles: CSM, TAM, SE, Support | Implying official employer product |

---

## Success for judges

| Criterion | How we hit it |
| --- | --- |
| Real World Impact | Named-account CS interrupt is a real job-to-be-done |
| Quality of Idea | Phone as **CS control plane**, not spam dialer; multi-trigger one engine; Stage Manager persona |
| Technical Implementation | CALL-E `createAndWait` at runtime; schema; dress rehearsal; writeback |
| Demo | ≤3 min: cue → dress rehearsal → curtain-up → decision → prompt book |

---

## Prize targeting

1. **Most Practical** (primary)  
2. Innovative only as secondary narrative (“agent stuck → phone”)  
3. Always submit **Most Valuable Feedback** survey  

---

## Packaging (awesome-phone-call-agents)

| Field | Value |
| --- | --- |
| Contribution area | `skills/customer-success-voice-signal/` (primary); optional thin `apps/` later |
| Skill folder | `customer-success-voice-signal/` |
| List blurb (draft) | Stage Manager voice signal for CS: CALL-E cues the account owner when support is stuck, SLA is at risk, an agent needs a decision, or health/onboarding stalls — structured decision writeback, dress rehearsal first. |

## Open implementation choices (next)

- [x] Product/skill name → `customer-success-voice-signal`  
- [x] Persona → Stage Manager  
- [x] Skill scaffold under `skills/customer-success-voice-signal/`  
- [ ] Real curtain-up in demo video  
- [ ] Optional Slack webhook writeback  

---

## Changelog

| Date | Change |
| --- | --- |
| 2026-07-31 | Locked: CS-only MVP; all four trigger families; Sentry-shaped unbranded |
| 2026-07-31 | Named **customer-success-voice-signal** |
| 2026-08-01 | Locked persona **Stage Manager**; dress rehearsal / curtain up vocabulary |

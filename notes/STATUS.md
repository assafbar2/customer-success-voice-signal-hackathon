# Status

| Field | Value |
| --- | --- |
| Last update | 2026-08-01 |
| Devpost | Registered |
| Primary idea | **`customer-success-voice-signal`** — Stage Manager; CS-only callee; multi-trigger |
| Persona | **Stage Manager** (dress rehearsal / curtain up) |
| CALL-E SDK | `@call-e/calle` ^0.6.0 — dial path proven |
| Code | **Yes** — `skills/customer-success-voice-signal/` |
| Live cues | **2 attempted** — `stuck_support` **succeeded** (decision **1** / `take_over_chat`); `agent_needs_decision` rung, mapping still flaky (unclear) |
| Secrets | Local `.env` only (gitignored). Never commit keys/phones. |
| PR | https://github.com/assafbar2/customer-success-voice-signal-hackathon/pull/1 |

## Locked decisions

0. Name: **`customer-success-voice-signal`**  
1. MVP phone target: **CS only** (not customer)  
2. Triggers: stuck support · SLA · agent decision · health/onboarding  
3. Branding: Sentry-**shaped**, not Sentry-**branded**  
4. Package: skill → `skills/customer-success-voice-signal/`  
5. Persona: **Stage Manager**  

See `docs/02-prd.md` · `docs/05-dev-design-plan.md`.

## Blockers / next

- Demo video ≤3 min ([`submission/video-script.md`](../submission/video-script.md))  
- Awesome-list PR + Devpost package  
- Extra CALL-E calls if quota tight  
- Optional: second cue live polish (`agent_needs_decision`)

## Log

- 2026-07-31: Project folder; ideas 1/2/5; registered; PRD locked; named product; architecture + private GitHub.  
- 2026-08-01: Stage Manager skill scaffold (schemas, fixtures, dress rehearsal CLI, writeback, curtain-up client).  
- 2026-08-01: First curtain-up — auth OK, ring OK, **voicemail** → mapped `no_answer`.  
- 2026-08-01: Second curtain-up (`stuck_support`) — **answered**; decision **1** Take over in chat now.  
- 2026-08-01: Additional live probes on `agent_needs_decision` — ring OK; structured map unclear (still demo name-drop).  
- 2026-08-01: Public docs trimmed to match as-built.  

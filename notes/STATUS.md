# Status (operator log)

| Field | Value |
| --- | --- |
| Last update | 2026-08-03 |
| Product | **Stage Manager** — skill id `customer-success-voice-signal` |
| Judge site | https://assafbar2.github.io/customer-success-voice-signal-hackathon/ (live) |
| Hardening PR | https://github.com/assafbar2/customer-success-voice-signal-hackathon/pull/3 |
| Live ladder | `research/calle-api-notes.md` |
| Evidence | `submission/evidence/` (redacted) |
| MVF draft | `submission/mvf-feedback.md` |
| Pre-submit | [`submission/PRE-SUBMIT.md`](../submission/PRE-SUBMIT.md) |

## Live outcomes (honest)

| Cue | Best curtain-up result | Also observed |
| --- | --- | --- |
| `stuck_support` | Decision **1** take over in chat | Prior voicemail → `no_answer` |
| `agent_needs_decision` | Decision **1** approve A | Prior `unclear` (mapping) |

## Product loop (closed)

- [x] Decision → action intent → Slack / GitHub live adapters (env-gated)
- [x] HTTP cue listener — `npm run serve-cue` → `POST /cue` (curl → engine → apply-action)
- [x] SDK depth — `failureCode` / `completionConfidence` / optional `webhookUrl` (create→persist→wait)
- [x] Identity read-back — spoken stage code before 1/2/3 counts
- [x] MVF writeup — `submission/mvf-feedback.md`

## Submit checklist (pre-submit)

Master list: [`submission/PRE-SUBMIT.md`](../submission/PRE-SUBMIT.md)

- [ ] **MVF survey** — paste `submission/mvf-feedback.md` on Devpost (same session as video/Devpost)
- [ ] Demo video — `submission/video-script.md`
- [ ] Terminal GIF — `submission/gif-notes.md` → README + site
- [ ] Awesome-list PR — `submission/awesome-list/PACKAGING.md` (MVF is a gate on that checklist)
- [ ] Devpost form — `submission/devpost.md`
- [x] GitHub repo homepage → Pages URL
- [x] Vercel leftover project removed
- [x] GitHub topics added (call-e, voice-agents, customer-success, hackathon, phone-call-agent)
- [ ] Social preview image (repo Settings → Social preview)

**Dated nudge:** `notes/REMINDER-2026-09-01.md`

## Still open (residual)

| Item | Status |
| --- | --- |
| Hash-chained prompt book | Skipped (hack scope) |
| Real CS conversations for Real World Impact | Open (operator) |
| Packaging split (`skills/` → `apps/typescript/…`) | Open (merge risk only) |
| Video / GIF / awesome-list / MVF / OG | Open — tracked in PRE-SUBMIT |

# Status (operator log)

| Field | Value |
| --- | --- |
| Last update | 2026-08-12 |
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
| `stuck_support` | Decision **1** take over in chat (incl. 2026-08-12 live: stage code 4821 + “1”) | Prior voicemail → `no_answer`; first 2026-08-12 map was `unclear` (CALL-E paraphrased `decision`) |
| `agent_needs_decision` | Decision **1** approve A | Prior `unclear` (mapping) |

## Product loop (closed)

- [x] Decision → action intent → Slack / GitHub live adapters (env-gated)
- [x] HTTP cue listener — `npm run serve-cue` → `POST /cue` (curl → engine → apply-action)
- [x] HTTP live arming — `CUE_ALLOW_LIVE=1` required; non-loopback needs secret; timingSafeEqual
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

## Win checklist (repo review, 2026-08-03)

Rubric state: Technical ✓ · Idea ✓ · Impact ✓ · **Demo ✗** — the video is 25% of the
rubric and 100% of the emotional argument. Everything below serves it.

- [ ] **Video spine = the full loop live:** `curl → serve-cue → phone rings → "one" → apply-action --adapter slack → message lands`. That 30 seconds IS "Most Practical".
- [ ] **One live curtain-up run of the whole new chain** (listener + adapter, not components separately) → append to the live ladder in `research/calle-api-notes.md`. Do it as the video take — one stone, two birds.
- [ ] **Fresh-clone judge sanity pass:** clean `git clone → npm install → npm test → curl POST /cue`, exactly as a judge would, before Devpost submit.
- [ ] Awesome-list PR timing: bar was "v1 solid" — with 67+ tests, live adapters, HTTP listener, green CI, v1 is arguably solid now. Their PR review latency is the one clock we don't control.
- Operational: two agents (Cursor + Claude Code) commit here — **sync clones before each session** to avoid merge-conflict theater.

**Dated nudge:** `notes/REMINDER-2026-09-01.md`

## Still open (residual)

| Item | Status |
| --- | --- |
| Hash-chained prompt book | Skipped (hack scope) |
| Real CS conversations for Real World Impact | Open (operator) |
| Packaging split (`skills/` → `apps/typescript/…`) | Open (merge risk only) |
| Video / GIF / awesome-list / MVF / OG | Open — tracked in PRE-SUBMIT |

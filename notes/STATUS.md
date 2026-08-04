# Status (operator log)

| Field | Value |
| --- | --- |
| Last update | 2026-08-03 |
| Product | **Stage Manager** — skill id `customer-success-voice-signal` |
| Judge site | https://assafbar2.github.io/customer-success-voice-signal-hackathon/ (live) |
| Hardening PR | https://github.com/assafbar2/customer-success-voice-signal-hackathon/pull/3 |
| Live ladder | `research/calle-api-notes.md` |
| Evidence | `submission/evidence/` (redacted) |

## Live outcomes (honest)

| Cue | Best curtain-up result | Also observed |
| --- | --- | --- |
| `stuck_support` | Decision **1** take over in chat | Prior voicemail → `no_answer` |
| `agent_needs_decision` | Decision **1** approve A | Prior `unclear` (mapping) |

## Product loop (closed)

- [x] Decision → action intent → Slack / GitHub live adapters (env-gated)
- [x] HTTP cue listener — `npm run serve-cue` → `POST /cue` (curl → engine → apply-action)

## Submit checklist

- [ ] Awesome-list PR (`submission/awesome-list/PACKAGING.md`) — **after v1 is solid; recurring nudge, do not drop**
- [ ] Devpost submit + MVF survey (draft text: `submission/devpost.md`)
- [x] GitHub repo homepage → Pages URL
- [x] Vercel leftover project removed
- [x] GitHub topics added (call-e, voice-agents, customer-success, hackathon, phone-call-agent)
- [ ] Social preview image (repo Settings → Social preview — manual upload; dark stage + "Ack is not a decision.")
- [ ] Terminal GIF of dress rehearsal (README + site) — cheap "video before the video"
- [ ] Demo video with real call audio (separate track — review notes in `submission/video-script.md`)

## Win checklist (repo review, 2026-08-03)

Rubric state: Technical ✓ · Idea ✓ · Impact ✓ · **Demo ✗** — the video is 25% of the
rubric and 100% of the emotional argument. Everything below serves it.

- [ ] **Video spine = the full loop live:** `curl → serve-cue → phone rings → "one" → apply-action --adapter slack → message lands`. That 30 seconds IS "Most Practical".
- [ ] **One live curtain-up run of the whole new chain** (listener + adapter, not components separately) → append to the live ladder in `research/calle-api-notes.md`. Do it as the video take — one stone, two birds.
- [ ] **Fresh-clone judge sanity pass:** clean `git clone → npm install → npm test → curl POST /cue`, exactly as a judge would, before Devpost submit.
- [ ] Awesome-list PR timing: bar was "v1 solid" — with 67+ tests, live adapters, HTTP listener, green CI, v1 is arguably solid now. Their PR review latency is the one clock we don't control.
- Operational: two agents (Cursor + Claude Code) commit here — **sync clones before each session** to avoid merge-conflict theater.

**Dated nudge:** `notes/REMINDER-2026-09-01.md`

## Still open (Opus / Fable residual)

| Item | Status |
| --- | --- |
| Slack + GitHub wire-out | Done (Fable) |
| HTTP `/cue` listener | Done |
| SDK `failureCode` / `completionConfidence` / `webhookUrl` | Open |
| Identity read-back + hash-chained prompt book | Open |
| Real CS conversations for Real World Impact | Open (operator) |
| MVF survey writeup | Open |
| Packaging split (`skills/` → `apps/typescript/…`) | Open (merge risk only) |
| OG / GIF / evidence dashboard screenshot | Open (operator) |

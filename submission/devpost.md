# Devpost submission text — Stage Manager

Copy-paste source for the Devpost form. Keep the honesty; cut length before charm.

---

## Project name

**Stage Manager**

## Tagline (Devpost tagline field)

> Ack is not a decision.

Alternate (if a longer field): *When the renewal goes quiet, page the owner — not the customer.*

## Elevator pitch (~200 chars, for short fields)

When a named account hits a high-risk moment, Stage Manager rings the CS owner — never the customer — captures a closed-set 1/2/3 decision in ~60s, and hands it to the next system as an action intent.

---

## Full description (long field, structured to the judging rubric)

### The problem

Every company pages an engineer when a server goes down. Nobody pages the human who owns the renewal when the account goes quiet. Customer Success owns the revenue relationship; Slack owns the noise. When support loops, SLA turns red, an agent hits `needs_human`, or onboarding stalls — the alert hides under everything else until churn is already expensive.

PagerDuty-style tools phone you to *acknowledge* an alert. Ack is not a decision.

### 1 — Real World Impact

- **Right person:** interrupt the account owner, not the account. Never the customer.
- **Faster decision:** closed-set 1/2/3 line reading in ~60 seconds instead of thread archaeology.
- **Audit trail:** every decision lands in the prompt book (NDJSON audit log) and show report — the kind of trail you hand a manager, not another Slack shrug.
- **Monday-morning practical:** four real CS cues (stuck support, SLA risk, agent-needs-decision, health/onboarding stall), one engine, and a decision → action-intent seam pointed at the systems CS teams already use.

### 2 — Quality of the Idea

Phone-call agents mostly point outward (sales dialers, customer bots) or stop at incident ack. Stage Manager points the phone **inward** at the B2B customer-success / renewal lane — still open on the awesome-list — and treats the call as a **structured decision capture**, not a conversation. The decision is state, then an action intent for the next system (ticket / CRM / Slack), not a chat ack.

### 3 — Technical Implementation (CALL-E at runtime)

- CALL-E SDK (`@call-e/calle`): `calls.create` → persist call id → `calls.waitForResult` (not `createAndWait`), with idempotency keys. Optional `webhookUrl` + `CALLE_WAIT=0` for async completion.
- Result mapping prefers `failureCode` / `completionConfidence` / `structuredResult`; summary heuristics only when codes are absent. Never invent a decision.
- **Identity read-back:** spoken 4-digit stage code before a 1/2/3 is logged as the call-sheet owner’s decision.
- **Safety rails:** dress rehearsal (dry-run) by default; live requires `--live` + `PLACES`; CS owner only; fixture phones rejected on live; per-owner call budget; timezone-aware quiet hours; HOLD/failure never poison cue dedupe; untrusted cue text wrapped before it reaches the prompt.
- 85 tests + typecheck; webhook-shaped stdin **and** `POST /cue` HTTP listener; exit codes 0/2 (HOLD)/3.
- **Operator-proven live ladder,** misses included: voicemail and `unclear` captures logged alongside the two successful curtain-up decisions. Redacted evidence in the repo.

### 4 — Product Experience & Demo

- Judges run the full loop in four commands with **no API key**: dress rehearsal → line readings → action-intent dry-run → local receipt.
- Deployable inbound: `npm run serve-cue` → `curl POST /cue` → same engine → `apply-action --adapter slack` lands the decision in a real channel.
- Curtain-up (real ring) is one env file away, gated on purpose.
- ≤3 min demo video with real call audio: problem → dress rehearsal → live decision → writeback → handoff.

### What's next

- Zendesk / Salesforce adapter shapes documented at the seam (Slack + GitHub already live).
- Awesome-list PR once v1 is battle-tested.

### Most Valuable Feedback

See [`submission/mvf-feedback.md`](mvf-feedback.md) — structured feedback for the MVF survey (closed-set flakiness, no DTMF, failureCode docs, idempotency retries, identity primitive wishlist).

**Submit MVF in the same pre-submit pass as the video, GIF, and awesome-list PR** — checklist: [`PRE-SUBMIT.md`](PRE-SUBMIT.md).

---

## Built with (Devpost tags)

`typescript` · `node` · `call-e` · `vitest` · `zod` · `github-pages` · `github-actions`

## Links

- Repo: https://github.com/assafbar2/customer-success-voice-signal-hackathon
- Judge site: https://assafbar2.github.io/customer-success-voice-signal-hackathon/
- Skill: `skills/customer-success-voice-signal/`
- Live evidence (redacted): `submission/evidence/` · full ladder: `research/calle-api-notes.md`
- MVF: `submission/mvf-feedback.md`

---

*No customers were called in the making of this demo.*

# Most Valuable Feedback — Stage Manager → CALL-E platform

Copy/adapt into the Devpost **Most Valuable Feedback** survey. Written from operator live ladder + SDK integration work on `customer-success-voice-signal` (@call-e/calle ^0.6.0). Honest, specific, actionable.

---

## One-line summary

Closed-set phone decisions work, but speech-only capture is flaky, voicemail lacks a first-class typed outcome, and several useful SDK fields were easy to miss from the happy-path docs.

---

## What worked well

1. **`calls.create` + idempotency + `waitForResult`** — clear contract. We deliberately use create → persist `call.id` → wait (not `createAndWait`) so a crash mid-dial still leaves a recoverable id under `data/open-calls/`. That pattern should be documented as the recommended production shape.
2. **`resultSchema` / `structuredResult`** — when it lands, the closed-set 1/2/3 path is excellent for CS decision capture.
3. **Task prompt control** — enough room for persona, untrusted-cue wrapping, and identity read-back instructions without fighting the SDK.
4. **Webhook URL on create (`webhookUrl`)** — once discovered, the async completion path is obvious. Pairing it with create→persist is the right crash-safe story.

---

## Friction / bugs / gaps (ranked)

### 1. Structured-result flakiness on closed-set answers (high)

**Observed:** Two live `agent_needs_decision` curtain-ups rang and conversed, then mapped to `unclear` (calls `call_pBTeqKhl…`, `call_9FtyqEiM…` in our ladder). A later retry captured **Decision 1**. Same skill, same schema, same phone.

**Ask:** Publish reliability guidance for short closed-set captures (retry policy, confidence thresholds, when `structuredResult` is null despite a spoken “one”). Prefer a typed `unknown` / `unclear` enum in schema examples so skills don’t invent decisions.

### 2. No DTMF — closed sets are speech-only (high)

**Observed:** Line readings must be spoken (“one / two / three”). There is no SDK DTMF / keypad path. Background noise and short affirmations fight the classifier.

**Ask:** Optional DTMF collection for closed-set skills (press 1/2/3), or a documented speech-vs-keypad recommendation. This is the single biggest reliability unlock for “Most Practical” decision skills.

### 3. Voicemail / no-answer as prose, not a typed field (high → partially mitigated)

**Observed:** Early ladder rows needed summary-string heuristics (`"voicemail"`, `"no answer"`) because we weren’t wiring `failureCode` / attempt-level codes.

**Ask:** Document the canonical `failure_code` vocabulary (voicemail, no_answer, busy, …) next to `task_completed` and `completion_confidence` in the “reading a result” guide. Make “prefer failureCode over summary text” the default recipe in quickstarts.

*(We now prefer `failureCode` + `completionConfidence` in Stage Manager; summary heuristics are last resort only when codes are absent.)*

### 4. `completionConfidence` / `evidence` under-documented for decision skills (medium)

**Observed:** Typings expose `completionConfidence` and `evidence`, but happy-path examples stop at `structuredResult`. Low confidence with a plausible-looking structured object is a footgun for anything that writes to a ticket/CRM.

**Ask:** Show a three-gate example: `taskCompleted === true` ∧ confidence not low ∧ schema-valid structured → accept; else HOLD/unclear.

### 5. Idempotency semantics for “same cue, new attempt” (medium)

**Observed:** We key idempotency as `csvs:{trigger}:{account}:{event_id}`. Retries after a soft `unclear` need a deliberate key bump or a new `event_id`, otherwise you may replay the prior run.

**Ask:** Document when idempotency returns the prior call vs starts a new dial, and recommend a version suffix for human-initiated retries (`…:v2`).

### 6. Identity / caller verification is skill-authored, not platform-assisted (medium)

**Observed:** Anyone who picks up the CS owner’s phone can speak “one”. We added a spoken stage-code read-back in the task + `resultSchema`, but the platform doesn’t help (no PIN challenge primitive).

**Ask:** Optional “challenge phrase / code” helper on create (platform generates, validates, surfaces `identity_confirmed` on the Call) would raise the floor for approval-class and CS-decision skills.

---

## Concrete doc / API wishlist

| Item | Why |
| --- | --- |
| Canonical `failure_code` list | Stop every skill inventing summary regexes |
| DTMF for closed sets | Reliability for 1/2/3 decisions |
| Result-reading recipe with confidence | Prevent invented decisions |
| create → persist → wait (not only createAndWait) | Crash safety |
| Idempotency retry versioning | Clear operator retries after `unclear` |
| Identity challenge primitive | Bound decisions to the intended person |

---

## Evidence pointers (this repo)

- Live ladder (wins + misses): `research/calle-api-notes.md`
- Redacted samples: `submission/evidence/`
- Mapping that prefers SDK fields: `skills/customer-success-voice-signal/src/map/sdkOutcome.ts`, `toDecision.ts`
- Identity read-back: `skills/customer-success-voice-signal/src/calle/stageCode.ts`, `intent.ts`
- Crash-safe dial: `skills/customer-success-voice-signal/src/calle/client.ts`

---

*Submitted as operator feedback from building Stage Manager for the CALL-E hackathon. No customers were called in the making of this demo.*

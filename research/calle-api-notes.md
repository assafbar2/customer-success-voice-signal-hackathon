# CALL-E API notes (Stage Manager)

## Get / rotate API keys

**https://dashboard.heycall-e.com/account/api-keys**

Put the value in `skills/customer-success-voice-signal/.env` as `CALLE_API_KEY` (gitignored).  
Skill docs: [`../skills/customer-success-voice-signal/references/auth-and-keys.md`](../skills/customer-success-voice-signal/references/auth-and-keys.md).

## SDK

- Package: `@call-e/calle` `^0.6.0`
- Entry: `CalleClient` → `calls.create` → persist `call.id` → `calls.waitForResult` (with `idempotencyKey`)
- Auth: `CALLE_API_KEY` (Bearer); optional `CALLE_BASE_URL`

## Curtain-up payload

```ts
const created = await client.calls.create(
  {
    task: intent.task,
    recipients: [{ phones: [e164], region, locale }],
    resultSchema: intent.result_schema,
    metadata: { skill, persona, never_call_customer: true, … },
  },
  { idempotencyKey },
);
// persist created.id under data/open-calls/
const call = await client.calls.waitForResult(created.id, { timeoutMs });
```

Implemented in `src/calle/client.ts` (`curtainUp`) + `src/calle/intent.ts` (`buildCallIntent`).

## Result mapping

Prefer SDK fields over prose (see [calle-sdk.md](../skills/customer-success-voice-signal/references/calle-sdk.md)):

1. `failureCode` (call + attempts) → `no_answer` when voicemail / no_answer / …
2. `taskCompleted === false` → never a 1/2/3
3. Low `completionConfidence` → `unclear`
4. `structuredResult` + **identity read-back** (spoken stage code)
5. Gated transcript fallback
6. Summary-string heuristics **only** when no failure codes were supplied

## Modes

| Mode | Ring? | Needs key? | Cue-history? |
| --- | --- | --- | --- |
| Dress rehearsal | No | No | No |
| Curtain up | Yes | `CALLE_API_KEY` + `CS_OWNER_E164` + `--live` + `PLACES` | Live dial outcomes only (HOLD does not append) |

## Live probe log (no secrets)

Full ladder from operator curtain-up runs. Winning rows are real; earlier rows are assets (mapping / voicemail), not erased.

| Date | Cue | Result | Call run (prefix) | Notes |
| --- | --- | --- | --- | --- |
| 2026-08-01 | `stuck_support` | Voicemail → `no_answer` | `call_xpCzdX7Y…` | Auth + dial proven |
| 2026-08-01 | `stuck_support` | **Decision 1** `take_over_chat` | `call_cslZ3Hcu…` | Answered; prompt book OK |
| 2026-08-01 | `agent_needs_decision` | `unclear` | `call_pBTeqKhl…` | Ring OK; capture flaky |
| 2026-08-01 | `agent_needs_decision` | `unclear` | `call_9FtyqEiM…` | Ring OK; capture flaky |
| 2026-08-01 | `agent_needs_decision` | **Decision 1** `approve_a` | `call_ylJkGID4…` | Answered; prompt book OK |

Redacted committed samples: [`../submission/evidence/`](../submission/evidence/).

## Docs

- https://docs.heycall-e.com/  
- https://github.com/CALLE-AI/call-e-integrations  
- Skill SDK notes: [`../skills/customer-success-voice-signal/references/calle-sdk.md`](../skills/customer-success-voice-signal/references/calle-sdk.md)
- MVF writeup: [`../submission/mvf-feedback.md`](../submission/mvf-feedback.md)
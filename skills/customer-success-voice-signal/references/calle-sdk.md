# CALL-E SDK usage — Stage Manager

How we use `@call-e/calle` on curtain-up, and what we deliberately do **not** invent.

## Dial shape (crash-safe)

```text
calls.create(payload, { idempotencyKey })
        ↓
persist call.id → data/open-calls/<id>.json
        ↓
calls.waitForResult(id)     ← default
```

We **do not** use `createAndWait`. If the process dies after dial, the open-call file still has `call.id` for recovery.

### Optional `webhookUrl`

Set `CALLE_WEBHOOK_URL` to pass `CreateCallInput.webhookUrl`. CALL-E also POSTs the terminal result there.

| Env | Behavior |
| --- | --- |
| `CALLE_WEBHOOK_URL` set, `CALLE_WAIT` unset/true | create → persist → **wait** (webhook is dual delivery) |
| `CALLE_WEBHOOK_URL` set, `CALLE_WAIT=0` | create → persist → **return** (`decision: queued`; completion via webhook) |

## Result mapping (never invent a decision)

Prefer platform fields, in order:

1. **`failureCode`** (call + attempt) → `no_answer` when codes look like voicemail / no_answer / unreachable / busy  
2. **`taskCompleted === false`** → never a 1/2/3  
3. **`completionConfidence` low** (score &lt; 0.45 or label `low`) → `unclear`  
4. **`structuredResult`** (consistent `option_id` / decision / label)  
5. Gated transcript phrases (last resort for option only)  
6. **Summary-string heuristics** — only when **no** failure codes were supplied  

Implementation: `src/map/sdkOutcome.ts` + `src/map/toDecision.ts`.

## Identity read-back (stage code)

Before accepting a 1/2/3 on curtain-up, the callee must speak a **4-digit stage code** (from ticket digits or a stable hash of `event_id`).

- Generated in `src/calle/stageCode.ts`
- Spoken in the task prompt (`src/calle/intent.ts`)
- Required in `resultSchema` as `stage_code` + `identity_confirmed`
- Enforced in `toDecision` — mismatch / missing → `unclear` (not logged as the owner’s decision)

Dress rehearsal simulates option 1 and notes the stage code that *would* be used — no live proof.

## Structured result schema

```json
{
  "option_id": "1"|"2"|"3",
  "decision": "…",
  "decision_label": "…",
  "stage_code": "4821",
  "identity_confirmed": true
}
```

## Related

- Live ladder: [`../../../research/calle-api-notes.md`](../../../research/calle-api-notes.md)
- Auth/env: [auth-and-keys.md](auth-and-keys.md)
- Safety: [safety.md](safety.md)

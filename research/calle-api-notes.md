# CALL-E API notes (Stage Manager)

## Get / rotate API keys

**https://dashboard.heycall-e.com/account/api-keys**

Put the value in `skills/customer-success-voice-signal/.env` as `CALLE_API_KEY` (gitignored).  
Skill docs: [`../skills/customer-success-voice-signal/references/auth-and-keys.md`](../skills/customer-success-voice-signal/references/auth-and-keys.md).

## SDK

- Package: `@call-e/calle` `^0.6.0`
- Entry: `CalleClient` → `client.calls.createAndWait(...)`
- Auth: `CALLE_API_KEY` (Bearer); optional `CALLE_BASE_URL`

## Curtain-up payload

```ts
await client.calls.createAndWait({
  task: intent.task, // Stage Manager script
  recipients: [{ phones: [e164], region, locale }],
  resultSchema: {
    type: "object",
    required: ["option_id", "decision", "decision_label"],
    properties: { /* option_id enum 1|2|3, decision, decision_label */ },
  },
  metadata: {
    skill: "customer-success-voice-signal",
    persona: "Stage Manager",
    never_call_customer: true,
    trigger_id,
    account_id,
  },
});
```

Implemented in `src/calle/client.ts` (`curtainUp`) + `src/calle/intent.ts` (`buildCallIntent`).

## Result mapping

Prefer `call.structuredResult`, fall back to `call.recipients[0].structuredResult`, then transcript digits (`src/map/toDecision.ts`).

If structured result is missing and the summary looks like voicemail / no answer → `decision: no_answer` (never invent a line reading).

## Modes

| Mode | Ring? | Needs key? | Cue-history? |
| --- | --- | --- | --- |
| Dress rehearsal | No | No | No |
| Curtain up | Yes | `CALLE_API_KEY` + `CS_OWNER_E164` + `--live` + `PLACES` | Yes |

## Live probe log (no secrets)

| Date | Cue | Result | Notes |
| --- | --- | --- | --- |
| 2026-08-01 | `stuck_support` | Voicemail → `no_answer` | Auth + dial proven |
| 2026-08-01 | `stuck_support` | **Decision 1** `take_over_chat` | Answered; prompt book OK |
| 2026-08-01 | `agent_needs_decision` | `unclear` | Ring OK; mapping still flaky |

## Docs

- https://docs.heycall-e.com/  
- https://github.com/CALLE-AI/call-e-integrations  

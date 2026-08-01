# CALL-E API notes (Stage Manager)

## SDK

- Package: `@call-e/calle` `^0.6.0`
- Entry: `CalleClient` → `client.calls.createAndWait(...)`
- Auth: `CALLE_API_KEY` (Bearer); optional `CALLE_BASE_URL`

## Curtain-up payload shape

```ts
await client.calls.createAndWait({
  task: intent.task, // Stage Manager script
  recipients: [{ phones: [e164], region, locale }],
  resultSchema: {
    type: "object",
    required: ["option_id", "decision", "decision_label"],
    properties: { /* ... */ },
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

## Result mapping

Prefer `call.structuredResult`, fall back to `call.recipients[0].structuredResult`.
Map via `src/map/toDecision.ts` onto `DecisionResult`.

## Modes

| Mode | Ring? | Cue-history? |
| --- | --- | --- |
| Dress rehearsal | No | No |
| Curtain up | Yes (`createAndWait`) | Yes |

## Docs

- https://docs.heycall-e.com/
- https://github.com/CALLE-AI/call-e-integrations

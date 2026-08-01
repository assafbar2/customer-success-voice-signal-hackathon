# Dev / design plan — Stage Manager skill

**Skill path:** [`skills/customer-success-voice-signal/`](../skills/customer-success-voice-signal/)  
**Persona:** Stage Manager (see [04-stack-hosting-tone.md](./04-stack-hosting-tone.md) §3)

## Phases

| Phase | Status | Notes |
| --- | --- | --- |
| 0 — Docs lock | Done | PRD, architecture, stack/tone |
| 1 — Skill scaffold | Done | Zod schemas, fixtures, dress rehearsal CLI |
| 2 — Policy + writeback | Done | `shouldRing`, prompt book, show report, cue-history on curtain-up only |
| 3 — Curtain-up | Ready | `@call-e/calle` `createAndWait`; gate = `--live` + `PLACES` |
| 4 — Demo video | Next | Dress rehearsal → one live cue → prompt book |
| 5 — awesome-list PR | Next | Package `skills/customer-success-voice-signal/` |

## Runbook (local)

```bash
cd skills/customer-success-voice-signal
npm install && npm test && npm run typecheck
npm run signal -- --fixture stuck_support_acme.json          # dress rehearsal
# curtain-up (operator only):
# npm run signal -- --fixture stuck_support_acme.json --live PLACES
```

## Design anchors

- Callee = CS owner only  
- Four cues as first-class fixtures  
- Closed-set line readings 1/2/3  
- Exit codes: 0 ok · 2 HOLD · 3 failure  

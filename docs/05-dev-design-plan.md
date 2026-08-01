# As-built + remaining — Stage Manager skill

**Skill:** [`skills/customer-success-voice-signal/`](../skills/customer-success-voice-signal/)  
**Tone / glossary:** [04-stack-hosting-tone.md](./04-stack-hosting-tone.md)

## Done

| Piece | Notes |
| --- | --- |
| Docs lock | PRD, architecture, stack/tone |
| Skill scaffold | Zod schemas, 4 fixtures, CLI |
| Policy + writeback | `shouldRing`, prompt book, show report, cue-history (live only) |
| Dress rehearsal | Default; no ring; no `CALLE_API_KEY` required |
| Curtain-up | `@call-e/calle` `createAndWait`; gate = `--live` + `PLACES` |
| Live probe | `stuck_support` answered → decision **1** (`take_over_chat`) |
| Tests | `npm test` · `npm run typecheck` |

## Remaining

| Piece | Notes |
| --- | --- |
| Demo video ≤3 min | Script: [`submission/video-script.md`](../submission/video-script.md) |
| Awesome-list PR | Package `skills/customer-success-voice-signal/` → [awesome-phone-call-agents](https://github.com/CALLE-AI/awesome-phone-call-agents) |
| Devpost package | Video URL + repo PR + CALL-E email |
| Optional | Extra CALL-E quota; polish second live cue (`agent_needs_decision`); Slack webhook |

**Not in scope for this hackathon ship:** demo UI app, DB, real Sentry integrations.

## Runbook

```bash
cd skills/customer-success-voice-signal
npm install && npm test && npm run typecheck

# Dress rehearsal (judges / CI)
npm run signal -- --fixture stuck_support_acme.json
npm run signal -- --fixture agent_needs_decision_acme.json
npm run signal -- --list
npm run signal -- --last

# Curtain-up (operator only — needs .env)
# Keys: https://dashboard.heycall-e.com/account/api-keys
# npm run signal -- --fixture stuck_support_acme.json --live PLACES
```

## Design anchors

- Callee = CS owner only  
- Four cues as first-class fixtures  
- Closed-set line readings 1/2/3  
- Exit codes: `0` ok · `2` HOLD · `3` failure  

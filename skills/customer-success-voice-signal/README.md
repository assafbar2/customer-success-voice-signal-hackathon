# customer-success-voice-signal

**Persona:** Stage Manager  
**Callee:** CS owner only — never the customer  
**Default mode:** Dress rehearsal (no ring)

> When the account is on fire, we cue the firefighter — not the building.

## How judges run this

```bash
cd skills/customer-success-voice-signal
npm install
npm test && npm run typecheck

# Dress rehearsal — no ring, no CALL-E key
npm run signal -- --fixture stuck_support_acme.json
npm run signal -- --stdin < events/webhook_stuck_support.json

# Or: HTTP inbound (deployable listener — same engine)
npm run serve-cue &
curl -sS -X POST http://127.0.0.1:8787/cue \
  -H 'content-type: application/json' \
  -d @events/webhook_stuck_support.json

# Decision → action intent → dry-run apply (no live CRM / Slack)
npm run apply-action -- --last --dry-run
npm run apply-action -- --last
npm run signal -- --list
npm run signal -- --last
```

### Curtain-up (real phone — operator only)

1. Copy `.env.example` → `.env` (never commit `.env`)
2. API key: **https://dashboard.heycall-e.com/account/api-keys**
3. Set `CALLE_API_KEY`, `CS_OWNER_E164`, `SIGNAL_CONFIRM=PLACES`
4. Run: `npm run signal -- --fixture stuck_support_acme.json --live PLACES`
5. Check `data/prompt-book.ndjson`, `data/show-report.md`, and `data/actions/pending/`

Crash recovery / remap (no new ring): `npm run signal -- --fixture stuck_support_acme.json --from-call call_xxx`

### Exit codes

| Code | Meaning |
| --- | --- |
| 0 | Ok — dress rehearsal or curtain-up completed |
| 2 | HOLD — policy / live gate / house dark / placeholder phone |
| 3 | Failure — bad cue, missing key, CALL-E error |

### Safety

- CS owner only; fixture phones (`+1555555…`) rejected on live  
- Curtain-up needs `--live` **and** `PLACES`  
- House dark enforced on live only (owner/env timezone-aware)  
- Per-owner call budget (default 2 live dials / window)  
- Cue-history appends only after a live dial outcome — HOLD never poisons dedupe  
- Prefer SDK `failureCode` / `completionConfidence`; identity stage-code read-back before 1/2/3  

See [references/safety.md](references/safety.md) · [references/calle-sdk.md](references/calle-sdk.md) · [references/action-intents.md](references/action-intents.md) · [SKILL.md](SKILL.md).

## Scripts

| Script | What |
| --- | --- |
| `npm run signal -- …` | Stage Manager CLI |
| `npm run serve-cue` | HTTP listener — `POST /cue` → same engine as `--stdin` |
| `npm run apply-action -- …` | Apply/dry-run pending action intent (local receipt; Slack/GitHub stab is out of MVP) |
| `npm run dry-run -- …` | Force dress rehearsal |
| `npm test` | Vitest (no real calls) |
| `npm run typecheck` | `tsc --noEmit` |

## CLI flags

```text
--fixture <file>   Cue under fixtures/
--trigger <id>     First fixture matching trigger_id
--stdin            Read one JSON cue/event from stdin
--live             Request curtain-up (needs PLACES)
--dry-run          Force dress rehearsal
PLACES             Live gate (or SIGNAL_CONFIRM=PLACES)
--list             List fixtures
--last             Tail prompt book / show report
--from-call <id>   Map an existing CALL-E run (no new ring)
--verbose          Full call sheet preview
--help
```

## Cues

| ID | Fixture | Demo |
| --- | --- | --- |
| `stuck_support` | `stuck_support_acme.json` | Primary live path |
| `agent_needs_decision` | `agent_needs_decision_acme.json` | Second demo cue |
| `sla_risk` | `sla_risk_globex.json` | First-class |
| `health_onboarding` | `health_onboarding_initech.json` | First-class |

Sample non-fixture event: `events/sample_stuck_support.json` (pipe with `--stdin`).

Operator-proven redacted evidence: [`submission/evidence/`](../../submission/evidence/).

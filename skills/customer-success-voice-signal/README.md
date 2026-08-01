# customer-success-voice-signal

**Persona:** Stage Manager  
**Callee:** CS owner only — never the customer  
**Default mode:** Dress rehearsal (no ring)

> When the account is on fire, we cue the firefighter — not the building.

## Quick start

```bash
npm install
npm test
npm run typecheck

# Dress rehearsal
npm run signal -- --fixture stuck_support_acme.json
```

## Scripts

| Script | What it does |
| --- | --- |
| `npm run signal -- …` | Stage Manager CLI |
| `npm run dry-run -- …` | Alias path via `--dry-run` |
| `npm test` | Vitest (no real calls) |
| `npm run typecheck` | `tsc --noEmit` |
| `npm run build` | Emit `dist/` |

## CLI

```text
--fixture <file>   Cue under fixtures/
--trigger <id>     Pick first fixture for trigger
--live             Request curtain-up (needs PLACES)
--dry-run          Force dress rehearsal
PLACES             Live gate confirmation (or SIGNAL_CONFIRM=PLACES)
--list             List fixtures
--last             Tail prompt book / show report
--verbose          Full call sheet preview
--help
```

## Cues (triggers)

| ID | Fixture |
| --- | --- |
| `stuck_support` | `stuck_support_acme.json` |
| `agent_needs_decision` | `agent_needs_decision_acme.json` |
| `sla_risk` | `sla_risk_globex.json` |
| `health_onboarding` | `health_onboarding_initech.json` |

## Curtain-up checklist

1. Copy `.env.example` → `.env` (never commit `.env`)
2. Get / rotate an API key: **https://dashboard.heycall-e.com/account/api-keys**
3. Set `CALLE_API_KEY`, `CS_OWNER_E164`, `SIGNAL_CONFIRM=PLACES`
4. Run: `npm run signal -- --fixture stuck_support_acme.json --live PLACES`
5. Confirm writeback in `data/prompt-book.ndjson` and `data/show-report.md`

Full key-swap notes: [`references/auth-and-keys.md`](references/auth-and-keys.md).

## Layout

See `SKILL.md` for glossary and safety. Source under `src/`, cues under `fixtures/`.

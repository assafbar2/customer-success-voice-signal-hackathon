# Examples — Stage Manager

Fictional reserved numbers only (`+1555555…`). Never put real phones or API keys in samples.

## Dress rehearsal (default — no ring)

```bash
cd skills/customer-success-voice-signal
npm install
npm run signal -- --fixture stuck_support_acme.json
npm run signal -- --stdin < events/sample_stuck_support.json
```

Exit `0`. Writes prompt book + show report. Does **not** append cue-history.

## Curtain-up (opt-in live ring)

Requires local `.env` (`CALLE_API_KEY`, `CS_OWNER_E164`) and typed `PLACES`:

```bash
npm run signal -- --fixture stuck_support_acme.json --live PLACES
```

Callee is the **CS owner only**. Customer is never dialed.

## Policy HOLDs (exit 2)

| Situation | What happens |
| --- | --- |
| `--live` without `PLACES` | HOLD — stays in dress rehearsal |
| Severity below high | HOLD — `severity_below_threshold` |
| House dark (owner/env timezone) | HOLD — no live ring |
| Owner call budget exceeded | HOLD — `owner_budget` |
| Cue already dialed recently | HOLD — `already_cued` |
| Placeholder fixture phone on live | HOLD — `placeholder_phone` |

## Side effects

| Mode | Side effect |
| --- | --- |
| Dress rehearsal | Local files under `data/` only |
| Curtain-up | One CALL-E phone call to `CS_OWNER_E164` + local writeback |

Cancel / do not ring: omit `--live`, or do not type `PLACES`. There is no recurring schedule.

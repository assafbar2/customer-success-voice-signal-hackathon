# Auth and keys

Stage Manager loads env via `src/config/env.ts` (`loadDotEnv` + `readSkillEnv`).

## Get / rotate CALL-E API keys

**Create, copy, or rotate keys here:**

**https://dashboard.heycall-e.com/account/api-keys**

Paste the value into local `.env` as `CALLE_API_KEY=…`.  
Never commit `.env`. Swap keys anytime — no code changes.

Dress rehearsal does **not** need a key. Curtain-up does.

## Required for curtain-up

| Variable | Purpose |
| --- | --- |
| `CALLE_API_KEY` | CALL-E Developer API key from [API keys](https://dashboard.heycall-e.com/account/api-keys) (`CalleClient`) |
| `CS_OWNER_E164` | Real CS owner phone (overrides fixture placeholder) |
| `SIGNAL_CONFIRM` | Must be `PLACES` (or pass `PLACES` on argv with `--live`) |

## Optional

| Variable | Purpose |
| --- | --- |
| `CALLE_BASE_URL` | Default `https://api.heycall-e.com` |
| `CALLE_REGION` / `CALLE_LOCALE` | Recipient region/locale |
| `CS_OWNER_NAME` / `CS_OWNER_ID` | Override call sheet identity |
| `HOUSE_DARK_START` / `HOUSE_DARK_END` | Quiet hours (curtain-up only) |
| `DEDUPE_MINUTES` | Cue-history window |
| `DATA_DIR` | Prompt book / show report directory |
| `SLACK_WEBHOOK_URL` | Reserved for optional writeback |

## Rules

- Never commit `.env`
- Never print API keys or full phone numbers in logs (mask E.164)
- Dress rehearsal does not need `CALLE_API_KEY` to succeed
- Use `.env.example` as the empty placeholder template
- More CALL-E notes: [`../../../research/calle-api-notes.md`](../../../research/calle-api-notes.md)

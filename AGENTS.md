# AGENTS.md

## Cursor Cloud specific instructions

This repo has two runnable products:

1. **Stage Manager** (CALL-E hackathon) at `skills/customer-success-voice-signal/`
   (TypeScript, Node >= 20, npm). `site/` and `submission/demo-reel/` are presentation
   assets, not services.
2. **Sentrants** (living swarm of synthetic Sentry customers) at `sentrants/`
   (Python 3.12, FastAPI CLI). Not the CALL-E product. Dress rehearsal: hatch + serve,
   no LLM. Do not run live model calls unless asked.

### Working directory

Stage Manager commands (`npm test`, `npm run typecheck`, `npm run signal`) must be run from
`skills/customer-success-voice-signal/`, not the repo root. The startup update script installs
dependencies there automatically.

Sentrants commands (`python3 -m pip install -e '.[dev]'`, `python3 -m pytest`,
`python3 -m sentrants hatch`, `python3 -m sentrants serve`) must be run from `sentrants/`.

### Lint / test / build / run

Standard commands are documented in `skills/customer-success-voice-signal/README.md` and
`package.json` scripts. Summary:
- Lint/typecheck: `npm run typecheck` (there is no separate ESLint; `tsc --noEmit` is the lint gate)
- Test: `npm test` (Vitest, no real calls made)
- Build: `npm run build`
- Run (dress rehearsal, default): `npm run signal -- --fixture stuck_support_acme.json`

### Non-obvious caveats

- **Dress rehearsal is the default and needs no secrets.** It never places a phone call and
  simulates the decision (always option 1). This is the correct way to exercise the app without
  CALL-E credentials. Exit code 0 = ok, 2 = HOLD (policy gate), 3 = failure.
- **Curtain-up (live phone calls) is intentionally gated** and should NOT be run in CI/agents.
  It requires a real CALL-E API key + a real CS-owner phone number, and both `--live` and the
  literal `PLACES` confirmation. Fixture placeholder phones (`+1555...`) are rejected on live runs.
  To enable it locally, copy `.env.example` to `.env` and set `CALLE_API_KEY`, `CS_OWNER_E164`,
  `SIGNAL_CONFIRM=PLACES`.
- **Runtime output is written to `skills/customer-success-voice-signal/data/`**
  (`prompt-book.ndjson`, `show-report.md`). This directory is gitignored except for `.gitkeep`;
  files accumulate across runs (NDJSON append), so use `npm run signal -- --last` to inspect the
  latest entry.
- There is no database, Docker, or long-running server for the core product. The CLI runs and exits.

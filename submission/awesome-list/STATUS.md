# Awesome-list PR status

Target: https://github.com/CALLE-AI/awesome-phone-call-agents

## PR URL (paste this on Devpost)

**https://github.com/CALLE-AI/awesome-phone-call-agents/pull/250**

Opened 2026-08-27 by **assafbar2** from a laptop (`open-pr.sh`). Cursor Cloud cannot fork or push CALLE-AI (`cursor[bot]` 403 on this repo’s GitHub App token) — so this agent did **not** open #250. Do **not** open a second PR.

| Field | Value |
| --- | --- |
| Title | `feat(customer-success-voice-signal): add CS owner decision skill` |
| Branch | `feat/customer-success-voice-signal` → `main` |
| State | Open, not draft, mergeable |
| Skill `README.md` | Omitted (their validator rejects it) |
| `SKILL.md` `name:` | `customer-success-voice-signal` |
| References | `examples.md` + `safety.md` present |
| Secrets | `.env.example` placeholders only; no `.env`, `node_modules/`, or `data/` |
| README Skills one-liner | Present (CS / renewal lane, factual) |

## What is already done

- Skill packaged **without** `README.md`.
- `SKILL.md` `name:` matches directory `customer-success-voice-signal`.
- `references/examples.md` and `references/safety.md` present.
- README Skills one-liner ready (CS / renewal lane).
- **`python3 scripts/validate_repository.py` passed** on 2026-08-27 against upstream `main` + this skill (before the PR).
- Branch name `feat/customer-success-voice-signal` passes their `check_branch_name.py`.

## If you re-run the script

`bash submission/awesome-list/open-pr.sh` now prints the existing PR URL and exits. Do not create a second submission PR.

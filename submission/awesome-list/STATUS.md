# Awesome-list PR status

Target: https://github.com/CALLE-AI/awesome-phone-call-agents

**This repo cannot open that PR from Cursor Cloud.** The GitHub App token is scoped to `assafbar2/customer-success-voice-signal-hackathon` only (`cursor[bot]` got 403 on push/fork). Browser session here is not logged into GitHub.

## What is already done

- Skill packaged **without** `README.md` (their validator rejects skill-level README).
- `SKILL.md` `name:` matches directory `customer-success-voice-signal`.
- `references/examples.md` and `references/safety.md` present.
- README Skills one-liner ready (CS / renewal lane).
- **`python3 scripts/validate_repository.py` passed** on 2026-08-27 against upstream `main` + this skill.
- Branch name `feat/customer-success-voice-signal` passes their `check_branch_name.py`.

## What you do (~2 minutes)

**Not** the Cursor Cloud / cursor.com/agents terminal (`/workspace` → `cursor[bot]` 403).

On your **Mac** (Terminal.app or Cursor desktop local terminal):

```bash
pwd
# must be /Users/...  not /workspace
gh api user --jq .login
# must print assafbar2
# if 403:  brew install gh && gh auth login

cd /path/to/customer-success-voice-signal-hackathon
git pull origin main
bash submission/awesome-list/open-pr.sh
```

Paste the printed PR URL into Devpost (“URL to your pull request”) and replace the line below.

## PR URL (fill when opened)

**Not opened yet.** Cloud agent cannot fork or push to CALLE-AI (`cursor[bot]` 403). No `assafbar2/awesome-phone-call-agents` fork exists. Search of `CALLE-AI/awesome-phone-call-agents` for `customer-success-voice-signal` / Stage Manager: **0 PRs**.

Local packaging (2026-08-27, latest upstream `main`): `python3 scripts/validate_repository.py` **passed**; skill `README.md` omitted; branch name `feat/customer-success-voice-signal` valid.

_Paste the GitHub pull request URL here once `open-pr.sh` prints it._

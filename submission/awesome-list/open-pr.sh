#!/usr/bin/env bash
# Open the CALL-E awesome-list PR from YOUR GitHub login on YOUR machine.
# Cursor Cloud / cursor.com/agents terminals cannot do this (cursor[bot] 403).
# Already opened: https://github.com/CALLE-AI/awesome-phone-call-agents/pull/250
# Re-running this script should print that URL and exit — do not open a second PR.
set -euo pipefail

HACKATHON="$(cd "$(dirname "$0")/../.." && pwd)"
SRC="$HACKATHON/skills/customer-success-voice-signal"
WORKDIR="$(mktemp -d)"
trap 'rm -rf "$WORKDIR"' EXIT

howto() {
  cat <<'EOF' >&2

HOW TO RUN THIS (must be YOU, not Cursor Cloud):

  1. Open Terminal on your Mac — Spotlight → Terminal
     or Cursor *desktop* local terminal.

     Check you are NOT on the cloud VM:
       pwd
     WRONG:  /workspace          (cursor.com/agents / Cloud Agent)
     RIGHT:  /Users/yourname/... (your laptop)

  2. Confirm GitHub CLI is you:
       gh api user --jq .login
     Must print:  assafbar2
     WRONG: 403 / "Resource not accessible by integration" / cursor

     If wrong:
       brew install gh          # if gh is missing
       gh auth login            # GitHub.com → HTTPS → Login with a web browser
                                # authenticate as assafbar2

  3. Get this repo on the laptop, then:
       cd /path/to/customer-success-voice-signal-hackathon
       git pull origin main
       bash submission/awesome-list/open-pr.sh

  4. Paste the printed AWESOME_LIST_PR_URL into Devpost and into
     submission/awesome-list/STATUS.md

EOF
}

command -v gh >/dev/null || { echo "Need GitHub CLI (gh)." >&2; howto; exit 1; }
command -v python3 >/dev/null || { echo "Need python3 (used by their validator)." >&2; exit 1; }

if [[ "$HACKATHON" == /workspace || "$PWD" == /workspace || "$PWD" == /workspace/* ]]; then
  echo "ERROR: this is the Cursor Cloud VM (/workspace). gh here is cursor[bot] — it cannot fork CALLE-AI." >&2
  howto
  exit 1
fi

LOGIN="$(gh api user --jq .login 2>/dev/null || true)"
if [[ -z "$LOGIN" || "$LOGIN" == *'{'* || "$LOGIN" == cursor || "$LOGIN" == *'[bot]'* ]]; then
  echo "ERROR: gh is not logged in as you (got ${LOGIN:-empty / 403})." >&2
  howto
  exit 1
fi
if [[ ! "$LOGIN" =~ ^[A-Za-z0-9-]+$ ]]; then
  echo "ERROR: unexpected GitHub login: $LOGIN" >&2
  howto
  exit 1
fi

echo "GitHub user: $LOGIN"
EXISTING="$(gh pr list --repo CALLE-AI/awesome-phone-call-agents --head "$LOGIN:feat/customer-success-voice-signal" --state open --json url --jq '.[0].url // empty' 2>/dev/null || true)"
if [[ -z "$EXISTING" ]]; then
  EXISTING="$(gh pr list --repo CALLE-AI/awesome-phone-call-agents --search "customer-success-voice-signal author:$LOGIN" --state open --json url --jq '.[0].url // empty' 2>/dev/null || true)"
fi
if [[ -n "$EXISTING" ]]; then
  echo "Already open: $EXISTING"
  echo "Do not open a second PR. Paste that URL on Devpost."
  echo "AWESOME_LIST_PR_URL=$EXISTING"
  exit 0
fi
echo "Using skill source: $SRC"
echo "Workdir: $WORKDIR"

# Do not pass --remote: gh rejects it when a repository argument is given.
if ! gh repo fork CALLE-AI/awesome-phone-call-agents --clone=false; then
  echo "ERROR: could not fork CALLE-AI/awesome-phone-call-agents as $LOGIN." >&2
  howto
  exit 1
fi

gh repo clone "$LOGIN/awesome-phone-call-agents" "$WORKDIR/awesome-phone-call-agents"
cd "$WORKDIR/awesome-phone-call-agents"
git remote add upstream https://github.com/CALLE-AI/awesome-phone-call-agents.git 2>/dev/null || true
git fetch upstream
git checkout -B feat/customer-success-voice-signal upstream/main
python3 scripts/check_branch_name.py --branch feat/customer-success-voice-signal

DST="skills/customer-success-voice-signal"
rm -rf "$DST"
mkdir -p "$DST"
python3 - <<PY
import os, shutil
from pathlib import Path
src = Path("$SRC")
dst = Path("$DST")
skip_dirs = {"node_modules", "dist", "data", ".git"}
skip_files = {"README.md", ".env"}
for root, dirs, files in os.walk(src):
    rel = Path(root).relative_to(src)
    dirs[:] = [d for d in dirs if d not in skip_dirs]
    (dst / rel).mkdir(parents=True, exist_ok=True)
    for f in files:
        if f in skip_files or (f.startswith(".env.") and f != ".env.example"):
            continue
        shutil.copy2(Path(root) / f, dst / rel / f)
print("copied", sum(1 for p in dst.rglob("*") if p.is_file()), "files")
assert not (dst / "README.md").exists()
assert (dst / "SKILL.md").exists()
assert (dst / "references" / "examples.md").exists()
assert (dst / "references" / "safety.md").exists()
PY

python3 - <<'PY'
from pathlib import Path
p = Path("README.md")
text = p.read_text()
entry = "- [`customer-success-voice-signal`](skills/customer-success-voice-signal/) - Stage Manager skill that rings the CS owner (never the customer) for stuck-support / SLA / agent-needs-decision / onboarding cues; closed-set 1/2/3 with dress rehearsal by default and prompt-book writeback.\n"
if "skills/customer-success-voice-signal/" not in text:
    idx = text.find("### Skills")
    first = text[idx:].find("\n- [")
    at = idx + first + 1
    p.write_text(text[:at] + entry + text[at:])
    print("inserted README Skills entry")
else:
    print("README entry already present")
PY

python3 scripts/validate_repository.py
git add skills/customer-success-voice-signal README.md
git commit -m "$(cat <<'EOF'
feat(customer-success-voice-signal): add CS owner decision skill

Stage Manager rings the CS owner (never the customer) for stuck-support,
SLA, agent-needs-decision, and onboarding cues. Dress rehearsal by default.
python3 scripts/validate_repository.py passed.
EOF
)"
git push -u origin feat/customer-success-voice-signal
PR_URL="$(gh pr create --repo CALLE-AI/awesome-phone-call-agents \
  --title "feat(customer-success-voice-signal): add CS owner decision skill" \
  --body "$(cat <<'EOF'
## Summary

Adds **customer-success-voice-signal** (Stage Manager): a skill that rings the CS owner — never the customer — for stuck-support / SLA / agent-needs-decision / onboarding cues. Closed-set 1/2/3, dress rehearsal by default, prompt-book writeback.

Hackathon project: https://github.com/assafbar2/customer-success-voice-signal-hackathon
Judge site: https://assafbar2.github.io/customer-success-voice-signal-hackathon/

## Type

- [x] New skill
- [x] README awesome-list entry

## Checklist

- [x] Repository-facing content is written in English.
- [x] Branch name, commit messages, and PR title follow `docs/git-naming-conventions.md`.
- [x] No secrets, tokens, private phone numbers, call recordings, or private transcripts are included.
- [x] Real-world side effects are clearly described.
- [x] Phone numbers are masked in documentation and test fixtures unless they are clearly fictional.
- [x] Recurring workflows include cancellation behavior.
- [x] Runnable code has a dry-run, fake-server, or no-call path by default.
- [x] `python3 scripts/validate_repository.py` passes.
EOF
)"
)"
if [ -z "${PR_URL:-}" ]; then
  PR_URL="$(gh pr list --repo CALLE-AI/awesome-phone-call-agents --head "$LOGIN:feat/customer-success-voice-signal" --json url --jq '.[0].url' 2>/dev/null || true)"
fi
echo
echo "AWESOME_LIST_PR_URL=${PR_URL:-}"
echo "Paste that URL into Devpost and into $HACKATHON/submission/awesome-list/STATUS.md"

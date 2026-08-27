#!/usr/bin/env bash
# Open the CALL-E awesome-list PR from a laptop where YOU are logged into GitHub.
# This cloud agent cannot fork CALLE-AI/awesome-phone-call-agents (GitHub App
# token is scoped to this repo only).
set -euo pipefail

HACKATHON="$(cd "$(dirname "$0")/../.." && pwd)"
SRC="$HACKATHON/skills/customer-success-voice-signal"
WORKDIR="$(mktemp -d)"
trap 'rm -rf "$WORKDIR"' EXIT

command -v gh >/dev/null || { echo "Need GitHub CLI (gh) authenticated as you."; exit 1; }
command -v python3 >/dev/null

echo "Using skill source: $SRC"
echo "Workdir: $WORKDIR"

gh repo fork CALLE-AI/awesome-phone-call-agents --clone=false --remote=false || true
gh repo clone "$(gh api user --jq .login)/awesome-phone-call-agents" "$WORKDIR/awesome-phone-call-agents"
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
  PR_URL="$(gh pr list --repo CALLE-AI/awesome-phone-call-agents --head "$(gh api user --jq .login):feat/customer-success-voice-signal" --json url --jq '.[0].url' 2>/dev/null || true)"
fi
echo
echo "AWESOME_LIST_PR_URL=${PR_URL:-}"
echo "Paste that URL into Devpost and into $HACKATHON/submission/awesome-list/STATUS.md"


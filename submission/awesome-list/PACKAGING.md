# Awesome-list packaging (CALL-E)

Target: [CALLE-AI/awesome-phone-call-agents](https://github.com/CALLE-AI/awesome-phone-call-agents)

This hackathon repo keeps a skill `README.md` for judges. Their validator **rejects** skill-level `README.md` (except one allowlisted skill) and **requires** `references/examples.md` + `references/safety.md`.

Full pre-submit (video · GIF · this PR · **MVF**): [`../PRE-SUBMIT.md`](../PRE-SUBMIT.md).

## Checklist before opening their PR

1. Copy `skills/customer-success-voice-signal/` into their `skills/customer-success-voice-signal/`.
2. **Omit** `README.md` from that copy (keep `SKILL.md`, `references/`, `src/`, `fixtures/`, `events/`, tests).
3. Confirm `references/examples.md` and `references/safety.md` are present.
4. Confirm `SKILL.md` frontmatter `name:` matches the directory slug.
5. Run `python3 scripts/validate_repository.py` in their repo.
6. Add a one-line awesome README entry naming the **CS / renewal** lane (not “generic phone agent”).
7. Branch naming must match their `docs/git-naming-conventions.md` (not this repo’s `cursor/…` prefix).
8. **Pre-submit gate — MVF:** paste [`../mvf-feedback.md`](../mvf-feedback.md) into the Devpost **Most Valuable Feedback** survey in the same window as this PR / Devpost submit. Awesome-list alone is not “submitted.”

Homepage for the project (set on GitHub repo settings if API cannot):  
https://assafbar2.github.io/customer-success-voice-signal-hackathon/

## Suggested README one-liner

> **customer-success-voice-signal** — Stage Manager rings the CS owner (never the customer) for stuck support / SLA / agent-needs-decision / onboarding cues; closed-set 1/2/3 → action intent (Slack/GitHub).

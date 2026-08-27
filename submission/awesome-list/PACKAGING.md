# Awesome-list packaging (CALL-E)

Target: [CALLE-AI/awesome-phone-call-agents](https://github.com/CALLE-AI/awesome-phone-call-agents)

This hackathon repo keeps a skill `README.md` for judges. Their validator **rejects** skill-level `README.md` and **requires** `references/examples.md` + `references/safety.md`.

**Opened:** https://github.com/CALLE-AI/awesome-phone-call-agents/pull/250 — status in [`STATUS.md`](STATUS.md). Laptop one-shot (`open-pr.sh`) already ran; re-running it prints that URL and exits. Manual notes: [`../../notes/SUBMIT.md`](../../notes/SUBMIT.md).

## Copy rules

1. Copy `skills/customer-success-voice-signal/` → their `skills/customer-success-voice-signal/`.
2. **Omit** `README.md`, `node_modules/`, `data/`, `.env`.
3. Keep `SKILL.md`, `references/`, `src/`, `fixtures/`, `events/`, tests.
4. `SKILL.md` frontmatter `name:` must match the directory slug.
5. `python3 scripts/validate_repository.py` in **their** repo.
6. One README Skills entry naming the **CS / renewal** lane.
7. Branch: `feat/customer-success-voice-signal` (see their `docs/git-naming-conventions.md`). **Not** `cursor/…`.

## Suggested README one-liner

```markdown
- [`customer-success-voice-signal`](skills/customer-success-voice-signal/) - Stage Manager skill that rings the CS owner (never the customer) for stuck-support / SLA / agent-needs-decision / onboarding cues; closed-set 1/2/3 with dress rehearsal by default and prompt-book writeback.
```

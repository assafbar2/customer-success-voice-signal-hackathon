# Operator submit — not for judges

This file is the operator playbook. The public README does not link here.

Deadline: **2026-09-14, 11:45 pm SGT** ([official rules](https://call-e.devpost.com/rules)). MVF survey stays open through **2026-09-18, 11:45 pm SGT**.

---

## 1. Demo video (YouTube / Vimeo)

**Uploaded:** https://youtu.be/yvRq7P8F5-c — paste this on the Devpost form.

Source file: `submission/demo-reel/stage-manager-demo.mp4` (~2:08). Judge site still hosts the same cut. GitHub’s file preview often looks silent; YouTube is the submission host.

## 2. Awesome-list PR

**Opened:** https://github.com/CALLE-AI/awesome-phone-call-agents/pull/250

Paste **that PR URL** on Devpost (not this repo). Opened 2026-08-27 by `assafbar2` from a laptop. This cloud agent **cannot** open or update it (`cursor[bot]` is scoped to this repo only). Status: [`../submission/awesome-list/STATUS.md`](../submission/awesome-list/STATUS.md).

Do **not** run `open-pr.sh` again unless you need to reprint the URL — it now exits if #250 is already open.

Packaging notes (already applied in #250): [`../submission/awesome-list/PACKAGING.md`](../submission/awesome-list/PACKAGING.md).

<details>
<summary>How it was opened (do not repeat)</summary>

Hackathon rule: one PR to https://github.com/CALLE-AI/awesome-phone-call-agents.

**Fast path was:** Mac Terminal, `gh api user --jq .login` = `assafbar2`, then `bash submission/awesome-list/open-pr.sh`.

Manual path — their branch names cannot be `cursor/…`:

```bash
git clone https://github.com/CALLE-AI/awesome-phone-call-agents.git
cd awesome-phone-call-agents
python3 scripts/create_branch.py feat/customer-success-voice-signal
```

Copy **this** repo’s skill in, with the differences their validator requires:

```bash
rsync -a --delete \
  --exclude README.md \
  --exclude node_modules \
  --exclude dist \
  --exclude data \
  --exclude .env \
  --exclude .env.* \
  ../customer-success-voice-signal-hackathon/skills/customer-success-voice-signal/ \
  skills/customer-success-voice-signal/
```

Keep `.env.example` (not matched by `.env.*` if you copy file-by-file; `open-pr.sh` keeps it). **Omit** skill `README.md`. Keep `SKILL.md`. Keep `references/examples.md` and `references/safety.md`. `SKILL.md` frontmatter `name:` must equal `customer-success-voice-signal`.

README Skills one-liner:

```markdown
- [`customer-success-voice-signal`](skills/customer-success-voice-signal/) - Stage Manager skill that rings the CS owner (never the customer) for stuck-support / SLA / agent-needs-decision / onboarding cues; closed-set 1/2/3 with dress rehearsal by default and prompt-book writeback.
```

Commit style: `feat(customer-success-voice-signal): add CS owner decision skill`

</details>

## 3. Devpost project (Most Practical package)

1. Sign in at https://call-e.devpost.com/ with the email on your **CALL-E account**.
2. Register for the hackathon if the button still says Join.
3. **Enter a Submission** (or Edit if a draft exists).
4. Paste from [`../submission/devpost.md`](../submission/devpost.md):
   - Project name: **Stage Manager**
   - Tagline: **Ack is not a decision.**
   - Description: the “Full description” section
   - Built with: `typescript` `node` `call-e` `vitest` `zod`
5. Required links:
   - GitHub repo: `https://github.com/assafbar2/customer-success-voice-signal-hackathon`
   - Awesome-list **PR URL:** https://github.com/CALLE-AI/awesome-phone-call-agents/pull/250
   - Demo video: https://youtu.be/yvRq7P8F5-c
   - Optional demo app: judge site `https://assafbar2.github.io/customer-success-voice-signal-hackathon/`
   - CALL-E account email
6. Submit. You can edit until the deadline.

## 4. MVF survey (separate prize)

**Most Valuable Feedback** is **not** a field on the project form. It is a **separate CALL-E Feedback Survey** (5 × $200 + credits). Rules: one submission per person; it is awarded to **you**, not the project, and will not show on the project page.

**Submitted 2026-08-27** from [`../submission/mvf-feedback.md`](../submission/mvf-feedback.md) (ranked friction: DTMF, structured-result flakiness, `failureCode` docs, identity challenge). Confirm or edit:

https://docs.google.com/forms/d/e/1FAIpQLSfGWkt2F_ED6aLatQjtjBX8YEpBVQ47A39yeDd1KQRKX488Lg/viewform?usp=form_confirm&edit2=2_ABaOnufgH5C--yO4GwGkPGJicH5_pqVl5g81j3ndR2nLoqtuacRYq0PRI1xu1HSkdKZmEOQ

Do **not** submit a second form. Discord share was left unchecked (not posted). Feedback window: through **18 Sep 2026, 11:45 pm SGT**.

## 5. GitHub polish (once)

Repo Settings:

- Homepage URL already points at Pages. Keep it.
- **Social preview:** uploaded (`site/og.png` → GitHub Settings → Social preview). Live card uses `repository-images.githubusercontent.com`. Pages also serves https://assafbar2.github.io/customer-success-voice-signal-hackathon/og.png.
- Description can stay: voice signals for Customer Success — ring the CS owner, not the customer.
- Topics are fine; `site-operator` is optional to remove (cosmetic).

Do not commit `.env` or `skills/.../data/` (gitignored). Slack/GitHub adapters stay a stab — do not fire.

## 6. “Cloud” in Cursor — no extra GitHub push

**Cloud** under the agent input means the agent runs on a Cursor VM, not on your laptop. It is not a “you still need to push” badge.

- This agent **already pushes** to GitHub (`cursor/…` branches + PRs). You review/merge. You do **not** re-push those commits from the laptop.
- After merge, a laptop still needs a normal `git pull` to see `main`.
- Conversation lives at https://cursor.com/agents (this run: https://cursor.com/agents/bc-b19f74d3-3788-4666-806c-09770b724ac1). Code lives on GitHub after push. There is no magic laptop↔cloud folder sync. Uncommitted local files do **not** move to Cloud.
- **Android:** no native app yet. Open cursor.com/agents in Chrome; you can Install App (PWA). Follow-ups and PR review, not a full IDE.
- Another laptop: same agent URL. Then `git fetch` / checkout the branch (or `git pull` after merge) if you want the files locally.

## 7. Devpost “What to Submit” vs this repo (2026-08-27)

Checked against https://call-e.devpost.com/ and [official rules](https://call-e.devpost.com/rules). You submit the **Devpost form** yourself.

| Requirement | Ready? | Where |
| --- | --- | --- |
| Functional project using CALL-E SDK / SKILL (TypeScript) | Yes | `skills/customer-success-voice-signal/` — 93 tests, dress rehearsal default |
| English description of features | Yes | [`../submission/devpost.md`](../submission/devpost.md) — name **Stage Manager**, tagline **Ack is not a decision.** |
| PR to `CALLE-AI/awesome-phone-call-agents` (Agent Skills) | **Yes** | https://github.com/CALLE-AI/awesome-phone-call-agents/pull/250 — paste **that** URL on Devpost, not this repo |
| Demo video &lt; 3 min, **public YouTube or Vimeo** | **Yes** | https://youtu.be/yvRq7P8F5-c (~2:08) |
| CALL-E account email | You type it | `assaf.barnir@sentry.io` |
| Optional demo app URL | Yes (live) | https://assafbar2.github.io/customer-success-voice-signal-hackathon/ |
| Join the hackathon on Devpost | You | If the button still says **Join hackathon**, register first |
| MVF Feedback Survey (separate prize) | **Submitted** | [`../submission/mvf-feedback.md`](../submission/mvf-feedback.md) |

Validated this sitting: `npm test` (93) + `npm run typecheck` + dress rehearsal fixture + `POST /cue` (`decision: take_over_chat`) + `apply-action --last --dry-run` + awesome-list validator. Did **not** run curtain-up. Slack/GitHub adapters were **not** fired.

2026-08-27 later: recorded https://github.com/CALLE-AI/awesome-phone-call-agents/pull/250 in this repo.

**Devpost submitted:** https://devpost.com/software/stage-manager-customer-success-support

Public-page review: required fields are filled (PR #250, YouTube embed, CALL-E email on the form/story, demo app, submitted to CALL-E). Cleanup: delete the `iams_live_…` key line from the Story, rotate that key, drop “paste that URL…” / broken `mvf-feedback.md` links. Optional: add the GitHub repo as a source URL. Clean Story paste: [`../submission/devpost.md`](../submission/devpost.md).

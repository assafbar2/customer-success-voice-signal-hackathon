# Pre-submit checklist — Stage Manager

Do these **before** Devpost / awesome-list / video publish. Drafts live under `submission/`.

## Prize tracks (both)

| Track | What to submit | Draft |
| --- | --- | --- |
| **Most Practical** | Repo + video + awesome-list skill | `devpost.md` · `video-script.md` |
| **Most Valuable Feedback (MVF)** | Devpost MVF survey | [`mvf-feedback.md`](mvf-feedback.md) |

MVF is a separate prize (~5 × $200 + credits). Same judges read it. Fill it when you submit Devpost — do not leave it for “later.”

---

## 1 — Demo video (≤3 min)

Script: [`video-script.md`](video-script.md) · reel notes: [`demo-reel/README.md`](demo-reel/README.md)

- [ ] Shoot/edit per script (cold open on ring preferred)
- [ ] Stage code + line reading visible on live beat
- [ ] Decision → prompt book (action-intent dry-run optional; Slack/GitHub live send is out of scope)
- [ ] End card: repo + skill path + *“No customers were called…”*
- [ ] **Before upload:** paste MVF from [`mvf-feedback.md`](mvf-feedback.md) into the Devpost MVF survey (same submit session as the video)

## 2 — Terminal GIF (video-before-the-video)

Cheap social/README asset — dress rehearsal loop judges can see without pressing play.

- [ ] Capture: `npm run signal -- --fixture stuck_support_acme.json` (large terminal font)
- [ ] Optional second loop: `serve-cue` + `curl POST /cue` or `apply-action --last --dry-run` (do **not** live-send Slack)
- [ ] Drop into README + site
- [ ] Caption / alt text mentions **Most Practical** demo; README link to [`mvf-feedback.md`](mvf-feedback.md) so MVF isn’t invisible next to the GIF

## 3 — Skill submission list (awesome-list PR)

Packaging: [`awesome-list/PACKAGING.md`](awesome-list/PACKAGING.md)  
Target: https://github.com/CALLE-AI/awesome-phone-call-agents

- [ ] Follow PACKAGING.md (omit skill `README.md`; keep `examples.md` + `safety.md`)
- [ ] Validator passes
- [ ] README one-liner names **CS / renewal** lane
- [ ] **Pre-submit gate:** MVF survey drafted/submitted (`mvf-feedback.md`) — do not open the awesome-list PR as the only leftover; ship MVF in the same push window as Devpost

## 4 — Devpost form

- [ ] Copy body from [`devpost.md`](devpost.md)
- [ ] Link repo + Pages site + video
- [ ] **MVF survey** ← paste [`mvf-feedback.md`](mvf-feedback.md)
- [ ] Social preview / OG image uploaded on GitHub

## Operator pointers

| Item | Path |
| --- | --- |
| Status log | [`../notes/STATUS.md`](../notes/STATUS.md) |
| Sep 1 nudge | [`../notes/REMINDER-2026-09-01.md`](../notes/REMINDER-2026-09-01.md) |
| Deadline | **2026-09-14, 11:45 am SGT** (rules page) |

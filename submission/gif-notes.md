# Terminal GIF — dress rehearsal (pre-submit)

Cheap “video before the video” for README + site. Do this before Devpost upload.

## Capture

```bash
cd skills/customer-success-voice-signal
npm install
# Large font, ~12–15s loop
npm run signal -- --fixture stuck_support_acme.json
```

Optional second clip (seam visible):

```bash
npm run serve-cue &
curl -sS -X POST http://127.0.0.1:8787/cue \
  -H 'content-type: application/json' \
  -d @events/webhook_stuck_support.json
npm run apply-action -- --last --dry-run
```

## Checklist

- [ ] GIF shows Stage Manager / dress rehearsal / line readings 1–2–3 (no secrets)
- [ ] Embedded in root `README.md` and `site/` (or linked)
- [ ] Alt/caption: dress rehearsal — no ring, no API key
- [ ] **MVF:** same pre-submit pass as the GIF — paste [`mvf-feedback.md`](mvf-feedback.md) into the Devpost Most Valuable Feedback survey (don’t treat GIF as “done” while MVF is unchecked)

Full pre-submit: [`PRE-SUBMIT.md`](PRE-SUBMIT.md).

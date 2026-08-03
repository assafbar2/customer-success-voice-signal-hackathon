# Safety — Stage Manager

## Hard rules

1. **CS owner only.** Never cue a call to the end customer.
2. **Dress rehearsal by default.** No ring unless curtain-up gates pass.
3. **Live gate:** `--live` **and** type/env `PLACES`.
4. **Placeholder phones** (`+1555555…` fixtures) are rejected on curtain-up via `requireLivePhone`.
5. **House dark** (quiet hours) is enforced only on curtain-up, evaluated in the owner/env IANA timezone. Dress rehearsal may run at night with a note.
6. **Consent / opt-in:** `cs_owner.opt_in_phone` must be true or the cue is HOLD.
7. **Closed-set line readings only** (options 1/2/3). No open-ended discovery interview.
8. **No medical, emergency, legal advice, or harassment** workflows.
9. **Do not log secrets.** Mask phones; never print `CALLE_API_KEY`.
10. **Dedupe:** cue-history appends only after a live dial outcome. Curtain-up HOLD (house dark, live gate, placeholder, owner budget) does **not** poison dedupe. Dress rehearsal never appends.
11. **Owner budget:** max live dials per CS owner inside the dedupe window (`OWNER_MAX_RINGS`, default 2) — the phone stays rare across many accounts.
12. **Untrusted cue data:** brief/summary/ticket are wrapped as data-only context; never treated as instructions.
13. **Concurrent dials:** exclusive per-cue file lock before curtain-up.
14. **Failure audit:** CALL-E errors write a redacted prompt-book failure row without cue-history.

## HOLD vs failure

| Exit | When |
| --- | --- |
| 2 HOLD | Policy stop, missing PLACES, house dark, placeholder phone, opt-out, owner budget |
| 3 failure | Bad cue, missing API key on curtain-up, CALL-E transport error |

## Branding

Sentry-**shaped**, not Sentry-**branded**. Fictional accounts only (Acme, Globex, Initech).

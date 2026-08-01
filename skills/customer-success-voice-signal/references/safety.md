# Safety — Stage Manager

## Hard rules

1. **CS owner only.** Never cue a call to the end customer.
2. **Dress rehearsal by default.** No ring unless curtain-up gates pass.
3. **Live gate:** `--live` **and** type/env `PLACES`.
4. **Placeholder phones** (`+1555555…` fixtures) are rejected on curtain-up via `requireLivePhone`.
5. **House dark** (quiet hours) is enforced only on curtain-up. Dress rehearsal may run at night with a note.
6. **Consent / opt-in:** `cs_owner.opt_in_phone` must be true or the cue is HOLD.
7. **Closed-set line readings only** (options 1/2/3). No open-ended discovery interview.
8. **No medical, emergency, legal advice, or harassment** workflows.
9. **Do not log secrets.** Mask phones; never print `CALLE_API_KEY`.
10. **Dedupe:** curtain-up appends cue-history; dress rehearsal does not (so demos re-run).

## HOLD vs failure

| Exit | When |
| --- | --- |
| 2 HOLD | Policy stop, missing PLACES, house dark, placeholder phone, opt-out |
| 3 failure | Bad fixture, missing API key on curtain-up, CALL-E transport error |

## Branding

Sentry-**shaped**, not Sentry-**branded**. Fictional accounts only (Acme, Globex, Initech).

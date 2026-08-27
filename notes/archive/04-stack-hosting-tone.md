# Stack · submission · Stage Manager tone

## 1. Stack (as built)

| Layer | Choice |
| --- | --- |
| Language / runtime | TypeScript · Node 20+ |
| Package | `skills/customer-success-voice-signal/` (npm) |
| CALL-E | `@call-e/calle` → `CalleClient.calls.createAndWait` |
| Surface | CLI — `npm run signal` |
| Validation | Zod |
| Config | `.env` + JSON fixtures — **no DB** |
| Writeback | `prompt-book.ndjson` · `show-report.md` · `cue-history.ndjson` (live only) |
| Tests | vitest (no real calls in CI) |

### Explicit non-stack

- No Postgres/Redis  
- No real Sentry API  
- No demo UI app yet  
- Slack webhook optional / unused in MVP  
- No customer telephony beyond CALL-E  

### Layout

```text
customer-success-voice-signal-hackathon/
├── docs/
├── notes/STATUS.md
├── research/calle-api-notes.md
├── submission/video-script.md
└── skills/customer-success-voice-signal/
    ├── SKILL.md
    ├── src/          # see 03-architecture-flow.md
    └── fixtures/
```

---

## 2. Submission (what judges need)

| Required | What |
| --- | --- |
| Yes | Working project; CALL-E at runtime |
| Yes | PR to [awesome-phone-call-agents](https://github.com/CALLE-AI/awesome-phone-call-agents) |
| Yes | Devpost + PR URL + ≤3 min video |
| Yes | CALL-E account email |
| Optional | Hosted demo URL — **not required**; CLI + video is enough |

**Secrets:** `CALLE_*` / phones never committed. Keys: https://dashboard.heycall-e.com/account/api-keys  

**Win on video**, not uptime. Dress rehearsal first, then one curtain-up.

---

## 3. Tone — Stage Manager

**High-stakes CS problem, backstage delivery.** Short cues, closed-set line readings, dry wit — no corporate synergy.

| Do | Don’t |
| --- | --- |
| Theater ops vocabulary (hard) | Generic “AI assistant” voice |
| Dry wit, short lines | Synergy / pitch-deck fluff |
| “Cueing you, not the customer” | Jokes about customers or burn-out |
| README that smiles | Undermining safety / consent |

### Glossary

| Term | Meaning |
| --- | --- |
| **Dress rehearsal** | Dry-run. Default. No ring. |
| **Curtain up** | Live CALL-E (`--live` + `PLACES`). |
| **Cue** | Trigger event on a named account. |
| **Line readings** | Closed-set options 1 / 2 / 3. |
| **Prompt book** | NDJSON audit (`data/prompt-book.ndjson`). |
| **Show report** | Markdown writeback (`data/show-report.md`). |
| **House dark** | Quiet hours — curtain-up only. |
| **Call sheet** | Who we may ring (CS allowlist). |
| **HOLD** | Policy stop; exit code 2. |

### Microcopy

**Tagline:** *When the account is on fire, we cue the firefighter — not the building.*

**On the call:**

- “Hi Maya. Stage Manager. You're up for Acme.”  
- “Line reading. Press or say 1, 2, or 3.”  
- “Confirming option 1. Logging to the prompt book.”  

**CLI:**

- `Dress rehearsal (no ring)`  
- `Curtain up — this rings the CS owner`  
- `HOLD: …`  

### Safety stays straight-faced

Funny **around** the product, never about emergency/medical, harassment, or leaking data. Consent, call sheet, and house dark stay serious.

### Demo video

One Stage Manager chuckle → cue → dress rehearsal → curtain-up → prompt book. Delight + clarity, not stand-up.

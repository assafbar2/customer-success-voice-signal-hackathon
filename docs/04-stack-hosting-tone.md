# Tech stack · hosting · tone

## 1. Tech stack (locked proposal)

| Layer | Choice | Why |
| --- | --- | --- |
| Language | **TypeScript** | CALL-E ecosystem is TS-friendly; fast skill/app scaffolding |
| Runtime | **Node.js 20+** | CLI + small web demo |
| Package | **npm** workspace / single package | Simple for judges |
| CALL-E | **`@call-e/calle` `CalleClient.createAndWait`** | Required for hackathon; runtime, not mock-only |
| API shape | **CLI-first** skill (`npm run signal`) | Optional thin UI later |
| Validation | **Zod** | Event + DecisionResult schemas |
| Config | `.env` + JSON fixtures | No DB for MVP |
| Persistence MVP | **Prompt book NDJSON** + **show report** markdown | Free, portable, honest |
| Optional writeback | Slack incoming webhook | One env var |
| Tests | **vitest** + dress-rehearsal fixtures | No real calls in CI |
| Package for PR | Agent **Skill** folder `customer-success-voice-signal/` | Matches awesome-phone-call-agents |

### Explicit non-stack (MVP)

- No Postgres/Redis  
- No real Sentry API  
- No customer telephony beyond CALL-E  
- No heavy frontend framework (React only if Vite demo needs it; keep UI dumb)

### Default monorepo layout (this repo)

```text
customer-success-voice-signal-hackathon/   # GitHub name
├── docs/
├── skills/
│   └── customer-success-voice-signal/
│       ├── SKILL.md
│       ├── package.json
│       ├── src/
│       └── fixtures/
└── apps/demo-console/     # optional thin UI to fire triggers
```

*(Local folder may stay `calle-hackathon-2026` or be renamed to match GitHub.)*

---

## 2. Hosting (free) + hackathon rules

### Hackathon requirements (from official rules)

| Required? | What |
| --- | --- |
| **Yes** | Working project; CALL-E used at runtime |
| **Yes** | PR to [awesome-phone-call-agents](https://github.com/CALLE-AI/awesome-phone-call-agents) |
| **Yes** | Devpost submission + PR URL |
| **Yes** | Public demo **video** ≤3 min (YouTube/Vimeo) |
| **Yes** | CALL-E account email |
| **Optional** | URL to functional demo app |
| **Yes if private demo** | Login credentials for judges if site is private |

**No requirement** for a specific cloud, paid hosting, or always-on multi-region deploy. Judges may judge from **video + description** only.

### Free hosting options (if we expose a demo URL)

| Host | Fit | Notes |
| --- | --- | --- |
| **Railway / Render free tier** | Small Node API | Sleeps on free tier — say so in README |
| **Fly.io free allowance** | Node | Good enough for demo window |
| **Vercel** | Static demo UI + serverless routes | Fine if CALL-E secrets stay server-side |
| **Local + ngrok / Cloudflare Tunnel** | Live judging only | Fragile; video still primary |
| **GitHub only** | Skill + CLI dress rehearsal | Totally valid if video shows real call |

**Recommendation:**  
1. **Ship skill + CLI** as the core (always works offline from clone).  
2. Optional **demo console** on **Vercel or Render free**.  
3. **Win on video**, not uptime. Put dress rehearsal in the video first, then one curtain-up.

### Secrets

- `CALLE_*` / CLI auth: never commit  
- Demo deploy: env vars on host  
- Fixtures use fictional phones  

---

## 3. Tone — Stage Manager (locked persona)

### Principle

**High-stakes CS problem, backstage delivery.**  
The Stage Manager keeps the show moving: short cues, closed-set line readings, no drama about drama.

### Voice

| Do | Don’t |
| --- | --- |
| Theater ops vocabulary (hard) | Generic “AI assistant” voice |
| Dry wit, short lines | Corporate “synergy” |
| Self-aware Stage Manager (“I’m cueing you, not the customer”) | Cruel jokes about customers or CS burn-out |
| Line readings with personality | Meme spam mid-call |
| README that smiles | Undermining safety / consent |

### Glossary (use these terms in docs and CLI)

| Term | Meaning |
| --- | --- |
| **Dress rehearsal** | Dry-run. Default. No ring. |
| **Curtain up** | Live CALL-E call (`--live` + `PLACES`). |
| **Cue** | A trigger event on a named account. |
| **Cue sheet** | Catalog of fixtures / trigger ids. |
| **Line readings** | Closed-set options 1 / 2 / 3. |
| **Prompt book** | NDJSON audit of cues + decisions. |
| **Show report** | Markdown writeback after a cue. |
| **House dark** | Quiet hours — enforced on curtain-up only. |
| **Call sheet** | Who we may ring (CS owner allowlist). |
| **HOLD** | Policy stop; exit code 2. |

### Microcopy examples

**Product tagline options:**

- *The only CS notification that can’t hide under Slack.*  
- *When the account is on fire, we cue the firefighter — not the building.*  
- *Stage Manager for Customer Success. Dashboards are optional; picking up is not.*  

**On the call (Stage Manager):**

- “Stage Manager for Acme — this is a cue, not a crisis hotline. Well — account crisis. Small c.”  
- “Line readings. Option 3 is ‘not now,’ also known as the honest choice.”  
- “Confirming option 2. Logging to the prompt book.”  

**After decision:**

- “Logged. You may return to your regularly scheduled Slack.”  
- “Decision locked. House to half.”  

**UI / CLI:**

- `Dress rehearsal (no ring)`  
- `Curtain up — this rings the CS owner`  
- Empty state: `No cues. Either the house is quiet, or nobody’s looking.`  

### Safety still serious

Funny **around** the product, never about:

- Emergency / medical  
- Harassment or spam  
- Leaking customer data  

Consent, call sheet, house dark stay straight-faced.

### Demo video tone

Open with one Stage Manager line → show the cue → dress rehearsal → curtain-up → prompt book.  
Judges remember **delight + clarity**, not stand-up.

# Tech stack · hosting · tone

## 1. Tech stack (locked proposal)

| Layer | Choice | Why |
| --- | --- | --- |
| Language | **TypeScript** | CALL-E ecosystem is TS-friendly; fast skill/app scaffolding |
| Runtime | **Node.js 20+** | CLI + small web demo |
| Package | **npm** workspace / single package | Simple for judges |
| CALL-E | **CLI + MCP tools** (`plan_call`, `run_call`, `get_call_run`) via `@call-e/cli` / integrations | Required for hackathon; runtime, not mock-only |
| API shape | Thin **Hono** or **Express** demo server *or* CLI-first + static UI | Prefer **CLI + minimal Vite UI** if we want a browser “Fire signal” button |
| Validation | **Zod** | Event + DecisionResult schemas |
| Config | `.env` + JSON fixtures | No DB for MVP |
| Persistence MVP | **JSON/NDJSON files** on disk (audit log, last decisions) | Free, portable, honest |
| Optional writeback | Slack incoming webhook | One env var |
| Tests | **vitest** + dry-run fixtures | No real calls in CI |
| Package for PR | Agent **Skill** folder `customer-success-voice-signal/` | Matches awesome-phone-call-agents |

### Explicit non-stack (MVP)

- No Postgres/Redis  
- No real Sentry API  
- No customer telephony beyond CALL-E  
- No heavy frontend framework (React only if Vite demo needs it; keep UI dumb)

### Default monorepo layout (this repo)

```text
customer-success-voice-signal-hackathon/   # GitHub name
├── docs/                  # already started as calle-hackathon-2026/docs
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
| **GitHub only** | Skill + CLI dry-run | Totally valid if video shows real call |

**Recommendation:**  
1. **Ship skill + CLI** as the core (always works offline from clone).  
2. Optional **demo console** on **Vercel or Render free**.  
3. **Win on video**, not uptime. Put dry-run in the video first, then one real CALL-E call.

### Secrets

- `CALLE_*` / CLI auth: never commit  
- Demo deploy: env vars on host  
- Fixtures use fictional phones  

---

## 3. Tone — light, funny, judges should chuckle

### Principle

**High-stakes CS problem, low-pomp delivery.**  
We’re not clownish about outages — we’re human about the absurdity of “please check the dashboard at 2am.”

### Voice

| Do | Don’t |
| --- | --- |
| Dry wit, short lines | Corporate “synergy” |
| Self-aware agent (“I’m the annoying-but-useful ring”) | Cruel jokes about customers or CS burn-out |
| Option labels with personality | Meme spam mid-call |
| README that smiles | Undermining safety / consent |

### Microcopy examples

**Product tagline options:**

- *The only CS notification that can’t hide under Slack.*  
- *When the account is on fire, we call the firefighter — not the building.*  
- *Voice signal for Customer Success. Dashboards are optional; picking up is not.*  

**On the call (light):**

- “Sorry to interrupt your meeting about meetings…”  
- “This is a voice signal, not a crisis hotline. Well — account crisis. Small c.”  
- “Option 3 is ‘not now,’ also known as the honest choice.”  

**After decision:**

- “Logged. You may return to your regularly scheduled Slack.”  
- “Decision locked. The robots will pretend they knew.”  

**UI / CLI:**

- Button: `Fire voice signal (dry-run)`  
- Button: `Actually ring CS (this is not a drill… ok it kind of is)`  
- Empty state: `No signals. Either everything is fine, or nobody’s looking. Sus.`  

### Safety still serious

Funny **around** the product, never about:

- Emergency / medical  
- Harassment or spam  
- Leaking customer data  

Consent, allowlist, quiet hours stay straight-faced.

### Demo video tone

Open with one chuckle line → show the problem → call → writeback.  
Judges remember **delight + clarity**, not stand-up.

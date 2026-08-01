# customer-success-voice-signal-hackathon

**Product:** [`customer-success-voice-signal`](docs/02-prd.md) · **Persona:** Stage Manager  
**Hackathon:** [CALL-E: Your Code Is Calling](https://call-e.devpost.com/)  
**PR:** https://github.com/assafbar2/customer-success-voice-signal-hackathon/pull/1  

> *When the account is on fire, we cue the firefighter — not the building.*

When a named account hits a high-risk **cue**, the **Stage Manager** rings the **CS owner** (not the customer) with a short brief and line readings; the decision lands in the **prompt book** / **show report**.

---

## Judge site + demo reel

- **Landing page (source):** [`site/`](site/) — Stage Manager one-pager for judges  
  - **Vercel:** import the repo, root directory `site` → https://vercel.com/new/clone?repository-url=https://github.com/assafbar2/customer-success-voice-signal-hackathon&root-directory=site  
  - **GitHub Pages:** workflow [`.github/workflows/pages.yml`](.github/workflows/pages.yml) (enable Pages → Source: GitHub Actions after first push)
- **Self-made demo video (~70s TTS):** [`submission/demo-reel/stage-manager-demo.mp4`](submission/demo-reel/stage-manager-demo.mp4) · rebuild: `bash submission/demo-reel/build.sh`  
  - Script: [`submission/video-script.md`](submission/video-script.md)  
  - Honest note: voice is espeak (robotic). Swap VO later for a human take if you want polish.

## How judges run this

```bash
git clone https://github.com/assafbar2/customer-success-voice-signal-hackathon.git
cd customer-success-voice-signal-hackathon/skills/customer-success-voice-signal
npm install
npm test && npm run typecheck

# 1) Dress rehearsal — default, no ring, no CALL-E key
npm run signal -- --fixture stuck_support_acme.json
npm run signal -- --fixture agent_needs_decision_acme.json
npm run signal -- --list
npm run signal -- --last

# 2) Curtain-up — real phone (operator only)
# Get a key: https://dashboard.heycall-e.com/account/api-keys
# cp .env.example .env  → set CALLE_API_KEY, CS_OWNER_E164, SIGNAL_CONFIRM=PLACES
# npm run signal -- --fixture stuck_support_acme.json --live PLACES
```

Full skill docs: [`skills/customer-success-voice-signal/README.md`](skills/customer-success-voice-signal/README.md) · [`SKILL.md`](skills/customer-success-voice-signal/SKILL.md)

| Exit | Meaning |
| --- | --- |
| 0 | Ok |
| 2 | HOLD (policy / live gate / house dark) |
| 3 | Failure |

**Safety:** CS owner only · dress rehearsal default · curtain-up needs `--live` + `PLACES` · fixture phones never dialed live.

---

## Docs map

| Path | Purpose |
| --- | --- |
| [docs/02-prd.md](docs/02-prd.md) | Product decisions |
| [docs/03-architecture-flow.md](docs/03-architecture-flow.md) | As-built flow + modules |
| [docs/04-stack-hosting-tone.md](docs/04-stack-hosting-tone.md) | Stack + Stage Manager glossary |
| [docs/05-dev-design-plan.md](docs/05-dev-design-plan.md) | Done / remaining runbook |
| [docs/01-ideas-1-2-5.md](docs/01-ideas-1-2-5.md) | Historical idea exploration |
| [notes/STATUS.md](notes/STATUS.md) | Status log |
| [submission/video-script.md](submission/video-script.md) | ≤3 min demo script |
| [skills/…](skills/customer-success-voice-signal/) | **Stage Manager skill** |

## Official links

- Devpost: https://call-e.devpost.com/  
- Rules: https://call-e.devpost.com/rules  
- **CALL-E API keys:** https://dashboard.heycall-e.com/account/api-keys  
- **Submit PR here:** https://github.com/CALLE-AI/awesome-phone-call-agents  
- Extra calls form: https://forms.gle/EPQttEZ1rkW8iq9q6  

## MVP choices

| | |
| --- | --- |
| Callee | CS only |
| Triggers | stuck support · SLA · agent needs decision · health/onboarding |
| Default | Dress rehearsal (no ring) |
| Live gate | `--live` + `PLACES` |
| Surface | CLI (no demo UI yet) |

## Remaining

- [ ] Demo video ≤3 min  
- [ ] PR to awesome-phone-call-agents + Devpost  
- [ ] Request extra CALL-E calls if quota tight  
- [x] Skill scaffold + dress rehearsal  
- [x] Curtain-up path (`stuck_support` → decision 1)  

## Judging (equal weight)

1. Real World Impact  
2. Quality of the Idea  
3. Technical Implementation (CALL-E at runtime)  
4. Product Experience & Demo (≤3 min video)

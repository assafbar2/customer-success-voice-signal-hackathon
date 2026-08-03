# customer-success-voice-signal-hackathon

**Product:** Stage Manager · skill id [`customer-success-voice-signal`](skills/customer-success-voice-signal/)  
**Hackathon:** [CALL-E: Your Code Is Calling](https://call-e.devpost.com/) · aiming **Most Practical**  
**Live site:** https://assafbar2.github.io/customer-success-voice-signal-hackathon/

> Every company pages an engineer when a server goes down. Nobody pages the human who owns the renewal when the account goes quiet.
>
> *PagerDuty phones you to acknowledge an alert. Ack is not a decision.*

When a named account hits a high-risk **cue**, **Stage Manager** rings the **CS owner** (never the customer) with a ~60s closed-set line reading (1/2/3). The decision is **state** in the prompt book — not a chat ack.

---

## Why this vs paging tools

| | PagerDuty / Opsgenie-style page | Stage Manager |
| --- | --- | --- |
| Who | On-call engineer | **CS owner** of a named account |
| Output | Acknowledge / escalate | **Closed-set CS decision** (take over, approve A/B, own ticket…) |
| Audit | Incident timeline | Prompt book + show report |
| Default | Live page | **Dress rehearsal** — live needs `--live` + `PLACES` |

Lane check: awesome-list phone agents already cover deploy approvals; **B2B customer success / renewal** is still open.

## Judge site

- Source: [`site/`](site/) via **GitHub Pages** (GitHub Actions)  
- URL: https://assafbar2.github.io/customer-success-voice-signal-hackathon/  
- Set the GitHub repo **Homepage** field to that URL (not the old Vercel 404)

## How judges run this

```bash
git clone https://github.com/assafbar2/customer-success-voice-signal-hackathon.git
cd customer-success-voice-signal-hackathon/skills/customer-success-voice-signal
npm install
npm test && npm run typecheck

# Dress rehearsal — default, no ring, no CALL-E key
npm run signal -- --fixture stuck_support_acme.json
npm run signal -- --stdin < events/sample_stuck_support.json
npm run signal -- --list

# Curtain-up — operator only
# https://dashboard.heycall-e.com/account/api-keys
# cp .env.example .env → CALLE_API_KEY, CS_OWNER_E164, SIGNAL_CONFIRM=PLACES
# npm run signal -- --fixture stuck_support_acme.json --live PLACES
```

| Exit | Meaning |
| --- | --- |
| 0 | Ok |
| 2 | HOLD (policy / live gate / house dark / owner budget) |
| 3 | Failure |

**Safety:** CS owner only · dress rehearsal default · per-owner call budget · house dark timezone-aware · HOLD never poisons cue dedupe · fixture phones never dialed live.

Live ladder (including voicemail / unclear): [`research/calle-api-notes.md`](research/calle-api-notes.md) · redacted rows: [`submission/evidence/`](submission/evidence/)

## Docs map

| Path | Purpose |
| --- | --- |
| [skills/customer-success-voice-signal/](skills/customer-success-voice-signal/) | **Stage Manager skill** |
| [docs/02-prd.md](docs/02-prd.md) | Product decisions |
| [docs/03-architecture-flow.md](docs/03-architecture-flow.md) | As-built flow |
| [submission/awesome-list/PACKAGING.md](submission/awesome-list/PACKAGING.md) | Awesome-list PR packaging |
| [notes/STATUS.md](notes/STATUS.md) | Operator status (not a pitch deck) |
| [LICENSE](LICENSE) | MIT |

## Official links

- Devpost: https://call-e.devpost.com/  
- Rules: https://call-e.devpost.com/rules  
- **CALL-E API keys:** https://dashboard.heycall-e.com/account/api-keys  
- **Submit list PR:** https://github.com/CALLE-AI/awesome-phone-call-agents  
- Extra calls form: https://forms.gle/EPQttEZ1rkW8iq9q6  

## Submit checklist

- [x] Skill + dress rehearsal + curtain-up path  
- [x] Judge site on GitHub Pages  
- [ ] Awesome-list PR (see packaging notes) + Devpost  
- [ ] Demo video with real call audio (tracked separately)  

## Judging criteria (Devpost)

1. Real World Impact  
2. Quality of the Idea  
3. Technical Implementation (CALL-E at runtime)  
4. Product Experience & Demo (≤3 min video)

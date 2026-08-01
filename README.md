# customer-success-voice-signal-hackathon

**Product:** [`customer-success-voice-signal`](docs/02-prd.md)  
**Hackathon:** [CALL-E: Your Code Is Calling](https://call-e.devpost.com/)  
**Deadline:** 2026-09-14  
**Status:** Registered · PRD locked · private GitHub  

> *The only CS notification that can’t hide under Slack.*

## Goal

Win **Most Practical Use Case** ($4,000) if possible; stay competitive for Innovative / Honorable; always submit **Most Valuable Feedback** survey.

## Docs map

| Path | Purpose |
| --- | --- |
| [docs/02-prd.md](docs/02-prd.md) | Product requirements |
| [docs/03-architecture-flow.md](docs/03-architecture-flow.md) | **One-view flow, entities, functions** |
| [docs/04-stack-hosting-tone.md](docs/04-stack-hosting-tone.md) | **Stack, free hosting, funny tone** |
| [docs/01-ideas-1-2-5.md](docs/01-ideas-1-2-5.md) | Earlier idea exploration |
| `notes/` | Status log |
| `skills/` | (next) skill implementation |
| `submission/` | Devpost / video / PR checklist |

## Official links

- Devpost: https://call-e.devpost.com/
- Rules: https://call-e.devpost.com/rules
- Setup / integrations: https://github.com/CALLE-AI/call-e-integrations
- **Submit PR here:** https://github.com/CALLE-AI/awesome-phone-call-agents
- Extra calls form: https://forms.gle/EPQttEZ1rkW8iq9q6
- Feedback survey (MVF prize): via Devpost details

## Product (locked)

### `customer-success-voice-signal`

When a named account hits a high-risk moment, CALL-E **calls the CS owner** (not the customer) with a short brief and decision options; structured result is written back.

See [docs/02-prd.md](docs/02-prd.md). Background: [docs/01-ideas-1-2-5.md](docs/01-ideas-1-2-5.md).

| MVP | Choice |
| --- | --- |
| Name / skill id | `customer-success-voice-signal` |
| Callee | CS only |
| Triggers | stuck support · SLA · agent needs decision · health/onboarding |
| Branding | Sentry-shaped, not branded |
| PR target | `skills/customer-success-voice-signal/` |

## Next actions

- [ ] Request extra CALL-E calls  
- [ ] Install CALL-E CLI + auth (`calle auth login`)  
- [ ] Scaffold `skills/customer-success-voice-signal/` under this repo  
- [ ] Dry-run first call path  

## Judging (equal weight)

1. Real World Impact  
2. Quality of the Idea  
3. Technical Implementation (CALL-E at runtime)  
4. Product Experience & Demo (≤3 min video)

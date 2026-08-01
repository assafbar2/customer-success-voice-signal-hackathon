# customer-success-voice-signal-hackathon

**Product:** [`customer-success-voice-signal`](docs/02-prd.md) · **Persona:** Stage Manager  
**Hackathon:** [CALL-E: Your Code Is Calling](https://call-e.devpost.com/)  
**Deadline:** 2026-09-14  
**Status:** Registered · PRD locked · skill scaffolded · private GitHub  

> *When the account is on fire, we cue the firefighter — not the building.*

## Goal

Win **Most Practical Use Case** ($4,000) if possible; stay competitive for Innovative / Honorable; always submit **Most Valuable Feedback** survey.

## Docs map

| Path | Purpose |
| --- | --- |
| [docs/02-prd.md](docs/02-prd.md) | Product requirements |
| [docs/03-architecture-flow.md](docs/03-architecture-flow.md) | **One-view flow, entities, functions** |
| [docs/04-stack-hosting-tone.md](docs/04-stack-hosting-tone.md) | **Stack, free hosting, Stage Manager tone** |
| [docs/05-dev-design-plan.md](docs/05-dev-design-plan.md) | Skill phases + runbook |
| [docs/01-ideas-1-2-5.md](docs/01-ideas-1-2-5.md) | Earlier idea exploration |
| [notes/STATUS.md](notes/STATUS.md) | Status log |
| [skills/customer-success-voice-signal/](skills/customer-success-voice-signal/) | **Stage Manager skill** |
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

When a named account hits a high-risk **cue**, the **Stage Manager** rings the **CS owner** (not the customer) with a short brief and line readings; structured result goes to the **prompt book** / **show report**.

See [docs/02-prd.md](docs/02-prd.md). Background: [docs/01-ideas-1-2-5.md](docs/01-ideas-1-2-5.md).

| MVP | Choice |
| --- | --- |
| Name / skill id | `customer-success-voice-signal` |
| Persona | Stage Manager |
| Callee | CS only |
| Triggers | stuck support · SLA · agent needs decision · health/onboarding |
| Branding | Sentry-shaped, not branded |
| Default mode | Dress rehearsal (no ring) |
| Live gate | `--live` + type/env `PLACES` |
| PR target | `skills/customer-success-voice-signal/` |

## Next actions

- [ ] Request extra CALL-E calls  
- [ ] Curtain-up one live cue for demo video  
- [ ] Package / PR to awesome-phone-call-agents  
- [x] Scaffold `skills/customer-success-voice-signal/`  
- [x] Dress rehearsal path green  

## Judging (equal weight)

1. Real World Impact  
2. Quality of the Idea  
3. Technical Implementation (CALL-E at runtime)  
4. Product Experience & Demo (≤3 min video)

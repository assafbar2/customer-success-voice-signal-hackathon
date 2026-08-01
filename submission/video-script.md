# Demo video script — Stage Manager (≤3:00)

**Goal:** One chuckle, then clarity. Show the real job, the CLI, one live ring, writeback.  
**Primary cue:** `stuck_support` · **Name-drop:** `agent_needs_decision`

---

## Shot list + spoken lines

| Time | Shot | Spoken / on-screen |
| --- | --- | --- |
| **0:00–0:20** | Face or title card → terminal ready | **VO:** “Customer Success owns the account. Slack owns the noise. When Acme’s support path is stuck, we don’t dial the customer — we cue the firefighter.” *Beat / half-smile:* “Stage Manager. Headset on.” |
| **0:20–0:50** | Terminal: `cd skills/customer-success-voice-signal` → dress rehearsal | **VO:** “Dress rehearsal first. Default. No ring.” *Run:* `npm run signal -- --fixture stuck_support_acme.json` · Show call sheet preview + simulated line reading 1 · “Prompt book and show report update without touching a phone.” |
| **0:50–1:10** | Quick `--list` or second fixture flash | **VO:** “Four cues on the sheet — stuck support, SLA, agent needs a decision, health stall. Same engine.” *Optional flash:* `agent_needs_decision_acme.json` in `--list`. |
| **1:10–2:10** | Curtain-up CLI + phone rings + answer | **VO:** “Curtain up. Live gate: `--live` and `PLACES`.” *Run:* `npm run signal -- --fixture stuck_support_acme.json --live PLACES` · Cut to phone ringing · **On call (Stage Manager):** “Hi Maya. Stage Manager. You're up for Acme.” · Brief (ticket stuck, two bot handoffs) · “Line reading. Press or say 1, 2, or 3.” · Maya: “One.” · “Confirming option 1 — take over in chat. Logging to the prompt book. Clear.” |
| **2:10–2:35** | Terminal + `data/show-report.md` / prompt book | **VO:** “Decision one — take over in chat. Written to the prompt book and show report. Structured. Auditable. No CRM cosplay.” |
| **2:35–2:50** | Name-drop second cue (fixture or one line of `--list`) | **VO:** “Same path for when an agent hits needs-human — closed-set approve A, B, or escalate. We don’t freestyle policy on a cold call.” |
| **2:50–3:00** | Tagline card | **VO:** “When the account is on fire, we cue the firefighter — not the building. Stage Manager. CALL-E.” · End card: repo + skill path. |

**Hard stop at 3:00.** Prefer landing at ~2:50.

---

## Stage Manager call beat (record this take clean)

```text
Hi Maya. Stage Manager. You're up for Acme.

Sorry for the interrupt — Ticket 4821 is looping. Two bot handoffs, still open,
enterprise account. You're on the call sheet.

Line reading. Press or say 1, 2, or 3.
1: Take over in chat now.
2: Assign to SE.
3: Not now — snooze two hours.

[Maya: One.]

Confirming option 1 — take over in chat now. Logging to the prompt book.
Clear. Break a leg — or just open the ticket.
```

One chuckle max in the open (or in the VO before the ring). Then business.

---

## B-roll / screen checklist

- [ ] Terminal font large enough for 1080p crop  
- [ ] Dress rehearsal output: persona, cue, line readings, “no ring”  
- [ ] Curtain-up command visible (`--live PLACES`) — **no secrets on screen** (mask `.env`, blur phone if needed)  
- [ ] Phone UI: incoming call + answer (or screen-record handset)  
- [ ] Show report / prompt book snippet with `stuck_support` + decision 1  
- [ ] Fixtures list or `agent_needs_decision` name-drop (~2s)  
- [ ] End card: `skills/customer-success-voice-signal/` + hackathon repo URL  

## Do not show

- API keys, full E.164, `.env` contents  
- Fake “dashboard” UI (none shipped)  
- Pitch-deck slides or prize-chasing language  
- Long phase calendars or architecture essays  

## Recording notes

- Capture dress rehearsal offline first (reliable cut).  
- Curtain-up: one clean answered take; keep a dress-rehearsal fallback cut if the live ring flakes.  
- Mic: VO can be post; live call audio from the handset is the hero beat.  

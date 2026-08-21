# Demo video script — Stage Manager (≤3:00)

**Status:** Agent-recorded reel shipped (`submission/demo-reel/stage-manager-demo.mp4`, ~65s). TTS VO. Call beat from 2026-08-12 live transcript. CLI is a real screen recording.  
**Problem framing:** Customer Success and other customer-facing teams.

**Goal:** Problem → why phone → product → dress rehearsal → live decision → writeback → business value → end.  
**Tone:** Stage Manager. One light beat, then clarity.  
**Primary cue on screen:** `stuck_support` · **Second cue:** `agent_needs_decision` (name-drop or flash)

---

## Problem statement (must land early)

Customer Success and other customer-facing teams own named accounts and renewals, but the signal that matters is buried under Slack, ticket queues, and dashboards. When support loops, SLA turns red, an agent hits `needs_human`, or onboarding stalls, the “notification” is easy to miss — until churn or breach is already expensive.

**Phone is the interrupt that still works** — but only if it is rare, short, structured, and aimed at the **CS owner**, not a spam dialer to the customer.

## Business value (say plainly)


| Value               | One line for VO / card                                                        |
| ------------------- | ----------------------------------------------------------------------------- |
| **Right person**    | Interrupt the owner, not the account.                                         |
| **Faster decision** | Closed-set 1 / 2 / 3 in ~60s instead of thread archaeology.                   |
| **Audit trail**     | Decision lands in prompt book / show report — not lost in chat.               |
| **Safe by default** | Dress rehearsal first; live needs explicit `PLACES`; never call the customer. |
| **One engine**      | Four cue types, same pipeline — practical Monday-morning CS ops.              |


Prize narrative we aim at: **Most Practical** (primary) · also submit **Most Valuable Feedback** (separate survey — [`mvf-feedback.md`](mvf-feedback.md)).

Pre-submit (video + GIF + awesome-list + MVF): [`PRE-SUBMIT.md`](PRE-SUBMIT.md).

---



## Shot list + spoken lines


| Time          | Shot                                                 | Spoken / on-screen                                                                                                                                                                                                                                          |
| ------------- | ---------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **0:00–0:25** | Title: **Stage Manager** · dark stage / spotlight    | **VO — problem:** “Customer Success owns the revenue relationship. Slack owns the noise. When a named account is stuck — looping support, red SLA, agent blocked, health going quiet — the alert hides under everything else.”                              |
| **0:25–0:40** | Tagline card                                         | **VO — value:** “Phone still cuts through. We don’t dial the customer. We cue the firefighter.” *Beat:* “Stage Manager. Headset on.” **On screen:** *Places, please — your account is on.*                                                                  |
| **0:40–1:05** | Terminal dress rehearsal                             | **VO:** “Dress rehearsal first — default, no ring, no keys required for judges.” *Run:* `npm run signal -- --fixture stuck_support_acme.json` · Show call sheet + line readings 1/2/3 · “Preview the cue. Update the prompt book without touching a phone.” |
| **1:05–1:20** | `--list` / four cues                                 | **VO:** “Four cues, one engine: stuck support, SLA risk, agent needs a decision, health or onboarding stall.”                                                                                                                                               |
| **1:20–2:15** | Curtain-up + call beat (live take or recreated beat) | **VO:** “Curtain up. Live gate: `--live` and `PLACES`.” · **On call:** “Hi Maya. Stage Manager. You’re up for Acme.” · Brief · “Line reading — one, two, or three.” · Maya: “One.” · “Take over in chat. Logging to the prompt book. Clear.”                |
| **2:15–2:35** | Show report / prompt book                            | **VO — value:** “Decision one — take over in chat. Structured writeback. Auditable. The kind of trail you can hand a manager, not another Slack shrug.”                                                                                                     |
| **2:35–2:50** | Second cue flash                                     | **VO:** “Same path when an agent hits needs-human — approve A, B, or escalate. We ran that live too.”                                                                                                                                                       |
| **2:50–3:00** | End card: repo + skill path                          | **VO:** “When the account is on fire, we cue the firefighter — not the building. Stage Manager. CALL-E.” **On screen (small):** repo URL · `skills/customer-success-voice-signal/` · *No customers were called in the making of this demo.* |


**Hard stop ≤3:00.** Prefer ~2:50.

---



## On-screen business-value beats (optional lower-thirds)

Use 1–2 max so it doesn’t feel like a pitch deck:

1. `CS owner only · never the customer`
2. `Dress rehearsal default · live needs PLACES`
3. `Decision → prompt book`

---



## Stage Manager call beat (clean take)

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

---



## B-roll checklist

- [ ] Terminal font large enough for 1080p  
- [ ] Dress rehearsal: persona, cue, line readings, “no ring”  
- [ ] Curtain-up command (`--live PLACES`) — **no secrets**  
- [ ] Stage code identity beat (or dress-rehearsal note of the code)  
- [ ] Writeback with `stuck_support` → decision 1  
- [ ] Adapter beat: `apply-action --dry-run` only (Slack/GitHub live send is out of scope — do not fire)  
- [ ] `agent_needs_decision` name-drop  
- [ ] End card: `skills/customer-success-voice-signal/` + repo URL  
- [ ] **Pre-submit (same day as upload):** MVF survey filled from [`mvf-feedback.md`](mvf-feedback.md) — see [`PRE-SUBMIT.md`](PRE-SUBMIT.md)



## Do not show

- API keys, full E.164, `.env`  
- Fake product dashboard  
- Prize-chasing / “please give us Most Practical” language  
- Reading the MVF survey on camera (submit it on Devpost; don’t pitch it in the reel)



## Review notes to consider before shooting (2026-08-03)

Ideas from repo review — take or leave per beat:

1. **Cold open with the ring.** Instead of 25s of problem VO first, open on the actual
   phone call: ring → "Hi Maya. Stage Manager. You're up for Acme." (~8s), hard cut to
   black: *"That call happened because a support ticket looped twice."* Then the problem
   statement. Real ring audio in the first 10 seconds is the single most convincing asset
   we own — don't bury it at 1:20.
2. **Keep the closer.** "Break a leg — or just open the ticket." is the best line in the
   repo. It stays.
3. **End card joke** (doubles as the safety differentiator):
   *"No customers were called in the making of this demo."*
4. **No Slack land.** Slack/GitHub adapters are a stab to show the handoff is possible.
   Video writeback is the prompt book. Do not fire a real channel.
5. Metaphor rationing on screen: pair theater terms with plain speech on first use
   ("dress rehearsal — dry-run", "curtain up — live call"). VO can stay theatrical.
6. **Identity beat.** Stage code read-back before “one” — shows the decision is bound to
   the call-sheet owner, not whoever picks up.
7. **MVF is not a video beat** — it’s a Devpost survey filled the same day you upload the
   video. Draft: [`mvf-feedback.md`](mvf-feedback.md). Gate: [`PRE-SUBMIT.md`](PRE-SUBMIT.md).

## Approval

Reply with **approve** (or edit notes). After approval we will:

1. Rebuild the mp4 **with a real audio track** (TTS or your VO files).
2. Keep ≤3:00 and match this script’s problem + value beats.
3. Tick video + MVF together on [`PRE-SUBMIT.md`](PRE-SUBMIT.md).


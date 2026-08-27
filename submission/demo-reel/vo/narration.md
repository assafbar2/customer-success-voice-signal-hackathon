# Human VO — paste this into another model

Use this if the agent reel’s neural TTS is still too synthetic. One narrator for 1–3 and 5. Two additional voices for the call (Stage Manager vs owner).

**Direction:** conversational, unhurried, slightly dry. Pause after “That is the problem.” Smile on “Break a leg — or just open the ticket.” Do not punch every period like a trailer.

**Suggested ElevenLabs:** a mid-Atlantic / US documentary male, stability ~0.55, similarity ~0.75, style exaggeration off, speaker boost on. Rate: slightly under conversational.

Save outputs as:

```text
submission/demo-reel/human-vo/01_problem.wav
submission/demo-reel/human-vo/02_insight.wav
submission/demo-reel/human-vo/03_cli.wav
submission/demo-reel/human-vo/04a_host.wav
submission/demo-reel/human-vo/04b_sm.wav      # Stage Manager lines, concatenated in order, 400ms gaps
submission/demo-reel/human-vo/04c_owner.wav   # both owner lines, 400ms gaps — or cut into the timeline by hand
submission/demo-reel/human-vo/05_close.wav
```

Then: `VO_DIR=human-vo bash submission/demo-reel/build.sh`

If you record one continuous take, name it `full.wav` and we can cut to picture later. Prefer the per-beat files.

---

## 01_problem

Every company pages an engineer when a server goes down. Almost nobody pages the human who owns the renewal when the account goes quiet.

Customer Success owns the revenue relationship. Slack owns the noise. When a named account is looping in support — two bot handoffs, ticket still open, enterprise on the line — the alert is just another message in a river of messages. Until churn is already expensive.

That is the problem.

## 02_insight

Phone still cuts through. Not as a spam dialer to the customer. As a sixty-second interrupt for the C S owner. Rare. Short. Structured. One, two, or three. Then hang up.

This is Stage Manager.

## 03_cli

Judges run the whole loop with no A P I key. Dress rehearsal is the default: same call sheet, same line readings, same prompt book — no ring. Four cues, one engine: stuck support, S L A risk, agent needs a human, health or onboarding stall.

## 04a_host

When we took it live, Call E rang the C S owner only. Never the customer.

## 04b_sm (Stage Manager)

Hi. Stage Manager. You are up for Acme. Stage code — please repeat: four eight two one.

Line reading. Say one, two, or three. One: take over in chat now.

Logging takeover in the prompt book. Clear. Break a leg — or just open the ticket.

## 04c_owner

Four eight two one.

One.

## 05_close

That decision is state. Not a Slack shrug. An action intent for the next system. Ack is not a decision. This is.

When the account is on fire, we cue the firefighter — not the building. Stage Manager. No customers were called in the making of this demo.

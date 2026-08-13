# How 2,000 Sentrants come alive

Name is **Sentrants**. One of them is a **sentrant**. You still run the place.

They are not 2,000 ChatGPT tabs. They are not a spreadsheet that wiggles. They hatch as a swarm, then they keep living.

---

## Hatch — one night, all 2,000 at once

### 1. Sample people who could exist

The census is the mix. Do **not** roll each field independently — that’s how you get a 23-year-old staff founder on Enterprise self-hosted Unity in LatAm with `seer.auto` on. Margins look right. Nobody looks real.

Hatch with **rejection sampling + a few hard no’s**:

| No | Why |
| --- | --- |
| age 23 + staff / boss | Not yet. |
| age 55 + junior + bootcamp | Almost never. |
| founder + shop: corporate | That’s a boss. |
| founder + junior | Founders aren’t juniors. |
| `trying` + tenure 6 years | They would be `in` or `gone`. |
| `trying` + enterprise + five signals | They’re not trying. |
| `gone` with empty memory | They left for a reason. Give them one. |
| `seer.mcp` + hobby + developer + tenure 0 | Slow down. |
| `replay.web` + geo india + shop corporate | Rare. PII. Don’t make it common. |
| self_hosted + plan developer | That’s not how that works. |

Plus **segment priors** (not independent dice):

- Corporate India: more `coder`, more Spring/Java, more `business`, less Replay, `seer.mcp` if they’re in Cursor.
- 23 / bootcamp / coder: Next/React, `trying` or fresh `in`, `errors` only, loud, price-sensitive.
- 55 / Rails / boss: `in`, spans + PagerDuty + releases, pinned SDK, low change-appetite.
- Founder 30 / startup: Team plan, near quota, will try Seer, will scream at Price.

Keep drawing until 2,000 pass. A 2% slice still has dozens of people. That’s the point of 2,000.

Each sentrant also gets a **portfolio that matches the life**, not a random subset of [portfolio.md](./schema/portfolio.md):

- `trying` → `errors`, maybe nothing else  
- `in` + paying → errors + some of spans / alerts / releases  
- Seer pieces only if they’re `in`, mostly coders, not the whole swarm overnight  

### 2. Name them (no model)

Name lists by `geo`. Priya, Matt, Łukasz, Radhika, Diego. Fictional. Never a real customer. Unique enough on the floor.

### 3. Give them a grain of voice (still no model)

Compile a short `voice` from what they already are. This is the trick that makes click-to-talk work on night one **without** 2,000 LLM calls:

```text
You are Radhika, 30, coder, corporate India, Spring.
Plan: business. Using: errors, spans, seer.mcp.
Stage: in. Loud, low change-appetite, price-ok, hates noise.
Speak short. Mix in process. You review other people's PRs. You did not ask for Autofix to open them.
```

Every sentrant has this card at hatch. The model, when we finally call it, *plays* the card. It does not invent who they are.

### 4. One origin line

A sentence of how they got here. Templates with slots is enough to hatch:

> “Stuck Sentry on a Next app the week after bootcamp because Vercel was 500ing and Twitter said so.”

Optional polish: batch-rewrite origins with an LLM *once* so they don’t all sound like the same mad-lib. That’s a hatch-night job, not a runtime job. Skip it if the templates are good.

### 5. Drop them on the floor

2,000 dots, already in **trying / in / pissed / gone**. They fidget. The mix is visible without clicking. **This is the moment they are alive.** You have an audience. You have not opened 2,000 sockets.

Save file: SQLite. Close the laptop, they’re still there in the morning.

---

## They stay alive

| Beat | What happens | Model? |
| --- | --- | --- |
| **Breathe** | 2,000 particles on a canvas. Idle wander inside their camp. Always. | No |
| **Murmur** | Ticker from physics: someone near quota, someone turned on Logs, someone walked to pissed. Many at once. | No |
| **Jump** | “A month later.” All 2,000: renewal, quota, trying→in, pissed→gone or back to in, maybe they pick up `seer.mcp` if it exists and they would. | No |
| **Move** | You ship / price / break / … a portfolio id. **All 2,000 who feel it walk.** | No |
| **The room talks** | After the walk: many one-liners, sampled across camps × slices. One batched call. Cache on the person. | Yes, once per move |
| **Walk up to one** | Their card + origin + memory → a person. The chat writes memory. Next time they’re not a stranger. | Yes, that one |

No night watch. No twelve. The swarm is the unit. Mouths are lazy: we pay for language when the room just moved, or when you look someone in the eye.

If you stare at the floor and nobody has spoken yet, they are still alive. Ants don’t narrate. They move.

---

## Rewrite is also a hatch

“15% not 17%” = hatch the missing crowd, or retire a crowd to `gone`. New sentrants go through the same night (name, voice grain, origin). You don’t possess a living SaaS person and declare them self-hosted.

---

## First thing we actually run

1. Hatch 2,000 into SQLite. Print: counts by geo × shop × stage. If corporate India isn’t a *region*, the hatch is wrong.  
2. Canvas: 2,000 dots in four camps, fidgeting. Color-by geo. You should see India. You should see 23 vs 55.  
3. Click one: the card (no chat yet). If it reads like a person, hatch worked.  
4. Then chat. Then a move. Then Jump.

If step 2 doesn’t look like Sentry’s people, don’t touch a model. Fix the hatch.

# The House — design brief (review before build)

**Status:** proposal. Not a PRD. Not an implementation plan.  
**Correction:** the swarm is not a survey panel. It is a **living crowd of Sentry customers**. Polls, emails, launches, and breaking changes are things that happen *to them*. They keep living afterward.  
**Company:** Sentry.  
**Sibling:** Stage Manager ([`02-prd.md`](./02-prd.md)) is the phone interrupt when a *named* account is already on fire. The House is the installed base that account came from.

---

## The primitive

**There is a swarm of Sentry customers.**

They are live. Each one is a customer-chatbot with a body: identity, personality, a relationship to Sentry, a memory, and a trajectory. They do not reset when you close the tab.

Later — and the architecture assumes this from day one — they grow. They instrument a second SDK. They buy Performance. They hit quota. They upgrade. They ignore Seer. They open a ticket. They churn. Personality is the bias on all of that, not a bio pasted into a prompt.

Everything else in the original ask is an *operation on that swarm*:

```text
THE SWARM  (persistent customers — the product)
    │
    ├── time ticks     →  usage, noise, renewals, organic adopt / expand / churn
    │
    └── a Sentry role does something
            ├── probe     ask; don't write to their life
            ├── touch     they experience it (poll, email, in-app)
            ├── ship      feature / break / policy / price lands in their world
            └── god-mode  rewrite the mix (“15% not 17%”)
                    │
                    ▼
          lives update  →  the floor walks  →  prompt book
```

The poll is a scene. **The simulation is the product.**

---

## One-liner

> The House is a living installed base: a crowd of Sentry customer agents who remember what we did to them and keep going — adopting, expanding, stalling, churning. Every role can poll them and can change their lives. The spectrogram is how you watch them move.

---

## What “live” means (and does not)

**Live means persistent beings**, not a fresh cast per question.

Each member of the House has:

| Layer | What it is |
| --- | --- |
| **Identity** | Sentry-shaped facts: plan, deployment, SDKs, product surface, quota posture, role, region |
| **Personality** | Stable reaction function: noise tolerance, price sensitivity, change appetite (pin vs adopt), trust in Sentry, vocality, loyalty vs wandering |
| **Life** | Current relationship: products in use, usage, health, sentiment, contract clock, ticket load |
| **Memory** | What already happened to *them*: the quota email, the Python break, the Seer launch they ignored |
| **Trajectory** | Expanding / stable / noisy / at-risk / churning — and, later, actually churned |

**Live does not mean** 10,000 LLM sockets left open. They are always alive *as state*. They *think* when the clock ticks or when someone touches them. Same as any simulation: the Sims are not fully rendered when you’re in another room. If we confuse “alive” with “always chatting,” we will build a cost bomb and call it a world.

**Two clocks, both real:**

1. **World clock** — time passes. Quotas get hit. Renewals arrive. Noise accumulates. People adopt or don’t. The mix changes *because they lived*.  
2. **Operator clock** — someone at Sentry polls or ships. The House reacts *now*, remembers it, and the next tick starts from the new lives.

---

## Every role uses the same House

Not a CS toy. Not a Product toy. A shared world.

| Role | Polls to learn | Touches / ships to change |
| --- | --- | --- |
| Product | Will you adopt this? What’s missing? | Launch it into their lives; watch who actually turns it on over ticks |
| Eng | Does this break you? | Ship the SDK/API change to the affected platforms |
| CS | How does this email / policy land? | Send it; watch tickets, TAM pings, churn risk |
| Marketing | Does this campaign move anyone? | Run it |
| Pricing | Who pays, who stalls, who leaves? | Change the menu |
| Support | Does this deflection help or enrage? | Change the queue |
| Leadership | How is the base, really? | All of the above |

A poll can **impact behaviour**. In real life, “we’re thinking of deprecating X” is already a touch. So every operator action is typed:

| Verb | Writes to their life? |
| --- | --- |
| **Probe** | No. Lab question. Counterfactual. |
| **Touch** | Yes. They received this (survey, email, in-app, TAM rumour). |
| **Ship** | Yes. The product/policy/price is now in their world. |
| **God-mode** | Yes, but *you* rewrote reality (recalibrate the mix to match real Sentry, or run a counterfactual population). |

Without that distinction, every “just asking” permanently scars the base, and you cannot try two email drafts.

---

## Trunk and branch (how a living world stays usable)

One House that remembers everything, plus forks:

```text
trunk   = the canonical living House (history accumulates)
branch  = fork, try the email / the break / the price, watch them walk
commit  = merge the branch into trunk  (“curtain-up” inside the sim)
abandon = throw the branch away       (“dress rehearsal”)
```

- **Dress rehearsal** = branch. The crowd still *lives on the branch*. They grow and churn in that universe. Trunk is unharmed.  
- **Curtain-up (sim)** = commit to trunk. This is still not a real customer email. It means “this is now what happened to our digital base.”  
- **God-mode on trunk** = we looked at real Sentry and the House had drifted; we retune (15% → 17%) and record the rewrite.

This is how “they continue living” and “we still get to try things” coexist.

---

## How the mix changes

Two different operations. Do not collapse them.

**God-mode (census).** An operator says the House is wrong against reality, or wants a counterfactual: self-hosted is 12% of orgs, not 8%. That is a versioned, diffable rewrite. “15% not 17%” is a census commit. You name the **denominator** (orgs / ARR / event volume / vocality) or the number is meaningless.

**Life.** Nobody dragged a slider. Team-plan ants hit quota, some upgraded to Business, some churned. The live mix moved because they lived. Personality biases who does which.

Census is the **initial conditions** and the **recalibration lever**. Life is the **simulation**. If we regenerate disposable ants from a recipe every poll, there is no one left to grow.

The Cabinet is not a second population. It is **named members of the same swarm** you can follow across years of sim time — Lars the self-hosted platform lead, the near-quota Next.js shop, the TAM’d security reviewer. Same physics. Higher fidelity. Quotable.

---

## What you do to them (typed stimuli)

The original ask listed customer attributes and under-specified the question. At Sentry the **stimulus type chooses who feels it**. Asking mobile-only orgs about a Python SDK break and calling that “the customer base” is a lie.

| Type | Hits this layer | Example |
| --- | --- | --- |
| Breaking change | Project / SDK owners on the affected platforms | Python SDK init deprecation |
| Mass comms | Who would actually receive it | Quota / spike-protection email |
| Feature launch | Orgs that could adopt it — including those who will ignore it | Seer, Logs, Size Analysis |
| Policy | Security, self-hosted, residency-sensitive | AI training, retention, FSL |
| Pricing | Billing admins + economic buyers | PAYG, reserved volume, plan gates |
| Support policy | Whoever files issues + whoever owns the TAM relationship | SLA, chatbot deflection |

A stimulus is not a prompt. It is an object: the artifact, who it reaches, the **stations** they may walk to, and whether it is probe / touch / ship.

Stations are closed-set and scenario-specific — the same discipline as Stage Manager’s line readings. Not yes/no. After they walk, you read quotes. The walk *is* the vote.

---

## The floor (how the crowd looks)

Same ants. Different floors. Motion is the demo.

**Poll floor** — you ask; they walk to stations. You change the copy; they walk again.

Python deprecation email, 90-day window, no codemod:

1. Upgrade this sprint  
2. Pin and wait for a guide  
3. This breaks CI / many services — angry  
4. Not my platform — sit out  
5. Ping TAM / legal  
6. Evaluate leaving  

Enterprise Python + pinned SDKs pile into 2 and 3. JS-only should be filtered off this floor. Vocality-weight makes 3 look bigger than ARR-weight. Lars walks to 3 and says the quote you will actually hear.

Change to 12-month window + a codemod: particles flow. 3 shrinks toward 2, some of 2 toward 1. Lars moves to 2, not 1. ARR looks fine. Vocality still has a public-thread risk. **That split is the product.**

**Life floor** — nobody asked a question. Time passed. The same ants have drifted toward expanding / healthy / noisy / at-risk / churned. Color by plan, SDK, or role. This is how you *see* buying more Sentry, and leaving.

Click an ant → the person: identity, personality, life, last memories, why they walked. You can talk to them (they are chatbots). Talking is a **touch** unless you mark it probe.

God-mode slider: drag “self-hosted 8% → 12%.” That is a rewrite, not a walk. Optionally morph the crowd so the floor matches the new census.

Avoid cute ant-farm if it reads as a toy. Audience / house lights / spectrogram — operational, Sentry-serious.

---

## Sentry-shaped lives (preview, not the bible)

Do not start from geography and “are they a developer.” Start from what changes a Sentry life.

- **Commercial:** Developer / Team / Business / Enterprise · self-serve vs TAM’d · SaaS vs self-hosted vs dedicated · tenure · renewal clock · quota posture (headroom / near-limit / recently spiked) · competitive frame (Sentry-only vs Datadog/New Relic/self-rolled)  
- **Runtime:** primary SDKs · pinned vs current · Errors / Performance / Replays / Profiling / Crons / Seer / Logs / Size Analysis · alert noise · residency  
- **Who is speaking:** instrumenting developer · on-call · eng manager / SRE · billing admin · PM · security · OSS maintainer on free  
- **Modifiers:** company size, industry, region, language — not the identity  
- **Personality:** noise tolerance, price sensitivity, change appetite, trust, vocality, loyalty  

A German PM and a German on-call engineer will split on the same email. Expertise is SDK + surface + quota, not years-of-experience. Geography is comms and residency.

The attribute bible is question 2, after this spine locks.

---

## How the House stays honest

A living sim will agree with you forever if we let it.

1. Stations are closed-set and typed.  
2. Stimuli only hit who would really see them.  
3. Weights are visible — never one % as “customers think.”  
4. Named members may dissent from the swarm.  
5. **Calibration nights:** replay a past real event (quota email, SDK break, pricing page) and score the House against what CS actually heard. Drifted trunks get retuned in god-mode, with a scarlet letter on that commit.  
6. Probe vs touch vs ship is visible on every action.  
7. Fictionalize people. Sentry-shaped, not real names, not real event dumps, not TAM notes pasted into prompts.  
8. The House can **hurt you** — or it is theatre.

This is a digital twin for rehearsal and simulation. It does not replace research, CAB, or analytics. It does not email real customers. It is not a churn oracle with fake precision.

---

## Review locks

Mark agree / change. Questions 1–4 in the original ask are downstream.

| # | Lock | Proposed default |
| --- | --- | --- |
| L1 | **Job** | A **living swarm** of Sentry customer agents. Polling, comms, launches, breaks, pricing are operations on that swarm. They keep living. |
| L2 | **Name** | **The House** — the audience that lives between shows |
| L3 | **Populations** | One persistent swarm. Census = initial conditions + god-mode. Named members = featured ants in the *same* physics, not a disposable panel. |
| L4 | **Live** | Persistent state + memory + trajectory. Cognition on ticks and touches, not idle LLM sockets. |
| L5 | **Shared world** | Every Sentry role polls and acts on the same House. |
| L6 | **Trunk / branch** | Branch = dress rehearsal universe. Commit to trunk = sim curtain-up. God-mode retunes trunk against reality. |
| L7 | **Verbs** | Probe / touch / ship / god-mode. Polls may be touches. |
| L8 | **Stimuli are typed** | Breaking / comms / launch / policy / pricing / support-policy. Type chooses who feels it. |
| L9 | **Stations** | Closed-set, scenario-specific. Not yes/no by default. |
| L10 | **Mix** | God-mode census diffs *and* endogenous life. Denominator required (org / ARR / volume / vocality). |
| L11 | **Dimensions** | Plan, deployment, SDK, product surface, quota posture, role, personality. Geo and “developer?” are modifiers. |
| L12 | **Honesty** | Wrong-audience filter, calibration, visible verbs, HOLD on real-world send. In v1. |
| L13 | **Stage Manager** | Sibling. No phone in House v1. |
| L14 | **v1 vs later** | v1: the swarm exists, you can talk to them, poll them, touch them, see them walk, god-mode the mix. World clock is real but coarse. Later: they buy, expand, churn as first-class life — same beings, richer ticks. **Do not build disposable v1.** |

---

## Open questions (only what changes the story)

1. Is the **trunk** a single company-wide House, or does each team fork by default and only CS/Product maintain a canonical trunk?  
2. v1 world clock: **coarse ticks** (weekly health drift) or a real **economy** (quota → paywall → upgrade/churn) from day one? Recommendation: coarse ticks in v1, economy as the first “later,” on the same agents.  
3. When any role can ship into the House, who is allowed to **commit to trunk**? (Otherwise Marketing’s campaign poisons Eng’s baseline.)  
4. How fictional must named members be for an internal Sentry tool vs a public demo?

---

## What we will answer after lock (not now)

1. **How we build it** — agent schema, clocks, verb pipeline, where LLMs sit, what is a state machine.  
2. **Attribute bible** — dimensions, personality, life fields; which are quotas vs tags; what Sentry could export later.  
3. **N, look, interaction** — how many live, how the floor works, talking to one ant vs watching the crowd.  
4. **Mass management** — census god-mode, watching life change the mix, spectrogram motion.

The starting point does not change: **there is a swarm of Sentry customers.** Then we build everything else on top of them still being there tomorrow.

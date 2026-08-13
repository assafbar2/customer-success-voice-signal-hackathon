# The House — design brief (review before build)

**Status:** proposal. Not a PRD. Not an implementation plan.  
**Audience:** Assaf — lock the story, then we answer “how / attributes / N / mass-management.”  
**Company:** Sentry (this is Sentry-shaped *and* Sentry-named; unlike Stage Manager, this brief does not hide the employer).  
**Related:** Stage Manager ([`02-prd.md`](./02-prd.md)) is the interrupt when a *named account* is already in trouble. This is the rehearsal *before* we put many accounts in trouble.

---

## 1. What you are actually trying to build

You are not trying to build “a lot of chatbots with demographics.”

You are trying to build a **preflight chamber for irreversible customer-facing decisions**.

The job:

> Before we change the show — a policy, a mass email, a feature launch, a breaking SDK, a quota or pricing move — we run it in front of a **sampled twin of Sentry’s installed base**. We watch who moves, where they move, and what they would actually *do*. We HOLD or we proceed. We can explain the HOLD with a segment, not a vibe.

That is closer to:

- a **dress rehearsal for the audience**, not a survey tool
- **dynamic sampling** for customers, not “N live agents always on”
- a **human spectrogram** (people walk to corners of the room), not a yes/no poll
- a **census you can retune** (15% not 17%), not a spreadsheet of 10,000 persona cards

The ants are the *instrument*. The product is the *decision to ship or HOLD*.

---

## 2. Why the first framing will fail if we ship it as stated

These are the traps in the original ask. If we don’t kill them now, we will build an expensive toy that agrees with us.

| Trap | What it looks like | Why it dies at Sentry |
| --- | --- | --- |
| **Demographic roleplay** | “Senior Python dev in Germany, 8 years experience” | Sentry customers do not react as *resumes*. They react as *quota tightness, SDK pin, plan, self-hosted vs SaaS, on-call noise, TAM relationship*. A German PM and a German on-call engineer will vote opposite ways on the same email. |
| **Always-on live agents** | Thousands of persistent LLM loops “being” customers | Cost, drift, and no operator affordance. The House should be **standing and idle**, then **cast** for a rehearsal. Persistence belongs to a small **Cabinet**, not the swarm. |
| **Person as the only unit** | One agent = one human | Sentry’s unit of pain is layered: **org** (plan, contract, residency) × **project/SDK** (what a breaking change hits) × **role** (who reads the email). A pricing note hits billing admins. A Python SDK break hits instrumenting engineers. Seer/AI policy hits security + legal. |
| **Binary yes/no floor** | Ants walk to Yes or No | Almost no Sentry decision is binary. Real stations are *upgrade this sprint / pin and wait / open a ticket / threaten churn / ignore because this isn’t my platform / post on HN*. |
| **Confirmation bias** | Prompted agents who sound like Product | Worthless unless the House can **hurt you**. The angry self-hosted admin, the hobbyist on Developer plan, the enterprise security reviewer, the org that already evaluated Datadog — those voices are the point. |
| **% without a denominator** | “Make type A 15% not 17%” | 15% of *orgs* ≠ 15% of *ARR* ≠ 15% of *event volume* ≠ 15% of *GitHub issue authors*. Self-hosted can be small in org-count and huge in vocality. The census must name the weight. |

---

## 3. The better story

**Working name: The House.**  
Theater: Stage Manager cues the CS owner. **The House is the audience.** Before curtain-up on a customer-facing change, we dim the lights and watch the House react.

**Sentry metaphor (do not bury this):** Sentry already refuses to store every event. It **samples** so the remaining set still represents the error population. The House is that idea pointed at *people and orgs*. We do not interview the installed base. We keep a **census**, we **sample**, we watch the **issue** (grouped reaction) instead of 10,000 identical paraphrases.

**One-liner**

> The House is a versioned, sampleable twin of Sentry’s installed base. You pose a stimulus. A cast of the House walks to reaction stations. You inspect who moved and why. You retune the mix in the census, not by poking ants. Dress rehearsal is the default; sending the email / shipping the break is curtain-up.

**Sequel to Stage Manager (optional, not v1)**

```text
The House rehearses a change  →  HOLD?  →  Stage Manager rings the CS owner
                                         →  prompt book records both
```

v1 does not need a phone. v1 needs an honest audience.

---

## 4. Product objects (the design)

Four objects. If we add a fifth too early, we will drown.

```text
┌─────────────┐     ┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Census    │────►│   Stimulus  │────►│    Sample    │────►│   Stations  │
│  the mix    │     │  the change │     │  the House   │     │  where they │
│  (versioned)│     │  (typed)    │     │  (cast now)  │     │  walk       │
└─────────────┘     └─────────────┘     └──────┬───────┘     └─────────────┘
                                               │
                                               ▼
                                        ┌─────────────┐
                                        │   Cabinet   │
                                        │  named      │
                                        │  voices     │
                                        └─────────────┘
```

### 4.1 Census — the mix you edit

A **recipe**, not a roster. Versioned. Diffable. “It’s 15% not 17%” is a census commit.

Independent dimensions (quotas that sum to 100% *per dimension*), plus a **weighting mode**:

| Weight | Question it answers |
| --- | --- |
| Org count | “What does the typical customer think?” |
| ARR | “What does revenue think?” |
| Event volume | “What does the installed runtime think?” |
| Vocality | “What will we *hear* on GitHub / support / HN?” |

Operators pick a weight **per rehearsal**. The same census, four different houses. That is how you stop arguing past each other in a launch review.

You do **not** edit 200 agents. You edit the recipe; the next cast is regenerated. Individual ants are disposable.

### 4.2 Cabinet — the named voices that persist

~12–24 high-fidelity seats, not 10,000.

These are the people CS already has in their head: the self-hosted platform lead who files SDK issues, the TAM’d enterprise security reviewer, the Next.js startup that lives on quotas, the mobile org that only cares about crashes, the billing admin who never opens the product.

The Cabinet:

- has memory across rehearsals (“last time you shortened the deprecation window I said we would pin”)
- is quotable in a launch review
- is **not** statistically representative — that is the Sample’s job
- can be seeded from real (redacted) CS notes / forum archetypes, then fictionalized

If the swarm is the spectrogram, the Cabinet is the people you call on after the room has walked.

### 4.3 Stimulus — what you are testing (this is half the product)

The original ask listed attributes of *customers* and under-specified the *question*. At Sentry the stimulus type **chooses who gets cast**.

| Type | Cast this layer | Example |
| --- | --- | --- |
| Breaking change | Project / SDK owners on the affected platforms | Python SDK init deprecation |
| Mass comms | Who would actually receive it (role + plan + locale) | Quota / spike-protection email |
| Feature launch | Orgs that could adopt it, including ones that will ignore it | Seer, Logs, Size Analysis |
| Policy | Security, legal-adjacent, self-hosted, residency-sensitive | AI training / data retention / FSL |
| Pricing / packaging | Billing admins + economic buyers, weighted by ARR | PAYG default, reserved volume, plan gate |
| Support policy | Whoever files issues + whoever owns the TAM relationship | SLA, chatbot deflection, office hours |

A stimulus is not a prompt. It is a **typed object**:

- the artifact (email draft, changelog, pricing table, ToS delta, migration window)
- the **audience filter** (who would see this in real life — do not ask mobile-only orgs about a Python SDK break and call it “the customer base”)
- the **stations** (closed set of reactions, scenario-specific)
- the **behavior we care about** (not just opinion): ignore / adopt / delay / open ticket / ping TAM / churn / go public

Closed-set stations are the same design move as Stage Manager’s line readings. Free-text comes *after* the walk, as quotes, not as the vote.

### 4.4 Sample — the ants

Cast **for a run**, from the census, filtered by the stimulus.

Suggested sizes (lock later; this is the shape):

| Layer | N | Job |
| --- | --- | --- |
| Visual swarm | ~80–200 | Readable motion. The ants. |
| Statistical read | ~300–800 | Percentages you can defend in a review (± a few points). |
| Featured quotes | ~8–16 | Click an ant, read a card. |
| Cabinet | ~12–24 | Persistent, named, remembered. |

**“Live”** means: the House *exists* as a census + cabinet, and a dashboard can look inhabited. It does **not** mean thousands of LLM sessions idling. Inference happens on rehearsal. Between rehearsals they are dots on a map, not conversations.

---

## 5. Sentry-shaped dimensions (preview, not the bible)

Do **not** start from geography and “are they a developer.” Start from what actually changes a Sentry customer’s vote.

**Commercial / relationship**

- Plan: Developer / Team / Business / Enterprise  
- Motion: self-serve vs sales-assisted vs TAM’d  
- Deployment: SaaS vs self-hosted vs dedicated  
- Tenure + renewal proximity  
- Quota posture: plenty of headroom / always near limit / recently spiked  
- Competitive frame: Sentry-only vs also Datadog/New Relic/self-rolled  

**Runtime (this is the Sentry-specific gold)**

- Primary platforms / SDKs (JS, Python, mobile, .NET, Go, Ruby, PHP, Unity, …)  
- SDK hygiene: current vs pinned / several major versions behind  
- Product surface in use: Errors, Performance/spans, Replays, Profiling, Crons, Uptime, Seer, Logs, Size Analysis  
- Alert load / noise sensitivity (the historical #1 wound)  
- Data residency (US / EU / elsewhere)  

**Who is speaking (role)**

- Instrumenting developer  
- On-call engineer  
- Eng manager / platform / SRE  
- Billing admin / procurement  
- Product manager (uses Sentry as “is this bug real”)  
- Security / compliance  
- Open-source maintainer on the free plan  

**Org context (use sparingly)**

- Company size, industry, region — as *modifiers*, not the identity  
- Language / timezone — for comms rehearsals only  

**Calibration traits (how the House stays honest)**

- Support density, GitHub/forum vocality, recent incident with Sentry, champion vs silent majority  

Geography is a **comms and residency** dimension, not a personality. Expertise is **SDK + product surface + quota posture**, not years-of-experience.

The full attribute list is question 2. We should not write it until this spine is locked.

---

## 6. How it should feel (the ants)

Reference image: a **four-corners / spectrogram**. You ask a question; the room walks. You change the question; they walk again. Most questions are not two corners.

**Scene — Python SDK deprecation email, v1 copy (90-day window, no codemod)**

Stations on the floor:

1. Upgrade this sprint  
2. Pin and wait for a migration guide  
3. This breaks our CI / we have many services — angry  
4. Not my platform — sit out  
5. Ping TAM / legal / procurement  
6. Evaluate leaving  

The House walks. Enterprise Python + pinned SDKs pile into 2 and 3. JS-only orgs sit at 4 (correct — they were filtered poorly if they dominate the shot). Self-hosted vocality-weight makes 3 look bigger than ARR-weight. Cabinet member “Lars, self-hosted platform, 40 services” walks to 3 and says the quote you will actually hear.

**You change one thing:** 12-month window + a codemod in the email.

Particles flow. 3 shrinks toward 2, then some of 2 toward 1. Lars moves to 2, not 1. The ARR-weighted House looks fine. The vocality-weighted House still has a public-thread risk. That split **is the product**.

Interaction, not a slide:

- Pose / revise stimulus (the copy is a first-class object; editing it re-runs the walk)  
- Toggle weight (org / ARR / volume / vocality) — same census, different gravity  
- Filter the floor (“only Business+, only mobile, only near-quota”)  
- Click an ant → persona card + quote + which station + confidence  
- Census slider: drag “self-hosted 8% → 12%” and the *next* walk uses the new mix (optionally animate a re-cast)  
- Prompt book: every rehearsal is an audit row (stimulus version, census version, weight, station mix, HOLD/proceed)

Graphic direction: particles with weak identity (color = dimension you are currently coloring by: plan, SDK, role). Stations are labeled regions, not bars. Motion on stimulus change is the demo. Avoid a literal ant farm if it reads as cute instead of operational — “audience” / “house lights” / “spectrogram” can carry the same motion with Sentry’s seriousness.

---

## 7. How we keep the House from lying

This is the hard product. Visualization is the easy one.

1. **Stations are closed-set and typed** — same discipline as line readings.  
2. **Filter by who would really see it** — a House that includes the wrong people is a lie.  
3. **Weighting modes are visible** — never show a single % as “customers think.”  
4. **Cabinet is allowed to dissent from the swarm.**  
5. **Calibration nights:** replay a past real event (a quota email, an SDK break, a pricing page change) and score the House against what CS actually heard. Census versions that fail calibration get a scarlet letter.  
6. **Dress rehearsal is the default.** The House never sends the email. HOLD is a first-class output.  
7. **Fictionalize the Cabinet.** Sentry-shaped, not real customer names, not real event dumps, not confidential TAM notes pasted into prompts.

If we cannot name how a rehearsal could prove us *wrong*, we should not build it.

---

## 8. What we are not building (v1)

- A replacement for user research, CAB, or analytics  
- A CSAT oracle or churn predictor with fake precision  
- Outbound to real customers  
- Always-on thousands of LLM agents  
- A generic “synthetic users” SaaS unmoored from Sentry’s runtime  
- Yes/no as the default station set  

---

## 9. Review locks — decide these, then we answer 1–4

Please mark agree / change on each. The numbered questions in the original ask are downstream of these.

| # | Lock | Proposed default |
| --- | --- | --- |
| L1 | **Job** is preflight for irreversible customer-facing decisions, not a chatbot zoo | Agree |
| L2 | **Name / metaphor** | **The House** + sampling (Sentry) + spectrogram (viz) |
| L3 | **Three populations** | Census (mix) + Sample (ants, disposable) + Cabinet (named, persistent) |
| L4 | **“Live”** means standing census + on-demand cast, not idle LLM sessions | Agree |
| L5 | **Stimulus is typed** and chooses who is cast | Breaking / comms / launch / policy / pricing / support-policy |
| L6 | **Stations are closed-set and scenario-specific** | Not yes/no by default |
| L7 | **Census edits are recipe diffs** with an explicit **weight** (org / ARR / volume / vocality) | “15% of *what*” is mandatory |
| L8 | **Sentry dimensions start from plan, deployment, SDK, product surface, quota posture, role** — geo and “are they a developer” are modifiers | Agree |
| L9 | **Honesty mechanics** (wrong-audience filter, calibration against past events, HOLD) are in v1, not a later ethic slide | Agree |
| L10 | **Relationship to Stage Manager** | Sibling: House = before the damage; Stage Manager = after a named account is already on fire. No phone in House v1. |
| L11 | **v1 surface** | One rehearsal loop + spectrogram + census editor. Not a multi-tenant platform. |

---

## 10. Open questions (only the ones that change the story)

1. Is the primary operator **Product** (launches / breaks), **CS** (comms / policy), or a **launch review room** with both? The census weights and the Cabinet roster follow this.  
2. Do we optimize v1 for **one stimulus type** (recommendation: **breaking change + mass comms**, because Sentry has scar tissue there) or a generic “ask the House anything”?  
3. Is vocality-weight in v1, or do we only ship org-count + ARR and add vocality when we have a real proxy?  
4. How fictional must the Cabinet be for an internal Sentry tool vs a public demo?  
5. Is this an internal Sentry instrument, a hackathon sequel to Stage Manager, or both? (Brief assumes *internal instrument first*; theater vocabulary still works.)

---

## 11. What we will answer after lock (not now)

Once L1–L11 are marked:

1. **How we build it** — census file → stimulus schema → cast → station walk → spectrogram → prompt book; where LLMs sit; what is deterministic.  
2. **Attribute bible** — the dimension list, allowed values, which are quotas vs tags, which are Sentry-exportable later vs authored.  
3. **N, look, interaction** — exact cast sizes, dashboard loop, what “inhabited House” means when nothing is rehearsing.  
4. **Mass management** — census UX (sliders, diffs, versions), re-cast vs morph, coloring, and the spectrogram motion spec.

Until then, treating (2) as “list every demographic” or (3) as “how many live agents” would freeze the wrong product.

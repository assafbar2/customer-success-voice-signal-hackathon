# Implementation

**Sentrants.** Against [STORY.md](./STORY.md). How they live: [LIFE.md](./LIFE.md). Portfolio: [schema/portfolio.md](./schema/portfolio.md).

---

## 1. How we build it

The swarm is the product. A database is how they survive a closed laptop. Twelve “awake” people would be a parliament. We are not doing that.

```text
┌──────────────────────────────────────────────────────────────┐
│  FLOOR — the actual audience                                 │
│  every body · they fidget · they all walk · the room talks   │
└──────────────────────────┬───────────────────────────────────┘
                           │
┌──────────────────────────▼───────────────────────────────────┐
│  MOVES  (always at a portfolio id)                           │
│  ask / tell / price / ship / break / take / jump / rewrite   │
│  e.g. ship seer.mcp · take replay.web · price logs           │
└──────────────────────────┬───────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
┌───────────────┐  ┌───────────────┐  ┌────────────────────┐
│ BODIES        │  │ PHYSICS       │  │ VOICE              │
│ save file     │  │ every person  │  │ the room, not a    │
│ SQLite        │  │ walks, jumps  │  │ panel of twelve    │
└───────────────┘  └───────────────┘  └────────────────────┘
```

### Bodies = save file

Every person is a row. [schema/agent.schema.json](./schema/agent.schema.json). Not what you look at.

### Physics = the swarm moves as one

You make a **move** at a portfolio id. Every sentrant who would actually feel it gets a score. **All of them walk.** Re-score when you edit one sentence.

```text
# we shipped seer.auto (opens PRs without asking)
score_pissed =
    +1.5  coder, senior/staff          # my review queue
    +1.2  low change_appetite
    +1.0  corporate India / agency     # process, PII, “who allowed this”
    +0.8  loud
    -1.0  founder, high change_appetite, 23
    -2.0  already using seer.autofix and happy
```

**Jump** (“a month later”): renewal, quota, *trying*→*in* if they used it, *pissed*→*gone* if they stay mad and cheap, *pissed*→*in* if they cool off. They can pick up `seer.mcp` on their own if it shipped and they have appetite. Dumb on purpose in v1.

### Voice = the room

| What’s happening | LLM? |
| --- | --- |
| Whole swarm walks / fidgets / jumps | No. Physics. Every body. |
| After a walk, **the room talks** | Yes — many one-liners, sampled across *camps × slices* (india corporate, 23 bootcamp, 55 Rails, founders…). Not the same twelve faces. |
| You walk up to anyone | Yes — full person, their memory, their portfolio. |

No shift. No roster. The mix on the floor *is* the Sentry audience. Language is a cloud from that mix.

Batch the room (one job, many lines). Don’t open a socket per ant. Don’t pretend twelve ants are “the customers.”

### Moves

```text
POST /move        { kind, target, artifact, remember }
POST /jump        { days: 30 }
POST /rewrite     { mix, note }
POST /talk        { person_id, message }
POST /copy        → copy_id
POST /restore     { copy_id }
```

`kind`: ask / tell / price / ship / break / take  
`target`: a [portfolio](./schema/portfolio.md) id (`seer.autofix`, `logs`, `sdk.python`, …)  
`remember: false` = rehearsal. They walk; they forget.

### Stack

Python + FastAPI + SQLite · one canvas floor · one LLM adapter later for the room + 1:1 · mix in YAML. Rewrite sliders are a later UI on that YAML (spawn/retire crowds — not identity rewrite).

### Build order

1. Hatch 2,000 (see [LIFE.md](./LIFE.md)) — already the audience  
2. Floor, life mode, four camps, everyone visible, fidgeting  
3. Move at a portfolio id → whole swarm walks  
4. Room talks (many lines, by slice)  
5. Walk up to anyone (card; talk later)  
6. Jump in time  
7. Rewrite sliders (census UI: spawn/retire, never rewrite a living identity)  
8. Copy / restore  
9. Replay a real Sentry scar (quota mail, SDK break, FSL, Seer auto-on) and see if they hurt you

---

## 2. Who they are

**Human life** + **Sentry portfolio** + **seat** + **temperament**.

### Human

| Field | Values |
| --- | --- |
| `age` | 23 / 30 / 40 / 55 |
| `seniority` | junior / mid / senior / staff |
| `education` | bootcamp / self_taught / cs_degree / other |
| `geo` | us / europe / india / latam / east_asia |
| `shop` | hobby / startup / corporate / agency |
| `frameworks[]` | react, next, vue, django, fastapi, flask, rails, laravel, spring, express, flutter, unity, … |
| `seat` | **coder / founder / boss** |

`geo: india` + `shop: corporate` = corporate India.

### How they pay us

`plan` developer / team / business / enterprise · `motion` self_serve / sales_assisted · `deployment` saas / self_hosted · tenure · renewal · ARR band · quota posture · competitive frame · platforms · sdk hygiene · alert noise · residency us/eu.

### What they have of *us* — not `products: [seer]`

See [schema/portfolio.md](./schema/portfolio.md).

```yaml
using:
  signals: [errors, spans, logs]
  capabilities: [issues.suspect_commits, alerts.slack, seer.explain, seer.mcp]
```

A Next founder trying: `errors`.  
A Rails boss in: `errors`, `spans`, `alerts.pagerduty`, `releases`.  
Corporate India in Cursor: `errors`, `spans`, `seer.mcp` — and never `replay.web`.

Those are different people. “They use Seer” is a lie.

### Temperament

`noise_tolerance` · `price_sensitivity` · `change_appetite` · `trust` · `loud` · `loyalty`

### Life

`stage`: **trying / in / pissed / gone** · sentiment · usage · memory.

### Weighting

headcount / ARR / usage / loudness. Always say which.

---

## 3. Number, look, talk

**Sized like an audience, not a focus group.**

Rule: the smallest slice we actually care about still has a **crowd**. If Unity is ~2% of the mix, Unity is dozens of people, not four. That puts the swarm around **~2,000**. 15% vs 17% is 300 vs 340. You can see it. India corporate is a region of the floor, not a spokesperson.

Everyone is on the floor. Everyone walks. Everyone is talkable.

**Alive:** the mass fidgets. Ticker is many things happening in the mix, not a narrator. After a move the room is loud.

**Look:** dark floor. Color-by age, geo, shop, plan, framework, or a portfolio id (who has `seer.mcp`). Two overlays:

- **Life** — trying / in / pissed / gone  
- **Move** — the camps for *this* target (ship it / ignore it / pissed / not me / leaving)

**Hats:** Product, Eng, CS, Pricing — same swarm. Hat suggests a move (Eng → Break `sdk.*`, Product → Ship `seer.review`, Pricing → Price `logs`).

---

## 4. Managing the masses

**Rewrite** = sliders = [schema/census.example.yaml](./schema/census.example.yaml). Drag a slice (“self-hosted 8% → 12%”): **spawn a crowd or retire a crowd**. Don’t rewrite a living person’s identity. That’s god-mode on the census, not Jump.

Jump also moves the mix (they lived). Show *target* vs *now*.

New portfolio ids: add to [schema/portfolio.md](./schema/portfolio.md), default `using` to off, teach physics.

**Walk:** magnets. Whole swarm steers. New question → new magnets. Rewrite → fade in/out a crowd. Jump → they walk to new life camps.

---

## Words we killed

| Dead | Use instead |
| --- | --- |
| The House / Colony | **Sentrants** |
| stimulus | move + target + artifact |
| tick | Jump — “a month later” |
| shift of 12 / cabinet | the swarm. all of them. |
| `products: [seer]` | portfolio ids (`seer.autofix`, `seer.mcp`, …) |
| tickets / bots closing tickets | gone. we don’t do that here. |

---

## Open

1. Is **Ask** allowed to remember? (Default: no.)  
2. Hatch-night LLM polish on origins — yes or skip until templates annoy us.

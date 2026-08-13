# Technical implementation

**Sentrants.** This is the build. Story: [STORY.md](./STORY.md). Hatch: [LIFE.md](./LIFE.md).

---

## Shape

```text
operator  →  FastAPI  →  physics (all 2000)  →  SQLite
                │                ↓
                │         room-talk (batched; templates now, LLM later)
                ↓
         canvas floor (2k dots)  ←  GET /swarm
         click → GET /person/:id
         Move / Jump / Life     →  POST, then lerp
```

Two processes:

| Process | Job |
| --- | --- |
| **engine** | Python. Hatch, jump, move, talk, rewrite. Owns SQLite. |
| **floor** | Browser. Draws the swarm. Does not own truth. |

FastAPI is not what makes them alive. Hatch + SQLite + physics already are. FastAPI is the **live wire**: the browser POSTs a move or a jump and lerps 2,000 dots without regenerating HTML. `data/floor.html` is a snapshot you can open; it cannot take a Move.

No agent runtime. No LangGraph. No socket per ant.

---

## Stack

| Layer | Choice | Why |
| --- | --- | --- |
| Engine | Python 3.12 | Hatch + physics is data, not a web app |
| API | FastAPI | Live wire. POST move/jump, GET swarm. Not the soul. |
| Save | SQLite, one file `data/sentrants.sqlite` | Copy the file = snapshot |
| Census | YAML | Git-diffable rewrite |
| Floor | One HTML canvas, 2d | 2,000 circles is nothing. WebGL later if trails demand it |
| LLM | One port: `complete(system, user) → str` | Anthropic/OpenAI behind it. Hatch does not call it |

---

## Save file

One row per sentrant. Indexed columns for the mix and the floor; the rest is JSON that matches [schema/agent.schema.json](./schema/agent.schema.json).

```sql
CREATE TABLE sentrants (
  id            TEXT PRIMARY KEY,
  stage         TEXT NOT NULL,          -- trying|in|pissed|gone
  geo           TEXT NOT NULL,
  shop          TEXT NOT NULL,
  seat          TEXT NOT NULL,
  age           INTEGER NOT NULL,
  plan          TEXT NOT NULL,
  x             REAL NOT NULL,          -- floor
  y             REAL NOT NULL,
  body          TEXT NOT NULL           -- JSON
);

CREATE TABLE meta (
  key TEXT PRIMARY KEY,
  value TEXT NOT NULL
);

CREATE TABLE events (
  id INTEGER PRIMARY KEY,
  at TEXT NOT NULL,
  kind TEXT NOT NULL,
  target TEXT,
  payload TEXT NOT NULL
);
```

`meta`: census hash, hatch seed, sim day.  
`events`: prompt book. Every move / jump / rewrite / talk.

Snapshot: `cp data/sentrants.sqlite data/snapshots/<id>.sqlite`. Restore: copy back.

---

## Hatch (engine, no LLM)

Module: `sentrants.hatch`.

1. Load census YAML → integer **quotas** (largest-remainder so they sum to `n`).
2. `propose()` — draw a person with **segment priors** (corporate India, bootcamp Next, Rails boss…). Framework is drawn; platforms are **derived**. Don’t roll platform and framework independently.
3. Hard **reject** (23+staff, founder+corporate, …). See [LIFE.md](./LIFE.md).
4. Hard **overflow reject** — if `geo=us` is already full, no more US. Same for shop, seat, age, plan, framework, stage.
5. Repeat until `n=2000` or panic (too many stuck → loosen the last overflow, log it).
6. Name, compile `voice`, fill `origin`.
7. Place on the floor: jitter inside the camp rect for `stage`.
8. Insert SQLite. Print mix. If `geo=india × shop=corporate` isn’t a crowd, hatch is wrong — don’t draw, don’t call a model.

`--seed` is required for replay.

Rewrite is hatch of a delta: spawn into underfilled quotas, or set overflow people to `gone`.

---

## Physics (engine, no LLM)

`sentrants.physics.score(person, move) → {camp: float}` then argmax (or softmax sample for scatter inside a camp).

A **move** is `{kind, target, artifact, remember}`. `target` is a portfolio id.

Eligibility: `gone` sit out unless the move is Ask-about-churn. Python break → only people with `python` in platforms. etc.

**Jump(days)**: for each body, tick tenure, renewal, quota, sentiment; maybe `trying`→`in`; maybe `pissed`→`gone` if cheap and mad; maybe pick up a shipped capability if `change_appetite` is high. Then re-place on the life floor.

Scoring functions live in `sentrants/moves/` keyed by `kind` + `target` (default generic). First real one: `ship seer.auto`.

---

## Voice (LLM, lazy)

Port: `sentrants.llm.complete`.

| Call | When | Prompt |
| --- | --- | --- |
| Room | After a walk | ~60 cards (stratified by camp × geo × shop × seat) → one-liners. Write `quote` onto those rows. |
| Talk | `POST /talk` | `voice` + `origin` + `body` + `memory` + user line. Append memory. |

Hatch never calls this. Room is **one** batched completion, not 2,000. v1 writes template one-liners into the same slots so the floor has a room without a model.

---

## Floor

Canvas 2d. 2,000 `arc()`s. 60fps fidget = tiny random walk clamped to camp AABB.

Camps (life mode): four labeled rects. Move mode: relabel, lerp `x,y` to new camps over ~1.5s.

`GET /swarm` returns `{id, x, y, stage, geo, age, shop, seat}[]` — not full bodies. `GET /person/:id` is the card.

Color-by is a shader on those fields. 2,000 points is ~50KB. Fine.

Static `data/floor.html` is still a snapshot (hatch / `sentrants floor`). The live floor is `sentrants serve`.

---

## HTTP (live floor)

```
GET  /
GET  /mix
GET  /slices
GET  /swarm
GET  /person/:id
POST /move      { target, remember }
POST /jump      { days: 30 }
POST /life
POST /talk      (later)
POST /rewrite   (later — census sliders, spawn/retire)
```

---

## Repo

```text
sentrants/
  sentrants/          # engine
    hatch.py
    physics.py
    room.py
    engine.py
    api.py
    db.py
    cli.py
    static/index.html # live floor
  schema/             # census, agent, portfolio, move
  data/               # sqlite, gitignored
  TECH.md             # this file
```

---

## v0 (this folder, now)

Hatch 2,000 → SQLite → mix printed. `python3 -m sentrants serve` → live floor. Move walks everyone. Jump is a month later. Room-talk is batched templates (same pick as a later LLM batch). No model. Hatch never calls one.

If the floor doesn’t look like Sentry, stop.

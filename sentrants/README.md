# Sentrants

**Sentrants** — Sentry + ants. A living swarm of Sentry customers. You run the place.

Not the CALL-E hackathon.

| File | What |
| --- | --- |
| [STORY.md](./STORY.md) | What this is |
| [TECH.md](./TECH.md) | Engineering: stack, save file, hatch, physics, floor |
| [LIFE.md](./LIFE.md) | How 2,000 of them hatch and stay alive |
| [NAMES.md](./NAMES.md) | Other names we didn’t pick |
| [IMPLEMENTATION.md](./IMPLEMENTATION.md) | Build · people · moves · the floor |
| [schema/portfolio.md](./schema/portfolio.md) | Full Sentry surface (signals + Seer/MCP/…) |
| [schema/agent.schema.json](./schema/agent.schema.json) | One sentrant |
| [schema/census.example.yaml](./schema/census.example.yaml) | The mix |
| [schema/slices.md](./schema/slices.md) | Audience joints (covering map + callouts) |
| [schema/move.example.yaml](./schema/move.example.yaml) | Something we did to them |

Copy to `/1Code/sentrants` on any laptop.

```bash
cd /1Code/sentrants
python3 -m pip install -e '.[dev]'
python3 -m sentrants hatch          # 2000 people → data/sentrants.sqlite
python3 -m sentrants mix
python3 -m sentrants slices         # covering map + callouts (US founder 23, corporate India, …)
python3 -m sentrants show --geo india --shop corporate
python3 -m sentrants walk           # ship seer.auto — who walks where (no save)
python3 -m sentrants serve          # live floor → http://127.0.0.1:8765/
```

`serve` is the live floor. **Life** / **Move: Seer auto** (lerp) / **Jump in time**. After a walk the room talks. Click anyone for the card.

Static snapshot still exists: `python3 -m sentrants floor` writes `data/floor.html`. That file cannot take a move — that’s why the API exists.

```bash
python3 -m pytest
python3 -m sentrants jump --days 30   # a month later, writes SQLite
```

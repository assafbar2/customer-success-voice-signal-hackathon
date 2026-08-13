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

**On your Mac it lives at** `/Users/assafbarnir/1Code/sentrants`.

This agent cannot create a separate GitHub repo (token is this hackathon repo only). Until `assafbar2/sentrants` exists, the code is this folder. Copy it out:

```bash
mkdir -p /Users/assafbarnir/1Code
git clone https://github.com/assafbar2/customer-success-voice-signal-hackathon.git /tmp/cs-hackathon
rm -rf /Users/assafbarnir/1Code/sentrants
cp -R /tmp/cs-hackathon/sentrants /Users/assafbarnir/1Code/sentrants
cd /Users/assafbarnir/1Code/sentrants
python3 -m pip install -e '.[dev]'
python3 -m sentrants hatch          # 2000 people → data/sentrants.sqlite
python3 -m sentrants serve          # http://127.0.0.1:8765/
```

`serve` is the live floor. **Life** / **Move: Seer auto** (lerp) / **Jump in time**. After a walk the room talks. Click anyone for the card.

Static snapshot still exists: `python3 -m sentrants floor` writes `data/floor.html`. That file cannot take a move — that’s why the API exists.

```bash
python3 -m pytest
python3 -m sentrants jump --days 30   # a month later, writes SQLite
```

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DB = ROOT / "data" / "sentrants.sqlite"

SCHEMA = """
CREATE TABLE IF NOT EXISTS sentrants (
  id    TEXT PRIMARY KEY,
  stage TEXT NOT NULL,
  geo   TEXT NOT NULL,
  shop  TEXT NOT NULL,
  seat  TEXT NOT NULL,
  age   INTEGER NOT NULL,
  plan  TEXT NOT NULL,
  x     REAL NOT NULL,
  y     REAL NOT NULL,
  body  TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS meta (
  key TEXT PRIMARY KEY,
  value TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS events (
  id INTEGER PRIMARY KEY,
  at TEXT NOT NULL,
  kind TEXT NOT NULL,
  target TEXT,
  payload TEXT NOT NULL
);
"""


def connect(path: Path | None = None) -> sqlite3.Connection:
    path = path or DEFAULT_DB
    path.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(path)
    con.row_factory = sqlite3.Row
    con.executescript(SCHEMA)
    return con


def _row(p: dict) -> tuple:
    h, s = p["human"], p["sentry"]
    body = {k: v for k, v in p.items() if not k.startswith("_")}
    if p.get("_quote"):
        body.setdefault("life", {})["last_quote"] = p["_quote"]
    if p.get("_camp"):
        body.setdefault("life", {})["camp"] = p["_camp"]
    return (
        p["id"],
        p["life"]["stage"],
        h["geo"],
        h["shop"],
        h["seat"],
        h["age"],
        s["plan"],
        p["_x"],
        p["_y"],
        json.dumps(body),
    )


def save_people(people: list[dict], *, seed: int, path: Path | None = None) -> Path:
    path = path or DEFAULT_DB
    if path.exists():
        path.unlink()
    con = connect(path)
    con.executemany(
        "INSERT INTO sentrants (id, stage, geo, shop, seat, age, plan, x, y, body) "
        "VALUES (?,?,?,?,?,?,?,?,?,?)",
        [_row(p) for p in people],
    )
    con.execute("INSERT INTO meta (key, value) VALUES ('seed', ?)", (str(seed),))
    con.execute("INSERT INTO meta (key, value) VALUES ('n', ?)", (str(len(people)),))
    con.execute("INSERT INTO meta (key, value) VALUES ('sim_day', '0')")
    con.execute("INSERT INTO meta (key, value) VALUES ('mode', 'life')")
    con.commit()
    con.close()
    return path


def upsert_people(people: list[dict], path: Path | None = None) -> None:
    con = connect(path)
    con.executemany(
        "UPDATE sentrants SET stage=?, geo=?, shop=?, seat=?, age=?, plan=?, x=?, y=?, body=? WHERE id=?",
        [
            (r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], r[9], r[0])
            for r in (_row(p) for p in people)
        ],
    )
    con.commit()
    con.close()


def meta_get(key: str, default: str = "", path: Path | None = None) -> str:
    con = connect(path)
    row = con.execute("SELECT value FROM meta WHERE key=?", (key,)).fetchone()
    con.close()
    return row["value"] if row else default


def meta_set(key: str, value: str, path: Path | None = None) -> None:
    con = connect(path)
    con.execute(
        "INSERT INTO meta (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
        (key, value),
    )
    con.commit()
    con.close()


def log_event(kind: str, payload: dict, target: str | None = None, path: Path | None = None) -> None:
    from datetime import datetime, timezone

    con = connect(path)
    con.execute(
        "INSERT INTO events (at, kind, target, payload) VALUES (?,?,?,?)",
        (
            datetime.now(timezone.utc).isoformat(),
            kind,
            target,
            json.dumps(payload),
        ),
    )
    con.commit()
    con.close()


def get_person(person_id: str, path: Path | None = None) -> dict | None:
    con = connect(path)
    row = con.execute("SELECT body, x, y FROM sentrants WHERE id=?", (person_id,)).fetchone()
    con.close()
    if not row:
        return None
    p = json.loads(row["body"])
    p["_x"] = row["x"]
    p["_y"] = row["y"]
    p["_camp"] = p.get("life", {}).get("camp") or p["life"]["stage"]
    p["_quote"] = p.get("life", {}).get("last_quote")
    return p


def swarm_dots(people: list[dict]) -> list[dict]:
    out = []
    for p in people:
        h, life = p["human"], p["life"]
        out.append(
            {
                "id": p["id"],
                "name": p["display_name"],
                "x": p["_x"],
                "y": p["_y"],
                "stage": life["stage"],
                "camp": p.get("_camp") or life.get("camp") or life["stage"],
                "geo": h["geo"],
                "shop": h["shop"],
                "seat": h["seat"],
                "age": h["age"],
                "plan": p["sentry"]["plan"],
                "framework": h["frameworks"][0],
                "origin": p["origin"],
                "quote": p.get("_quote") or life.get("last_quote"),
            }
        )
    return out


def load_people(path: Path | None = None) -> list[dict]:
    con = connect(path)
    out = []
    for row in con.execute("SELECT body, x, y FROM sentrants"):
        p = json.loads(row["body"])
        p["_x"] = row["x"]
        p["_y"] = row["y"]
        p["_camp"] = p.get("life", {}).get("camp") or p["life"]["stage"]
        p["_quote"] = p.get("life", {}).get("last_quote")
        out.append(p)
    con.close()
    return out

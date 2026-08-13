from fastapi.testclient import TestClient

from sentrants.api import app
from sentrants.census import load_census
from sentrants.db import save_people
from sentrants.hatch import hatch
import sentrants.db as dbmod


def test_floor_page_has_jump(tmp_path, monkeypatch):
    path = tmp_path / "s.sqlite"
    monkeypatch.setattr(dbmod, "DEFAULT_DB", path)
    save_people(hatch(load_census(), seed=1, n=40), seed=1, path=path)
    client = TestClient(app)
    page = client.get("/")
    assert page.status_code == 200
    assert "Jump in time" in page.text
    assert "Sentry down 90m" in page.text


def test_move_and_jump_endpoints(tmp_path, monkeypatch):
    path = tmp_path / "s.sqlite"
    monkeypatch.setattr(dbmod, "DEFAULT_DB", path)
    people = hatch(load_census(), seed=1, n=60)
    save_people(people, seed=1, path=path)
    client = TestClient(app)
    swarm = client.get("/swarm")
    assert swarm.status_code == 200
    assert swarm.json()["mode"] == "life"
    assert len(swarm.json()["swarm"]) == 60
    moved = client.post("/move", json={"target": "seer.auto"})
    assert moved.status_code == 200
    body = moved.json()
    assert body["mode"] == "move"
    assert body["quotes"]
    assert len(body["quotes"]) <= 60
    pid = body["swarm"][0]["id"]
    card = client.get(f"/person/{pid}")
    assert card.status_code == 200
    assert card.json()["name"]
    jumped = client.post("/jump", json={"days": 30})
    assert jumped.status_code == 200
    assert jumped.json()["day"] == 30
    assert jumped.json()["mode"] == "life"
    life = client.post("/life")
    assert life.status_code == 200
    assert life.json()["mode"] == "life"
    down = client.post("/move", json={"target": "sentry.down", "remember": True})
    assert down.status_code == 200
    assert down.json()["target"] == "sentry.down"
    assert down.json()["mode"] == "move"

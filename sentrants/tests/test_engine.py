from sentrants.census import load_census
from sentrants.db import load_people, save_people
from sentrants.engine import run_jump, run_move
from sentrants.hatch import hatch
import sentrants.db as dbmod


def _seed(tmp_path, monkeypatch, n=80):
    path = tmp_path / "s.sqlite"
    monkeypatch.setattr(dbmod, "DEFAULT_DB", path)
    people = hatch(load_census(), seed=1, n=n)
    save_people(people, seed=1, path=path)
    return path


def test_move_walks_everyone(tmp_path, monkeypatch):
    _seed(tmp_path, monkeypatch)
    out = run_move(target="seer.auto", remember=False)
    people = load_people()
    assert len(people) == 80
    assert sum(out["counts"].values()) == 80
    assert out["quotes"]
    assert people[0]["_camp"] in out["labels"]
    for p in people:
        mem = p["life"].get("memory") or []
        assert not any(m.get("target") == "seer.auto" for m in mem)


def test_move_remember_writes_memory(tmp_path, monkeypatch):
    _seed(tmp_path, monkeypatch, n=40)
    run_move(target="seer.auto", remember=True)
    people = load_people()
    remembered = [p for p in people if any(m.get("target") == "seer.auto" for m in p["life"].get("memory") or [])]
    assert len(remembered) == 40


def test_jump_changes_some_lives(tmp_path, monkeypatch):
    _seed(tmp_path, monkeypatch, n=200)
    before = [p["life"]["stage"] for p in load_people()]
    out = run_jump(days=30)
    after = [p["life"]["stage"] for p in load_people()]
    assert out["day"] == 30
    assert out["mode"] == "life"
    assert out["transitions"]
    assert before != after
    assert out["quotes"]

from sentrants.census import load_census
from sentrants.constraints import reject_reason
from sentrants.hatch import hatch
from sentrants.slices import COVERING, CALLOUTS


def test_rejects_impossible_people():
    people = hatch(load_census(), seed=0, n=200)
    for person in people:
        assert reject_reason(person) is None
    assert len(people) == 200


def test_india_corporate_is_a_crowd():
    people = hatch(load_census(), seed=1, n=400)
    n = sum(
        1
        for p in people
        if p["human"]["geo"] == "india" and p["human"]["shop"] == "corporate"
    )
    assert n >= 20, n


def test_trying_is_not_enterprise():
    people = hatch(load_census(), seed=2, n=300)
    bad = [
        p
        for p in people
        if p["life"]["stage"] == "trying" and p["sentry"]["plan"] == "enterprise"
    ]
    assert bad == []


def test_covering_map_is_everyone():
    people = hatch(load_census(), seed=1, n=400)
    covered = [p for p in people if any(pred(p) for _, _, pred in COVERING)]
    assert len(covered) == 400


def test_us_founder_23_exists():
    people = hatch(load_census(), seed=1, n=2000)
    pred = next(fn for sid, _, fn in CALLOUTS if sid == "us_founder_23")
    n = sum(1 for p in people if pred(p))
    assert 20 <= n <= 120, n

from __future__ import annotations

from sentrants.db import (
    get_person,
    load_people,
    log_event,
    meta_get,
    meta_set,
    swarm_dots,
    upsert_people,
)
from sentrants.layout import LIFE
from sentrants.physics import MOVES, apply_move, jump, to_life_floor
from sentrants.room import room_talk


def current_mode() -> str:
    return meta_get("mode", "life") or "life"


def current_day() -> int:
    return int(meta_get("sim_day", "0") or 0)


def current_target() -> str:
    return meta_get("move_target", "") or ""


def swarm_payload() -> dict:
    people = load_people()
    mode = current_mode()
    target = current_target()
    spec = MOVES.get(target) if mode == "move" else None
    if spec:
        camps, labels, title = spec["camps"], spec["labels"], spec["title"]
    else:
        camps, labels, title = LIFE, {k: k for k in LIFE}, "life"
    return {
        "mode": mode,
        "target": target if spec else "life",
        "title": title,
        "day": current_day(),
        "camps": {k: list(v) for k, v in camps.items()},
        "labels": labels,
        "swarm": swarm_dots(people),
    }


def run_move(*, target: str = "seer.auto", remember: bool = False) -> dict:
    people = load_people()
    summary = apply_move(people, target=target, remember=remember)
    quotes = room_talk(people)
    upsert_people(people)
    meta_set("mode", "move")
    meta_set("move_target", target)
    log_event("move", {"counts": summary["counts"], "remember": remember}, target)
    summary["quotes"] = quotes
    summary["day"] = current_day()
    summary["swarm"] = swarm_dots(people)
    return summary


def run_jump(*, days: int = 30) -> dict:
    people = load_people()
    summary = jump(people, days=days)
    quotes = room_talk(people)
    upsert_people(people)
    day = current_day() + days
    meta_set("sim_day", str(day))
    meta_set("mode", "life")
    log_event("jump", summary)
    summary["quotes"] = quotes
    summary["day"] = day
    summary["mode"] = "life"
    summary["target"] = "life"
    summary["labels"] = {k: k for k in LIFE}
    summary["camps"] = {k: list(v) for k, v in LIFE.items()}
    summary["swarm"] = swarm_dots(people)
    from collections import Counter

    summary["stages"] = dict(Counter(p["life"]["stage"] for p in people))
    return summary


def run_life() -> dict:
    people = load_people()
    to_life_floor(people)
    upsert_people(people)
    meta_set("mode", "life")
    return swarm_payload()


def person_card(person_id: str) -> dict | None:
    p = get_person(person_id)
    if not p:
        return None
    return {
        "id": p["id"],
        "name": p["display_name"],
        "origin": p["origin"],
        "voice": p["voice"],
        "human": p["human"],
        "sentry": {
            "plan": p["sentry"]["plan"],
            "deployment": p["sentry"]["deployment"],
            "using": p["sentry"]["using"],
        },
        "life": p["life"],
        "temperament": p["temperament"],
        "quote": p.get("_quote"),
    }

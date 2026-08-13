from __future__ import annotations

from random import Random

# x, y, w, h
LIFE = {
    "trying": (40, 40, 260, 420),
    "in": (340, 40, 520, 420),
    "pissed": (900, 40, 280, 420),
    "gone": (40, 500, 1140, 170),
}

SEER_AUTO = {
    "yes_leave_it": (40, 40, 210, 400),
    "yes_but_manual": (270, 40, 220, 400),
    "hell_no": (510, 40, 230, 400),
    "not_me": (760, 40, 220, 400),
    "leaving": (40, 480, 1140, 180),
}

SEER_AUTO_LABELS = {
    "yes_leave_it": "Leave it on",
    "yes_but_manual": "Fine if I click",
    "hell_no": "Not in my repo",
    "not_me": "I don't use Seer",
    "leaving": "I'm done",
}


def place(camps: dict, camp: str, rng: Random) -> tuple[float, float]:
    x, y, w, h = camps[camp]
    pad = 12
    return (
        x + pad + rng.random() * max(8, w - 2 * pad),
        y + pad + rng.random() * max(8, h - 2 * pad),
    )


def place_stable(camps: dict, camp: str, person_id: str) -> tuple[float, float]:
    rng = Random(person_id + camp)
    return place(camps, camp, rng)

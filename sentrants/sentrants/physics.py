from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from random import Random

from sentrants.layout import LIFE, SEER_AUTO, SEER_AUTO_LABELS, place_stable


def score_seer_auto(p: dict) -> dict[str, float]:
    """Camps for: we shipped Autofix opening PRs on its own."""
    h, s, t, life = p["human"], p["sentry"], p["temperament"], p["life"]
    if life["stage"] == "gone":
        return {"not_me": 3.0, "hell_no": 0, "yes_leave_it": 0, "yes_but_manual": 0, "leaving": 0.4}

    using = s["using"]["capabilities"]
    has_seer = any(x.startswith("seer.") for x in using)
    scores = {
        "yes_leave_it": 0.2,
        "yes_but_manual": 0.4,
        "hell_no": 0.3,
        "not_me": 0.2 if has_seer else 1.8,
        "leaving": 0.05,
    }
    if h["seat"] == "coder" and h["seniority"] in ("senior", "staff"):
        scores["hell_no"] += 1.5
        scores["yes_but_manual"] += 0.4
    if t["change_appetite"] < 0.35:
        scores["hell_no"] += 1.2
    if t["change_appetite"] > 0.7 and h["age"] == 23:
        scores["yes_leave_it"] += 1.4
    if h["geo"] == "india" and h["shop"] == "corporate":
        scores["hell_no"] += 1.0
        scores["yes_but_manual"] += 0.5
    if t["loud"] > 0.65:
        scores["hell_no"] += 0.4
        scores["leaving"] += 0.15
    if "seer.autofix" in using:
        scores["yes_but_manual"] += 1.2
        scores["hell_no"] -= 0.6
    if h["seat"] == "founder" and t["change_appetite"] > 0.55:
        scores["yes_leave_it"] += 0.8
    return scores


def pick_camp(scores: dict[str, float]) -> str:
    return max(scores, key=scores.get)


MOVES = {
    "seer.auto": {
        "kind": "ship",
        "title": "Seer will open PRs on issues it thinks it can fix",
        "score": score_seer_auto,
        "camps": SEER_AUTO,
        "labels": SEER_AUTO_LABELS,
    }
}


def apply_move(people: list[dict], *, target: str = "seer.auto", remember: bool = False) -> dict:
    spec = MOVES[target]
    counts: Counter = Counter()
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    for p in people:
        camp = pick_camp(spec["score"](p))
        p["_camp"] = camp
        p["_x"], p["_y"] = place_stable(spec["camps"], camp, p["id"])
        counts[camp] += 1
        if remember:
            p["life"].setdefault("memory", []).append(
                {
                    "at": now,
                    "kind": spec["kind"],
                    "target": target,
                    "remember": True,
                    "camp": camp,
                    "quote": None,
                }
            )
            if camp == "leaving":
                p["life"]["stage"] = "pissed" if p["life"]["stage"] != "gone" else "gone"
                p["life"]["sentiment"] = min(p["life"]["sentiment"], -0.4)
            elif camp == "hell_no":
                p["life"]["sentiment"] = max(-1.0, p["life"]["sentiment"] - 0.12)
    return {
        "target": target,
        "title": spec["title"],
        "mode": "move",
        "labels": spec["labels"],
        "counts": dict(counts),
        "camps": {k: list(v) for k, v in spec["camps"].items()},
    }


def to_life_floor(people: list[dict]) -> None:
    for p in people:
        stage = p["life"]["stage"]
        p["_camp"] = stage
        p["_x"], p["_y"] = place_stable(LIFE, stage, p["id"])


def jump(people: list[dict], *, days: int = 30, seed: int = 1) -> dict:
    rng = Random(seed + days + len(people))
    months = max(1, round(days / 30))
    changed = Counter()
    for p in people:
        s, life, t = p["sentry"], p["life"], p["temperament"]
        before = life["stage"]
        s["tenure_months"] = int(s["tenure_months"]) + months
        if s.get("renewal_in_days") is not None:
            s["renewal_in_days"] = max(0, int(s["renewal_in_days"]) - days)
        r = rng.random()
        stage = life["stage"]
        if stage == "trying" and s["tenure_months"] >= 2 and r < 0.32 + t["change_appetite"] * 0.2:
            life["stage"] = "in"
            life["usage"] = min(1.0, life["usage"] + 0.2)
            life["sentiment"] = min(1.0, life["sentiment"] + 0.1)
        elif stage == "pissed":
            if t["price_sensitivity"] > 0.6 and t["loyalty"] < 0.45 and r < 0.22:
                life["stage"] = "gone"
                life["usage"] = 0.0
            elif r < 0.28:
                life["stage"] = "in"
                life["sentiment"] = min(0.4, life["sentiment"] + 0.25)
        elif stage == "in":
            if s["quota_posture"] == "spiked_recently" and t["price_sensitivity"] > 0.55 and r < 0.14:
                life["stage"] = "pissed"
                life["sentiment"] = max(-1.0, life["sentiment"] - 0.3)
            elif t["change_appetite"] > 0.65 and r < 0.08:
                caps = s["using"]["capabilities"]
                if "seer.mcp" not in caps and s["plan"] != "developer":
                    caps.append("seer.mcp")
        if life["stage"] != before:
            changed[f"{before}->{life['stage']}"] += 1
    to_life_floor(people)
    return {"days": days, "transitions": dict(changed)}

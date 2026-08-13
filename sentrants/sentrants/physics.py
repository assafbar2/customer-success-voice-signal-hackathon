from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from random import Random

from sentrants.layout import (
    LIFE,
    OUTAGE,
    OUTAGE_LABELS,
    SEER_AUTO,
    SEER_AUTO_LABELS,
    place_stable,
)


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


def score_sentry_down(p: dict) -> dict[str, float]:
    """Camps for: Sentry SaaS has been down for 90 minutes."""
    h, s, t, life = p["human"], p["sentry"], p["temperament"], p["life"]
    scores = {
        "wait_it_out": 0.4,
        "we_were_blind": 0.5,
        "also_datadog": 0.15,
        "not_me": 0.1,
        "leaving": 0.08,
    }
    if s.get("deployment") == "self_hosted":
        return {"not_me": 4.0, "wait_it_out": 0, "we_were_blind": 0, "also_datadog": 0.1, "leaving": 0}
    if life["stage"] == "gone":
        return {"not_me": 2.4, "leaving": 0.6, "wait_it_out": 0, "we_were_blind": 0, "also_datadog": 0.3}

    if life["stage"] == "trying":
        scores["leaving"] += 0.8
        scores["wait_it_out"] -= 0.2
    if life["stage"] == "pissed":
        scores["leaving"] += 1.4
        scores["we_were_blind"] += 0.6
        scores["wait_it_out"] -= 0.3
    if life["stage"] == "in":
        scores["wait_it_out"] += 0.6

    if h["seat"] == "coder":
        scores["we_were_blind"] += 1.3
    if h["seat"] in ("founder", "boss"):
        scores["we_were_blind"] += 0.7
        scores["leaving"] += 0.25
    if t["loyalty"] > 0.65:
        scores["wait_it_out"] += 1.2
        scores["leaving"] -= 0.3
    if t["loyalty"] < 0.4:
        scores["leaving"] += 0.7
    if t["loud"] > 0.65:
        scores["we_were_blind"] += 0.4
        scores["leaving"] += 0.2
    frame = s.get("competitive_frame") or "sentry_only"
    if frame in ("also_datadog", "also_newrelic", "evaluating_exit", "self_rolled"):
        scores["also_datadog"] += 1.8
        scores["leaving"] += 0.3
    if s.get("plan") in ("business", "enterprise") and t["loyalty"] > 0.5:
        scores["wait_it_out"] += 0.5
    if h["shop"] == "hobby" or s.get("plan") == "developer":
        scores["wait_it_out"] += 0.3
        scores["we_were_blind"] -= 0.2
    return scores


MOVES = {
    "seer.auto": {
        "kind": "ship",
        "title": "Seer will open PRs on issues it thinks it can fix",
        "score": score_seer_auto,
        "camps": SEER_AUTO,
        "labels": SEER_AUTO_LABELS,
    },
    "sentry.down": {
        "kind": "break",
        "title": "Sentry SaaS has been down for 90 minutes",
        "score": score_sentry_down,
        "camps": OUTAGE,
        "labels": OUTAGE_LABELS,
    },
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
            _remember_hurt(p, camp, target)
    return {
        "target": target,
        "title": spec["title"],
        "mode": "move",
        "labels": spec["labels"],
        "counts": dict(counts),
        "camps": {k: list(v) for k, v in spec["camps"].items()},
    }


def _remember_hurt(p: dict, camp: str, _target: str) -> None:
    life, s = p["life"], p["sentry"]
    if camp == "leaving":
        if life["stage"] == "trying" or (life["stage"] == "pissed" and p["temperament"]["loyalty"] < 0.45):
            life["stage"] = "gone"
            life["usage"] = 0.0
        elif life["stage"] != "gone":
            life["stage"] = "pissed"
        life["sentiment"] = min(life["sentiment"], -0.4)
    elif camp in ("hell_no", "we_were_blind"):
        life["sentiment"] = max(-1.0, life["sentiment"] - 0.18)
        if camp == "we_were_blind" and life["stage"] == "in" and life["sentiment"] < -0.35:
            life["stage"] = "pissed"
    elif camp == "also_datadog":
        s["competitive_frame"] = "also_datadog"
        life["sentiment"] = max(-1.0, life["sentiment"] - 0.1)
    elif camp == "wait_it_out":
        life["sentiment"] = max(-1.0, life["sentiment"] - 0.05)


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

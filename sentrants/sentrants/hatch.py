from __future__ import annotations

import uuid
from collections import defaultdict
from random import Random

from sentrants.census import load_census, remaining_ok
from sentrants.constraints import reject_reason
from sentrants.flavor import compile_voice, name_for, origin_for
from sentrants.using import FRAMEWORK_PLATFORMS, assign_using
from sentrants.layout import LIFE, place_stable

CAMPS = LIFE  # back-compat

OVERFLOW_DIMS = ("geo", "shop", "seat", "age", "plan", "framework", "stage")


def _w(rng: Random, weights: dict):
    keys = [k for k, v in weights.items() if v > 0]
    vals = [weights[k] for k in keys]
    return rng.choices(keys, weights=vals, k=1)[0]


def _bump(d: dict, key, factor: float) -> dict:
    out = dict(d)
    if key in out:
        out[key] = out[key] * factor
    return out


def _remaining(census: dict, filled: dict, dim: str, src_key: str | None = None) -> dict:
    src = census[src_key or dim]
    q = census["_quotas"][dim]
    w = {}
    for k, _ in src.items():
        kk = int(k) if dim == "age" else k
        left = q[kk] - filled[dim].get(kk, 0)
        if left > 0:
            w[kk] = float(left)
    return w


def propose(rng: Random, census: dict, filled: dict | None = None) -> dict:
    filled = filled or {dim: defaultdict(int) for dim in OVERFLOW_DIMS}

    def take(dim: str, bumps: list[tuple] | None = None, src_key: str | None = None):
        w = _remaining(census, filled, dim, src_key)
        if not w:
            raw = census[src_key or dim]
            w = {int(k) if dim == "age" else k: float(v) for k, v in raw.items()}
        for key, factor in bumps or []:
            w = _bump(w, key, factor)
        if not any(v > 0 for v in w.values()):
            w = _remaining(census, filled, dim, src_key) or {
                int(k) if dim == "age" else k: float(v)
                for k, v in census[src_key or dim].items()
            }
        return _w(rng, w)

    geo = take("geo")
    shop_bumps = []
    if geo == "india":
        shop_bumps = [("corporate", 2.1), ("hobby", 0.45)]
    shop = take("shop", shop_bumps)

    seat_bumps = []
    if shop == "corporate":
        seat_bumps = [("founder", 0.0001), ("boss", 1.7)]
    if shop == "hobby":
        seat_bumps = [("boss", 0.15), ("founder", 1.5)]
    seat = take("seat", seat_bumps)

    age_bumps = []
    if seat == "founder":
        age_bumps = [(23, 1.25), (30, 1.45), (55, 0.15)]
    if seat == "boss":
        age_bumps = [(23, 0.12), (40, 1.5), (55, 2.1)]
    age = int(take("age", age_bumps))

    sen_w = dict(census["seniority"])
    if age == 23:
        sen_w["staff"] = 0
        sen_w["junior"] *= 2.2
        sen_w["senior"] *= 0.4
    if age == 55:
        sen_w["junior"] *= 0.12
        sen_w["staff"] *= 2.0
        sen_w["senior"] *= 1.4
    if seat == "founder":
        sen_w["junior"] = 0
    seniority = _w(rng, sen_w)

    edu_w = dict(census["education"])
    if age == 23:
        edu_w["bootcamp"] *= 2.3
        edu_w["cs_degree"] *= 0.8
    if age == 55:
        edu_w["bootcamp"] *= 0.2
        edu_w["cs_degree"] *= 1.3
    education = _w(rng, edu_w)

    fw_bumps = []
    if geo == "india" and shop == "corporate":
        fw_bumps = [("spring", 3.2), ("django", 1.6), ("rails", 0.35), ("next", 0.7)]
    if age == 23:
        fw_bumps += [("next", 2.2), ("react", 1.5), ("rails", 0.4)]
    if age == 55:
        fw_bumps += [("rails", 2.4), ("django", 1.4), ("next", 0.45)]
    framework = take("framework", fw_bumps)

    plan_bumps = []
    if shop == "hobby":
        plan_bumps = [("developer", 3.5), ("enterprise", 0), ("business", 0.25)]
    if shop == "corporate":
        plan_bumps = [("developer", 0.25), ("business", 1.8), ("enterprise", 1.7)]
    if seat == "founder":
        plan_bumps += [("team", 1.5), ("enterprise", 0.35)]
    plan = take("plan", plan_bumps)

    dep_w = dict(census["deployment"])
    if geo == "europe":
        dep_w["self_hosted"] *= 1.8
    if seat == "boss" and shop == "corporate":
        dep_w["self_hosted"] *= 1.4
    if plan == "developer":
        dep_w["self_hosted"] = 0
    deployment = _w(rng, dep_w)

    motion_w = dict(census["motion"])
    if plan in ("business", "enterprise"):
        motion_w["sales_assisted"] *= 2.2
    if shop == "hobby":
        motion_w["sales_assisted"] *= 0.2
    motion = _w(rng, motion_w)

    stage_bumps = []
    if plan == "developer":
        stage_bumps = [("trying", 2.0)]
    if plan == "enterprise":
        stage_bumps = [("trying", 0.2), ("in", 1.3)]
    stage = take("stage", stage_bumps)

    if stage == "trying":
        tenure = rng.randint(0, 8)
    elif stage == "gone":
        tenure = rng.randint(14, 96)
    else:
        tenure = rng.randint(4, 84)

    quota_w = dict(census["quota_posture"])
    if stage == "pissed":
        quota_w["spiked_recently"] *= 2.5
        quota_w["near_limit"] *= 1.6
    if stage == "trying":
        quota_w["spiked_recently"] *= 0.4
    quota_posture = _w(rng, quota_w)

    # temperament — then using, which needs change_appetite
    def trait(lo=0.15, hi=0.85, shift=0.0) -> float:
        x = rng.random() * (hi - lo) + lo + shift
        return max(0.05, min(0.95, x))

    change = trait(shift=0.15 if age == 23 else (-0.2 if age == 55 else 0))
    loud = trait(shift=0.1 if seat == "founder" else 0)
    price = trait(shift=0.25 if plan == "developer" or shop == "hobby" else -0.1)
    if shop == "corporate":
        price = trait(shift=-0.15)
    trust = trait(shift=-0.15 if deployment == "self_hosted" else 0.05)
    noise_t = trait(shift=-0.2 if stage == "pissed" else 0)
    loyalty = trait(shift=-0.25 if stage == "gone" else 0.05)

    using = assign_using(
        stage=stage,
        seat=seat,
        shop=shop,
        geo=geo,
        plan=plan,
        tenure=tenure,
        change_appetite=change,
        rng=rng,
    )

    arr = {
        "developer": "0",
        "team": rng.choice(["1k", "10k"]),
        "business": rng.choice(["10k", "50k"]),
        "enterprise": rng.choice(["50k", "150k_plus"]),
    }[plan]

    hygiene = "current"
    if age == 55 or deployment == "self_hosted":
        hygiene = rng.choice(["one_behind", "pinned_old", "pinned_old"])
    elif rng.random() < 0.25:
        hygiene = "one_behind"

    noise = "low"
    if stage == "pissed":
        noise = rng.choice(["moderate", "drowning", "drowning"])
    elif rng.random() < 0.35:
        noise = "moderate"

    competitive = "sentry_only"
    if stage == "gone":
        competitive = rng.choice(["evaluating_exit", "also_datadog", "also_newrelic"])
    elif rng.random() < 0.18:
        competitive = rng.choice(["also_datadog", "also_newrelic", "self_rolled"])

    residency = "eu" if geo == "europe" else ("us" if rng.random() < 0.75 else "eu")
    if geo == "india":
        residency = "us"

    memory = []
    if stage == "gone":
        memory.append(
            {
                "at": "2025-11-01T00:00:00Z",
                "kind": "price",
                "target": "quotas",
                "remember": True,
                "camp": "leaving",
                "quote": "The bill jumped. We left.",
            }
        )

    renewal = None if plan == "developer" else rng.randint(10, 340)

    person = {
        "id": uuid.uuid4().hex[:12],
        "schema_version": 3,
        "display_name": "",
        "origin": "",
        "voice": "",
        "human": {
            "age": age,
            "seniority": seniority,
            "education": education,
            "geo": geo,
            "shop": shop,
            "frameworks": [framework],
            "seat": seat,
        },
        "sentry": {
            "plan": plan,
            "motion": motion,
            "deployment": deployment,
            "tenure_months": tenure,
            "renewal_in_days": renewal,
            "arr_band": arr,
            "quota_posture": quota_posture,
            "competitive_frame": competitive,
            "platforms": list(FRAMEWORK_PLATFORMS[framework]),
            "sdk_hygiene": hygiene,
            "using": using,
            "alert_noise": noise,
            "data_residency": residency,
        },
        "temperament": {
            "noise_tolerance": round(noise_t, 3),
            "price_sensitivity": round(price, 3),
            "change_appetite": round(change, 3),
            "trust": round(trust, 3),
            "loud": round(loud, 3),
            "loyalty": round(loyalty, 3),
        },
        "life": {
            "stage": stage,
            "sentiment": round(
                {"trying": 0.2, "in": 0.35, "pissed": -0.55, "gone": -0.8}[stage]
                + rng.uniform(-0.15, 0.15),
                3,
            ),
            "usage": round(
                {"trying": 0.15, "in": 0.6, "pissed": 0.45, "gone": 0.0}[stage],
                3,
            ),
            "memory": memory,
        },
    }
    return person


def _overflow_key(p: dict, dim: str):
    if dim == "framework":
        return p["human"]["frameworks"][0]
    if dim in ("geo", "shop", "seat", "age"):
        return p["human"][dim]
    if dim == "plan":
        return p["sentry"]["plan"]
    if dim == "stage":
        return p["life"]["stage"]
    raise KeyError(dim)


def hatch(census: dict | None = None, *, seed: int = 1, n: int | None = None) -> list[dict]:
    census = census or load_census()
    n = n or int(census["n"])
    rng = Random(seed)
    quotas = census["_quotas"]
    filled = {dim: defaultdict(int) for dim in OVERFLOW_DIMS}
    people: list[dict] = []
    taken_names: set[str] = set()
    stuck = 0
    max_stuck = 40_000

    while len(people) < n:
        p = propose(rng, census, filled)
        why = reject_reason(p)
        if why:
            stuck += 1
            if stuck > max_stuck:
                raise RuntimeError(f"hatch stuck on reject={why} at {len(people)}/{n}")
            continue
        enforce_overflow = stuck <= 8_000
        blocked = False
        if enforce_overflow:
            for dim in OVERFLOW_DIMS:
                val = _overflow_key(p, dim)
                if val not in quotas[dim]:
                    continue
                if not remaining_ok(filled, quotas, dim, val):
                    blocked = True
                    break
        if blocked:
            stuck += 1
            if stuck > max_stuck:
                raise RuntimeError(f"hatch stuck on overflow at {len(people)}/{n}")
            continue
        p["display_name"] = name_for(p["human"]["geo"], rng, taken_names)
        p["origin"] = origin_for(p, rng)
        p["voice"] = compile_voice(p)
        p["_x"], p["_y"] = place_stable(LIFE, p["life"]["stage"], p["id"])
        people.append(p)
        for dim in OVERFLOW_DIMS:
            val = _overflow_key(p, dim)
            filled[dim][val] += 1
        stuck = 0
    return people

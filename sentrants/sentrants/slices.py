from __future__ import annotations

from collections.abc import Callable

Person = dict
Pred = Callable[[Person], bool]


def H(p: Person) -> dict:
    return p["human"]


def S(p: Person) -> dict:
    return p["sentry"]


def L(p: Person) -> dict:
    return p["life"]


def fw(p: Person) -> str:
    return H(p)["frameworks"][0]


def seer_caps(p: Person) -> list[str]:
    return [c for c in S(p)["using"]["capabilities"] if c.startswith("seer.")]


def js(p: Person) -> bool:
    return fw(p) in ("react", "next", "vue", "express")


def python(p: Person) -> bool:
    return fw(p) in ("django", "fastapi", "flask")


def mobile(p: Person) -> bool:
    plats = S(p)["platforms"]
    return fw(p) == "flutter" or any(x in plats for x in ("ios", "android", "react_native"))


# --- covering map: geo × shop, disjoint, should sum to ~100% ---

COVERING: list[tuple[str, str, Pred]] = [
    ("us_startup", "US startup", lambda p: H(p)["geo"] == "us" and H(p)["shop"] == "startup"),
    ("us_corporate", "US corporate", lambda p: H(p)["geo"] == "us" and H(p)["shop"] == "corporate"),
    ("us_hobby", "US hobby", lambda p: H(p)["geo"] == "us" and H(p)["shop"] == "hobby"),
    ("us_agency", "US agency", lambda p: H(p)["geo"] == "us" and H(p)["shop"] == "agency"),
    ("india_corporate", "Corporate India", lambda p: H(p)["geo"] == "india" and H(p)["shop"] == "corporate"),
    ("india_startup", "India startup", lambda p: H(p)["geo"] == "india" and H(p)["shop"] == "startup"),
    ("india_other", "India agency/hobby", lambda p: H(p)["geo"] == "india" and H(p)["shop"] in ("agency", "hobby")),
    ("eu_startup", "Europe startup", lambda p: H(p)["geo"] == "europe" and H(p)["shop"] == "startup"),
    ("eu_corporate", "Europe corporate", lambda p: H(p)["geo"] == "europe" and H(p)["shop"] == "corporate"),
    ("eu_other", "Europe agency/hobby", lambda p: H(p)["geo"] == "europe" and H(p)["shop"] in ("agency", "hobby")),
    ("latam", "LatAm", lambda p: H(p)["geo"] == "latam"),
    ("east_asia", "East Asia", lambda p: H(p)["geo"] == "east_asia"),
]


# --- callouts: the joints a Sentry person actually names ---
# Overlap is the point. A US founder 23 also sits in US startup.

CALLOUTS: list[tuple[str, str, Pred]] = [
    (
        "us_founder_23",
        "US founder, 23",
        lambda p: H(p)["seat"] == "founder" and H(p)["geo"] == "us" and H(p)["age"] == 23,
    ),
    (
        "us_founder_30",
        "US founder, 30",
        lambda p: H(p)["seat"] == "founder" and H(p)["geo"] == "us" and H(p)["age"] == 30,
    ),
    (
        "us_founder",
        "US founder (any age)",
        lambda p: H(p)["seat"] == "founder" and H(p)["geo"] == "us",
    ),
    (
        "us_startup_ic_23_js",
        "US startup IC, 23, JS/Next",
        lambda p: H(p)["geo"] == "us"
        and H(p)["shop"] == "startup"
        and H(p)["seat"] == "coder"
        and H(p)["age"] == 23
        and js(p),
    ),
    (
        "us_startup_ic",
        "US startup IC",
        lambda p: H(p)["geo"] == "us" and H(p)["shop"] == "startup" and H(p)["seat"] == "coder",
    ),
    (
        "us_corp_boss",
        "US corporate boss",
        lambda p: H(p)["geo"] == "us" and H(p)["shop"] == "corporate" and H(p)["seat"] == "boss",
    ),
    (
        "us_corp_ic",
        "US corporate IC",
        lambda p: H(p)["geo"] == "us" and H(p)["shop"] == "corporate" and H(p)["seat"] == "coder",
    ),
    (
        "bootcamp_23",
        "23, bootcamp",
        lambda p: H(p)["age"] == 23 and H(p)["education"] == "bootcamp",
    ),
    (
        "india_corp_ic",
        "Corporate India IC",
        lambda p: H(p)["geo"] == "india" and H(p)["shop"] == "corporate" and H(p)["seat"] == "coder",
    ),
    (
        "india_corp_spring",
        "Corporate India, Spring",
        lambda p: H(p)["geo"] == "india" and H(p)["shop"] == "corporate" and fw(p) == "spring",
    ),
    (
        "india_corp_boss",
        "Corporate India boss",
        lambda p: H(p)["geo"] == "india" and H(p)["shop"] == "corporate" and H(p)["seat"] == "boss",
    ),
    (
        "eu_self_hosted",
        "Europe, self-hosted",
        lambda p: H(p)["geo"] == "europe" and S(p)["deployment"] == "self_hosted",
    ),
    (
        "self_hosted",
        "Self-hosted (any)",
        lambda p: S(p)["deployment"] == "self_hosted",
    ),
    (
        "rails_old_hand",
        "Rails, 40 or 55",
        lambda p: fw(p) == "rails" and H(p)["age"] in (40, 55),
    ),
    (
        "python_backend",
        "Python (Django / FastAPI / Flask)",
        python,
    ),
    (
        "next_trying",
        "Next.js, still trying",
        lambda p: fw(p) == "next" and L(p)["stage"] == "trying",
    ),
    ("mobile", "Mobile (Flutter / iOS / Android)", mobile),
    ("unity", "Unity", lambda p: fw(p) == "unity"),
    ("laravel", "Laravel", lambda p: fw(p) == "laravel"),
    ("agency", "Agency", lambda p: H(p)["shop"] == "agency"),
    (
        "enterprise",
        "Enterprise plan",
        lambda p: S(p)["plan"] == "enterprise",
    ),
    (
        "sales_assisted",
        "Sales-assisted",
        lambda p: S(p)["motion"] == "sales_assisted",
    ),
    (
        "near_quota",
        "Near quota or spiked",
        lambda p: S(p)["quota_posture"] in ("near_limit", "spiked_recently"),
    ),
    (
        "seer_mcp",
        "Has Seer MCP",
        lambda p: "seer.mcp" in S(p)["using"]["capabilities"],
    ),
    (
        "seer_any",
        "Any Seer capability",
        lambda p: bool(seer_caps(p)),
    ),
    (
        "errors_only_trying",
        "Trying, errors only",
        lambda p: L(p)["stage"] == "trying" and S(p)["using"]["signals"] == ["errors"],
    ),
    ("pissed", "Pissed", lambda p: L(p)["stage"] == "pissed"),
    ("gone", "Gone", lambda p: L(p)["stage"] == "gone"),
    (
        "evaluating_exit",
        "Evaluating exit / already shopping",
        lambda p: S(p)["competitive_frame"] in ("evaluating_exit", "also_datadog", "also_newrelic"),
    ),
]


def _tally(people: list[Person], specs: list[tuple[str, str, Pred]]) -> list[tuple[str, str, int, float]]:
    n = len(people) or 1
    rows = []
    for sid, label, pred in specs:
        c = sum(1 for p in people if pred(p))
        rows.append((sid, label, c, 100.0 * c / n))
    return rows


def covering_report(people: list[Person]) -> str:
    n = len(people)
    rows = _tally(people, COVERING)
    covered = sum(
        1 for p in people if any(pred(p) for _, _, pred in COVERING)
    )
    lines = [
        f"covering map  (geo × shop, disjoint)   n={n}   union={covered} ({100.0 * covered / n:.1f}%)",
        f"  {'slice':<22} {'n':>5}  {'%':>6}",
    ]
    for sid, label, c, pct in rows:
        lines.append(f"  {label:<22} {c:5}  {pct:5.1f}%")
    total = sum(c for *_, c, _ in rows)
    lines.append(f"  {'(sum)':<22} {total:5}  {100.0 * total / n:5.1f}%")
    return "\n".join(lines)


def callouts_report(people: list[Person]) -> str:
    n = len(people)
    rows = _tally(people, CALLOUTS)
    lines = [
        "callouts  (joints — they overlap, that's the point)",
        f"  {'slice':<36} {'n':>5}  {'%':>6}",
    ]
    for sid, label, c, pct in sorted(rows, key=lambda r: -r[2]):
        lines.append(f"  {label:<36} {c:5}  {pct:5.1f}%")
    return "\n".join(lines)


def slices_report(people: list[Person]) -> str:
    return covering_report(people) + "\n\n" + callouts_report(people)

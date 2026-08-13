from __future__ import annotations

from random import Random

FIRST = {
    "us": [
        "Matt", "Maya", "Jordan", "Chris", "Alex", "Sam", "Riley", "Taylor",
        "Priya", "Luis", "Keisha", "Noah", "Emma", "Dev", "Avery",
    ],
    "europe": [
        "Łukasz", "Nina", "Jonas", "Claire", "Marta", "Felix", "Siobhan",
        "Hugo", "Ines", "Tomas", "Greta", "Omar", "Anika", "Piotr",
    ],
    "india": [
        "Priya", "Radhika", "Arjun", "Neha", "Rahul", "Ananya", "Vikram",
        "Sana", "Karthik", "Meera", "Aditya", "Isha", "Rohan", "Divya",
    ],
    "latam": [
        "Diego", "Camila", "Mateo", "Valentina", "Lucas", "Sofia", "João",
        "Lucia", "Andres", "Mariana", "Felipe", "Ana",
    ],
    "east_asia": [
        "Yuki", "Min", "Wei", "Hana", "Kenji", "Soo", "Mei", "Hiro",
        "Jin", "Aya", "Chen", "Nari",
    ],
}

LAST = {
    "us": [
        "Chen", "Patel", "Nguyen", "Brooks", "Garcia", "Kim", "Walsh",
        "Johnson", "Reed", "Singh", "Martinez", "Cole",
    ],
    "europe": [
        "Kowalski", "Berg", "Rossi", "Novak", "Weber", "O'Neill", "Dumont",
        "Silva", "Nagy", "Andersen",
    ],
    "india": [
        "Sharma", "Iyer", "Nair", "Gupta", "Reddy", "Khan", "Banerjee",
        "Mehta", "Pillai", "Desai",
    ],
    "latam": [
        "Silva", "Garcia", "Santos", "Lopez", "Costa", "Fernandez", "Rojas",
    ],
    "east_asia": [
        "Park", "Tanaka", "Wang", "Sato", "Kim", "Lin", "Nakamura", "Choi",
    ],
}


def name_for(geo: str, rng: Random, taken: set[str]) -> str:
    first = rng.choice(FIRST[geo])
    last = rng.choice(LAST[geo])
    base = f"{first} {last}"
    name = base
    i = 2
    while name in taken:
        name = f"{base} {i}"
        i += 1
    taken.add(name)
    return name


def compile_voice(p: dict) -> str:
    h, s, t, life = p["human"], p["sentry"], p["temperament"], p["life"]
    loud = "loud" if t["loud"] > 0.6 else "quiet"
    change = "hates change" if t["change_appetite"] < 0.35 else (
        "will try new things" if t["change_appetite"] > 0.65 else "careful about change"
    )
    price = "hates the bill" if t["price_sensitivity"] > 0.65 else (
        "doesn't look at invoices" if t["price_sensitivity"] < 0.35 else "notices price"
    )
    noise = "drowning in alerts" if s["alert_noise"] == "drowning" or t["noise_tolerance"] < 0.3 else (
        "can live with noise" if t["noise_tolerance"] > 0.7 else "picky about noise"
    )
    fw = ", ".join(h["frameworks"])
    using = ", ".join(s["using"]["signals"] + s["using"]["capabilities"][:4]) or "almost nothing"
    grain = "Speak short."
    if h["geo"] == "india" and h["shop"] == "corporate":
        grain += " Process matters. You review other people's work."
    if h["seat"] == "founder":
        grain += " It's your money and your product."
    if h["age"] == 23:
        grain += " Casual. You found Sentry on Twitter or a bootcamp friend."
    if h["age"] == 55:
        grain += " You've seen vendors come and go. Don't sell you."
    return (
        f"You are {p['display_name']}, {h['age']}, {h['seat']}, {h['shop']} in {h['geo']}, {fw}. "
        f"Plan: {s['plan']}. Using: {using}. Stage: {life['stage']}. "
        f"{loud}, {change}, {price}, {noise}. {grain}"
    )


ORIGINS = [
    "Stuck Sentry on a {fw} app {when} because {why}.",
    "A teammate added it. {when} I was the one who actually opened it.",
    "We were drowning. {why}. Sentry was the first thing that grouped it.",
    "Copied the wizard into {fw} {when}. Didn't think about it again until it paged me.",
    "Tried Datadog, kept Sentry for the stack traces. {when}.",
]


WHENS = {
    "trying": ["last month", "two weeks ago", "this sprint"],
    "in": ["a year ago", "three years back", "after the last big outage"],
    "pissed": ["ages ago — before they changed the bill", "back when it was simple"],
    "gone": ["years ago", "in another job, then we brought it here, then we left"],
}

WHYS = [
    "prod was 500ing on a Friday",
    "the mobile crash rate went stupid",
    "nobody could repro the bug",
    "PagerDuty was a joke without a stack trace",
    "Twitter said so",
    "the last shop used it",
]


def origin_for(p: dict, rng: Random) -> str:
    fw = p["human"]["frameworks"][0]
    stage = p["life"]["stage"]
    tmpl = rng.choice(ORIGINS)
    return tmpl.format(fw=fw, when=rng.choice(WHENS[stage]), why=rng.choice(WHYS))

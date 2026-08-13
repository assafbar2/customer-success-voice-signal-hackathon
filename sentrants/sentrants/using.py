from __future__ import annotations

from random import Random

FRAMEWORK_PLATFORMS = {
    "react": ["javascript"],
    "next": ["javascript", "nextjs"],
    "vue": ["javascript"],
    "django": ["python"],
    "fastapi": ["python"],
    "flask": ["python"],
    "rails": ["ruby"],
    "laravel": ["php"],
    "spring": ["java"],
    "express": ["javascript"],
    "flutter": ["ios", "android"],
    "unity": ["unity"],
}


def assign_using(
    *,
    stage: str,
    seat: str,
    shop: str,
    geo: str,
    plan: str,
    tenure: int,
    change_appetite: float,
    rng: Random,
) -> dict:
    signals = ["errors"]
    caps = ["issues"]

    if stage == "trying":
        return {"signals": signals, "capabilities": caps}

    paying = plan in ("team", "business", "enterprise")
    if paying and rng.random() < 0.75:
        signals.append("spans")
    if paying and rng.random() < 0.35:
        signals.append("logs")
    if paying and rng.random() < 0.55:
        caps.append("alerts.slack")
    if seat == "boss" and paying and rng.random() < 0.45:
        caps.append("alerts.pagerduty")
        caps.append("releases")
    if seat == "founder" and paying and rng.random() < 0.3:
        caps.append("releases")

    india_corp = geo == "india" and shop == "corporate"
    if paying and not india_corp and rng.random() < 0.22:
        signals.append("replay.web")

    if (
        stage == "in"
        and seat == "coder"
        and paying
        and tenure >= 4
        and change_appetite > 0.4
    ):
        if rng.random() < 0.4:
            caps.append("seer.explain")
        if rng.random() < 0.22:
            caps.append("seer.mcp")
        if rng.random() < 0.12:
            caps.append("seer.autofix")

    if stage == "gone":
        # they had a real setup, then left
        if "spans" not in signals and rng.random() < 0.6:
            signals.append("spans")
        if rng.random() < 0.4:
            caps.append("alerts.slack")

    # unique, stable order
    def uniq(xs: list[str]) -> list[str]:
        seen = []
        for x in xs:
            if x not in seen:
                seen.append(x)
        return seen

    return {"signals": uniq(signals), "capabilities": uniq(caps)}

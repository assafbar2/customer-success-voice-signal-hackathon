from __future__ import annotations


def reject_reason(p: dict) -> str | None:
    h = p["human"]
    s = p["sentry"]
    life = p["life"]
    age, seat, shop, seniority, education = (
        h["age"],
        h["seat"],
        h["shop"],
        h["seniority"],
        h["education"],
    )
    if age == 23 and seat == "boss":
        return "23-boss"
    if age == 23 and seniority == "staff":
        return "23-staff"
    if age == 55 and seniority == "junior" and education == "bootcamp":
        return "55-junior-bootcamp"
    if seat == "founder" and shop == "corporate":
        return "founder-corporate"
    if seat == "founder" and seniority == "junior":
        return "founder-junior"
    if life["stage"] == "trying" and s["tenure_months"] > 10:
        return "trying-old"
    if life["stage"] == "trying" and s["plan"] == "enterprise":
        return "trying-enterprise"
    if s["deployment"] == "self_hosted" and s["plan"] == "developer":
        return "self-hosted-free"
    using = s["using"]
    if "seer.mcp" in using["capabilities"] and shop == "hobby" and s["tenure_months"] < 2:
        return "mcp-hobby-new"
    if (
        "replay.web" in using["signals"]
        and h["geo"] == "india"
        and shop == "corporate"
    ):
        return "replay-india-corporate"
    if life["stage"] == "gone" and not life["memory"]:
        return "gone-no-memory"
    return None

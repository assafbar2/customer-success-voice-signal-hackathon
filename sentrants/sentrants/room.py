from __future__ import annotations

from collections import defaultdict

LINES = {
    "yes_leave_it": [
        "Leave it on. I want the PR.",
        "If it saves me a Friday, yes.",
        "Ship it. I'll revert if it's dumb.",
    ],
    "yes_but_manual": [
        "Fine if I click it. Not auto.",
        "I want the draft. I don't want it in main.",
        "Manual only. This is still my repo.",
    ],
    "hell_no": [
        "Not in my repo.",
        "Who turned this on.",
        "I review code. It doesn't open PRs.",
        "Process exists for a reason.",
    ],
    "not_me": [
        "I don't use Seer.",
        "Not my stack.",
        "I just wanted errors.",
        "Self-hosted. We were up.",
        "We left. Not my outage.",
    ],
    "leaving": [
        "I'm done.",
        "This is how we leave.",
        "We'll look at Datadog.",
    ],
    "wait_it_out": [
        "Status page says 90 minutes. I'm waiting.",
        "It'll come back. It always does.",
        "Don't tweet. Just wait.",
    ],
    "we_were_blind": [
        "Prod is on fire and I can't see it.",
        "Ninety minutes with no issues. That's the issue.",
        "We flew blind the whole morning.",
    ],
    "also_datadog": [
        "This is why we still pay Datadog.",
        "Dual-run exists for mornings like this.",
        "Sentry's dark. The other one isn't.",
    ],
    "trying": ["Still figuring it out.", "It's on. I haven't opened it much."],
    "in": ["This is how we debug.", "Don't break the SDK."],
    "pissed": ["The bill. The noise. Pick one.", "Fix the quota email."],
    "gone": ["We left.", "Not my problem anymore."],
}


def _diversify(group: list[dict], n: int) -> list[dict]:
    by_geo: dict[str, list] = defaultdict(list)
    for p in sorted(group, key=lambda x: x["id"]):
        by_geo[p["human"]["geo"]].append(p)
    out: list[dict] = []
    geos = list(by_geo)
    i = 0
    while len(out) < n and geos:
        geo = geos[i % len(geos)]
        if by_geo[geo]:
            out.append(by_geo[geo].pop(0))
        else:
            geos.remove(geo)
            if not geos:
                break
            continue
        i += 1
    return out


def template_line(p: dict) -> str:
    camp = p.get("_camp") or p["life"]["stage"]
    lines = LINES.get(camp, ["…"])
    idx = int(p["id"], 16) % len(lines) if p["id"] else 0
    return lines[idx]


def room_talk(people: list[dict], *, per_camp: int = 10, max_n: int = 60) -> list[dict]:
    """After a walk: ~60 one-liners, stratified by camp × geo. One batch, not 2000 mouths.

    v1 uses compiled templates. Same pick + write-back as a later LLM batch.
    """
    by_camp: dict[str, list] = defaultdict(list)
    for p in people:
        by_camp[p.get("_camp") or p["life"]["stage"]].append(p)
    picked: list[dict] = []
    for group in by_camp.values():
        picked.extend(_diversify(group, per_camp))
    picked = picked[:max_n]
    quotes = []
    for p in picked:
        line = template_line(p)
        p["_quote"] = line
        p["life"]["last_quote"] = line
        quotes.append(
            {
                "id": p["id"],
                "name": p["display_name"],
                "camp": p.get("_camp") or p["life"]["stage"],
                "geo": p["human"]["geo"],
                "shop": p["human"]["shop"],
                "seat": p["human"]["seat"],
                "text": line,
            }
        )
    return quotes

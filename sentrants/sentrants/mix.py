from __future__ import annotations

from collections import Counter, defaultdict

from sentrants.slices import slices_report


def mix_report(people: list[dict]) -> str:
    n = len(people)
    lines = [f"n = {n}", ""]

    def col(title: str, xs: list):
        c = Counter(xs)
        lines.append(title)
        for k, v in c.most_common():
            lines.append(f"  {k:22} {v:5}  {100.0 * v / n:5.1f}%")
        lines.append("")

    col("stage", [p["life"]["stage"] for p in people])
    col("geo", [p["human"]["geo"] for p in people])
    col("shop", [p["human"]["shop"] for p in people])
    col("seat", [p["human"]["seat"] for p in people])
    col("age", [p["human"]["age"] for p in people])
    col("plan", [p["sentry"]["plan"] for p in people])
    col("framework", [p["human"]["frameworks"][0] for p in people])

    lines.append("geo × shop  (corporate India should be a crowd)")
    grid = defaultdict(int)
    for p in people:
        grid[(p["human"]["geo"], p["human"]["shop"])] += 1
    for (geo, shop), v in sorted(grid.items(), key=lambda kv: -kv[1])[:18]:
        lines.append(f"  {geo:12} {shop:12} {v:5}  {100.0 * v / n:5.1f}%")
    lines.append("")

    india_corp = sum(
        1
        for p in people
        if p["human"]["geo"] == "india" and p["human"]["shop"] == "corporate"
    )
    lines.append(f"india × corporate = {india_corp}  ({100.0 * india_corp / n:.1f}%)")
    seer_mcp = sum(
        1 for p in people if "seer.mcp" in p["sentry"]["using"]["capabilities"]
    )
    lines.append(f"using seer.mcp    = {seer_mcp}  ({100.0 * seer_mcp / n:.1f}%)")
    lines.append("")
    lines.append(slices_report(people))
    return "\n".join(lines)

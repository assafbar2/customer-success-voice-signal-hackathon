from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CENSUS = ROOT / "schema" / "census.example.yaml"

INT_KEYS = {"age"}


def load_census(path: Path | None = None) -> dict:
    raw = yaml.safe_load((path or DEFAULT_CENSUS).read_text())
    n = int(raw["n"])
    quotas: dict[str, dict] = {}
    skip = {"n", "schema_version", "note", "primary_platform", "data_residency"}
    for key, val in raw.items():
        if key in skip or not isinstance(val, dict):
            continue
        parsed = {}
        for k, pct in val.items():
            parsed[int(k) if key in INT_KEYS else str(k)] = float(pct)
        quotas[key] = integer_quotas(parsed, n)
    raw["_quotas"] = quotas
    raw["_path"] = str(path or DEFAULT_CENSUS)
    return raw


def integer_quotas(pcts: dict, n: int) -> dict:
    """Largest-remainder so counts sum to n."""
    items = list(pcts.items())
    exact = [(k, pcts[k] / 100.0 * n) for k, _ in items]
    floored = [(k, int(v), v - int(v)) for k, v in exact]
    total = sum(f for _, f, _ in floored)
    need = n - total
    floored.sort(key=lambda t: t[2], reverse=True)
    counts = {k: f for k, f, _ in floored}
    for i in range(need):
        counts[floored[i % len(floored)][0]] += 1
    return counts


def remaining_ok(filled: dict, quotas: dict, dim: str, value) -> bool:
    q = quotas[dim][value]
    return filled[dim].get(value, 0) < q

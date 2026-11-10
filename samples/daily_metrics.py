#!/usr/bin/env python3
"""Script-first daily metrics: week-over-week change, staleness and 'what moved' (excerpt, no AI call).

Design: every metric carries value, prior, source file, as-of time and an age limit. A metric older
than its limit is reported as 'stale', a missing one as 'missing'. The digest is built by this
script; a model is only used on top of it when someone asks for commentary.
Run the self-test:  python3 daily_metrics.py
"""
import datetime as dt


def wow(value, prior):
    """Percent change vs the prior week; None when it cannot be computed honestly."""
    if value is None or prior in (None, 0):
        return None
    return round((value - prior) / abs(prior) * 100, 1)


def status_for(age_h, max_age_h, value):
    if value is None:
        return "missing"
    return "stale" if age_h is None or age_h > max_age_h else "ok"


def pick_prior(rows, as_of, days=7, tol=2):
    """Row whose date is closest to as_of - days (within tol days), else None."""
    target = as_of - dt.timedelta(days=days)
    best = None
    for r in rows:
        gap = abs((r["date"] - target).days)
        if gap <= tol and (best is None or gap < best[0]):
            best = (gap, r)
    return best[1] if best else None


def moved(metrics, threshold=15, min_base=10):
    """Largest movers: |WoW| >= threshold and a prior value big enough to mean something."""
    hit = [m for m in metrics if m.get("wow_pct") is not None
           and abs(m["wow_pct"]) >= threshold and (m.get("prior") or 0) >= min_base]
    return sorted(hit, key=lambda m: -abs(m["wow_pct"]))[:6]


if __name__ == "__main__":
    assert wow(903595, 540823) == 67.1
    assert wow(5, 0) is None and wow(None, 3) is None
    assert status_for(14.6, 36, 5) == "ok" and status_for(40, 36, 5) == "stale" and status_for(1, 36, None) == "missing"
    rows = [{"date": dt.date(2026, 11, 3), "v": 1}, {"date": dt.date(2026, 11, 4), "v": 2}]
    assert pick_prior(rows, dt.date(2026, 11, 10))["v"] == 1
    assert pick_prior(rows, dt.date(2026, 11, 30)) is None
    ms = [{"id": "a", "wow_pct": 80.0, "prior": 100}, {"id": "b", "wow_pct": 5.0, "prior": 100}, {"id": "c", "wow_pct": 90.0, "prior": 2}]
    assert [m["id"] for m in moved(ms)] == ["a"]
    print("daily_metrics: 8 checks passed")

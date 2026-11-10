#!/usr/bin/env python3
"""Seat dispatch with quota fallback and a usage guard (simplified from the studio's dispatch.sh).

Idea: every studio role ("seat") is assigned to one agent harness (a CLI such as Codex,
Hermes or Grok). A seat has one fallback. The dispatcher
  1. skips the primary and goes straight to the fallback when a usage guard says the primary's
     quota pool is running hot (and the role is not exempt),
  2. otherwise runs the primary; on a quota error (exit 429) or any failure it runs the fallback ONCE,
  3. appends one JSON line per attempt to a run log, so seat changes are backed by evidence.
Adapters are injected as callables, so the logic is testable without any CLI.
Run the self-test:  python3 dispatch_fallback.py
"""
import json
import time

SEATS = {
    "writer":   {"harness": "codex",  "fallback": {"harness": "primary"}},
    "critic":   {"harness": "primary", "fallback": {"harness": "codex"}},
    "animator": {"harness": "primary", "fallback": {"harness": "codex"}},
}
GUARD_EXEMPT = {"critic", "reviewer"}   # cheap read-only roles may keep using the hot pool
GUARD_PCT = 50.0


def dispatch(role, prompt, adapters, usage_pct=None, force_seat=False, log=None):
    seat = SEATS[role]
    fb = seat.get("fallback")
    attempts = []

    def run(harness, attempt, guard=None):
        t0 = time.time()
        code, out = adapters[harness](prompt)
        rec = {"role": role, "harness": harness, "attempt": attempt, "exit": code,
               "ok": code == 0 and bool(out), "wall_s": round(time.time() - t0, 3),
               "incident": "quota" if code == 429 else (None if code == 0 else "fail")}
        if guard:
            rec["guard"] = guard
        attempts.append(rec)
        if log is not None:
            log.append(json.dumps(rec))
        return rec, out

    hot = (usage_pct is not None and usage_pct >= GUARD_PCT and seat["harness"] == "primary"
           and role not in GUARD_EXEMPT and fb and fb["harness"] != "primary" and not force_seat)
    if hot:                                         # usage guard: route around the busy pool
        rec, out = run(fb["harness"], "guard", guard="primary_usage")
        return rec["ok"], out, attempts
    rec, out = run(seat["harness"], "primary")
    if not rec["ok"] and fb:                        # one fallback, never a loop
        rec, out = run(fb["harness"], "fallback")
    return rec["ok"], out, attempts


if __name__ == "__main__":
    ok = lambda p: (0, "done")
    quota = lambda p: (429, "")
    # 1. primary works -> one attempt
    r = dispatch("writer", "x", {"codex": ok, "primary": ok})
    assert r[0] and [a["attempt"] for a in r[2]] == ["primary"]
    # 2. primary hits quota -> fallback runs once
    r = dispatch("writer", "x", {"codex": quota, "primary": ok})
    assert r[0] and [a["attempt"] for a in r[2]] == ["primary", "fallback"] and r[2][0]["incident"] == "quota"
    # 3. both fail -> reported failure, still only two attempts
    r = dispatch("writer", "x", {"codex": quota, "primary": quota})
    assert not r[0] and len(r[2]) == 2
    # 4. guard: primary pool at 54 % -> animator goes straight to codex; critic is exempt
    r = dispatch("animator", "x", {"primary": ok, "codex": ok}, usage_pct=54)
    assert [a["harness"] for a in r[2]] == ["codex"] and r[2][0]["guard"] == "primary_usage"
    r = dispatch("critic", "x", {"primary": ok, "codex": ok}, usage_pct=54)
    assert [a["harness"] for a in r[2]] == ["primary"]
    print("dispatch_fallback: 5 checks passed")

#!/usr/bin/env python3
"""Evidence-only publishing gate: pure checks (excerpted and simplified from the studio's autopost gate).

Principle: the gate never publishes and never trusts a claim. Each check passes only when a file or
number proves it, and "not evidenced" is a FAIL, not a warning. This excerpt keeps the parts that
do not need media files: format status lookup, sourced-facts table, cover wording, originality share.
Run the self-test:  python3 evidence_gate.py
"""
import re

OWN_MIN = 20.0   # minimum share (%) of the picture that is our own work


def parse_formats(text):
    """formats.yaml -> {format_id: status}; only 'proven' formats may be posted without a human."""
    out, cur = {}, None
    for line in text.splitlines():
        m = re.match(r'^\s*-\s*id:\s*["\']?([^\s"\'#]+)', line)
        if m:
            cur = m.group(1)
            continue
        m = re.match(r'^\s*status:\s*["\']?([^\s"\'#]+)', line)
        if m and cur:
            out[cur] = m.group(1)
    return out


def facts_check(table):
    """Every numbered row of the facts table must end in a source (URL, path or quoted title)."""
    rows = re.findall(r'^\s*\|\s*\d+\s*\|.*$', table, re.M)
    if not rows:
        return False, "facts table not evidenced"
    for row in rows:
        cols = row.strip().strip('|').split('|')
        if not re.search(r'https?://|[\w.-]+/[\w./-]+|"[^"]+"', cols[-1]):
            return False, "fact %s has no source" % cols[0].strip()
    return True, "%d facts, all sourced" % len(rows)


def cover_check(text):
    """Cover must be plain words (>= 3) and not a bare metric like '40 KM'."""
    if not text or len(re.findall(r'\w+', text)) < 3:
        return False, "cover has fewer than 3 words"
    metric = re.search(r'\b\d+(?:\.\d+)?\s*(?:km|m|kg|ft|%)', text, re.I)
    subject = re.search(r'\b(?:temples?|map|festival|places|stays)\b', text, re.I)
    if metric and not subject:
        return False, "abstract metric cover: " + text
    return True, text


def originality_check(own_pct, has_own_script, has_credits):
    problems = []
    if own_pct is None or not 0 <= own_pct <= 100:
        return False, "own share not evidenced"
    if own_pct < OWN_MIN:
        problems.append("own %.0f %% < %.0f" % (own_pct, OWN_MIN))
    if not has_own_script:
        problems.append("own script not evidenced")
    if own_pct < 100 and not has_credits:
        problems.append("credits not evidenced")
    return (not problems), "; ".join(problems) or "ok"


if __name__ == "__main__":
    assert parse_formats('- id: "a"\n  status: proven\n- id: b\n  status: unproven') == {"a": "proven", "b": "unproven"}
    assert facts_check("| 1 | Hill is 800 m | https://example.org/x |")[0]
    assert not facts_check("| 1 | Hill is 800 m | I remember it |")[0]
    assert not facts_check("no table here")[0]
    assert not cover_check("ONE FLAME / 40 KM")[0]
    assert cover_check("5 temples, 1 map")[0]
    assert originality_check(41, True, True)[0]
    assert not originality_check(12, True, True)[0]
    assert not originality_check(None, True, True)[0]
    print("evidence_gate: 8 checks passed")

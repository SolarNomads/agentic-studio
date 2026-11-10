# X engagement loop: scout, draft, validate, gate, evaluate

[Back to overview](../README.md)

## Problem
Replying on X by hand does not scale, and unattended automation produces low-quality noise. The question: can an agent loop do the legwork while deterministic checks hold the quality bar, and can it be made to prove its value or be switched off?

## System built (design and tooling)
1. **Scout:** a research agent with X search returns a batch of targets and drafts as JSON (target post, author size band, topic, why, draft of at most 240 characters, sources).
2. **Validate (`ingest.py`):** everything the scout returns is treated as untrusted data. Schema check, https and host check, injection scan, link resolution; bad items are dropped, never repaired.
3. **Quality bar:** a draft must add one of: a fact, a tool, a number, a correction with its source, or one genuine question; no claim without a source opened during the run; at most one link, only when asked for alternatives; site mentions rate-limited.
4. **Gate (`cold_gate.py`):** an allowlist of target accounts, daily and hourly caps, quiet hours, and a decision log with scores per draft.
5. **Evaluate (`eval.py`, no AI):** daily, 3-day and weekly reports (25 lines, phone-readable) with a KEEP / CHANGE / STOP verdict from stated thresholds (engagement rate, visits, follower change, no negative signals); a KEEP raises the cap by 2 per day up to a ceiling.
6. **Kill rule:** a single file stops everything. It is created by the evaluator when two consecutive windows are below baseline, on any negative signal, or when caps are exceeded twice in a week, and only a human removes it.

## Evidence (what ran)
- Tests: 17 unit tests for the validator, gate and evaluator pass (run 10 Nov 2026). [E11](../evidence/README.md#e11)
- First gate run, 10 Nov 2026: 6 candidate replies were logged; the gate dropped 5, recorded 1 as a dry run, and 0 were posted. [E15](../evidence/README.md#e15)
- Earlier, a simpler version of the loop ran on the account in late October and early November 2026; I do not claim its results here. No results of this redesigned loop exist yet, which is why the evaluator and kill rule were built first.

## What I would do for a client
Run the loop in draft-only mode for the first days with a human skimming every batch, set the caps and the KEEP/STOP thresholds before the first post, and report the evaluator's verdict weekly. The accounts and the kill file stay under your control.

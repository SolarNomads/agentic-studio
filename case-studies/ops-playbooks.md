# Ops playbooks: one rulebook for every agent tool

[Back to overview](../README.md)

## Problem
Four different agent tools work in the same repository. Each reads different instruction files, forgets between sessions, and tends to improvise. Without one shared rulebook, the same mistake gets made in each tool.

## System built
- **One rules file** (about a dozen short rules plus "where to read first, by task") with a tiny pointer file for each tool, so every tool loads the same rules at start: reading order, "every fact needs a source you opened", "no secrets in chat, files or scripts", "done means verified live", explicit git paths, a report format, and an update loop (when a tool or decision changes, update its file and the resume file).
- **Smoke test for the rules:** a script asks each tool a question whose answer is only in the rules file; all four answered correctly on 9 Nov 2026. [E16](../evidence/README.md#e16)
- **Resume file:** a state file any tool or person reads first to continue the work without re-explaining.
- **Workflow coverage index:** 19 recurring workflows listed with where each is documented; 14 documented, 5 partial (10 Nov 2026). The audit is how the gaps were found.
- **Playbooks:** gates before publish ([sanitized copy](../samples/playbooks/gate-before-publish.md)), deploy cards with rollback ([sanitized copy](../samples/playbooks/deploy-card.md)), UX review, handoff and ship-verify, niche sourcing, quota checks, content formats.
- **Access library (concept):** a private register of every account the team uses (service, owner, login method, where the secret lives) without any secrets in it, so an agent that forgot can find how to reach a service and a human can revoke it. Contents are never published.
- **Briefs for a senior reviewer:** a short template (one decision, numbers and paths, not logs) used only when a judgement call meets written criteria, to keep expensive tokens for decisions.

## Evidence
- Rules smoke test: all four tools correct (9 Nov 2026). [E16](../evidence/README.md#e16)
- Coverage audit: 19 workflows, 14 documented, 5 partial (10 Nov 2026).
- Dispatch log with seat changes tied to benchmark results ([content studio](content-studio.md)). [E9](../evidence/README.md#e9)

## What I would do for a client
Write the rules file first, connect every tool you use to it, add a smoke test, and keep a resume file. Then document each recurring workflow as a playbook and keep a register of access that holds no secrets, so ownership stays with you.

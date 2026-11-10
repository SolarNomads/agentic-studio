# Mission Control: a phone dashboard for an agent team

[Back to overview](../README.md)

## Problem
Once several agents run scheduled jobs across several tools, the owner loses sight of what ran, what it used and what it produced. Chat channels are noisy. The need: one phone-first place to see state and give input, with a control plane that decides what an agent may do before it acts.

## System built
A private dashboard (behind an identity-aware access proxy, not public) served by a small Python app with no build step for the backend and a static front end.
- **Jobs and objects:** projects, tasks, runs and scheduled jobs shown as linked objects, one source of truth per entity, with a logging contract (project, task and session id on every run).
- **Token and spend board:** read-only; joins usage logs with a price catalogue to rank jobs and seats by usage, and shows quota meters. A usage guard in the dispatcher reads the same file ([dispatch sample](../samples/dispatch_fallback.py)).
- **Daily metrics script:** produces a source-labelled digest with week-over-week change, staleness and "what moved", with no AI call ([sample](../samples/daily_metrics.py)).
- **Studio pages:** reel library, calendar, taste labelling page and insights, built on one UI kit.
- **UI kit and automated UX gate:** one token file, shared components and a gallery page; a headless-browser check measures tap-target size, minimum text size, perceptual contrast and overflow at phone width, in light and dark ([contrast sample](../samples/apca_contrast.py)). New pages must pass the gate and a screenshot review.

## Evidence
- The UX gate reports its own failures. First measurement, 9 Nov 2026 (390x844): Today page 36/36 tap targets pass, 9 text nodes under 13 px and 12 below the contrast floor; Jobs page in dark mode 17 nodes below the contrast floor. Those findings became tracked tickets and the kit; this is the loop working, not a clean sheet. [E13](../evidence/README.md#e13)
- Daily metrics script: 12 unit tests pass (run 10 Nov 2026); it generated the 10 Nov digest. [E11](../evidence/README.md#e11)
- Feature tickets ship with live checks (API field, page text, cache-busted asset version), a reviewer pass and a rollback note.
- Not public: the dashboard itself. I can demonstrate it on a screen share.

## What I would do for a client
Skip the dashboard at first. Start with the daily metrics script and a jobs list so the owner can see what ran and what it cost; add pages only when a decision needs them. Build on one component kit with a contrast and tap-target gate from page one, so new screens do not drift.

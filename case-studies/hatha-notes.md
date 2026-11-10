# Hatha Notes: offline-first notes app for memorising teaching notes

[Back to overview](../README.md)

## Problem
A learner has pages of handwritten or printed teaching notes (Sanskrit terms included) and wants to memorise them. Typical note apps do not support the loop: capture a page, correct its structure, practise with shrinking cues, listen, recite, review missed words.

## System built
- **Web app (PWA)** and an **Android beta**, sharing one UI. Package and version are on the public installer page.
- **Capture:** photo to text. Web uses a browser OCR engine; Android uses on-device ML Kit, so there is no API key or per-image cost. Retained photos support an independent "photo text" review workspace where a block can be replaced explicitly, with shared undo.
- **Practice:** progressively smaller cues, on-device text-to-speech playback, recording your own pronunciations into playlists, recitation checks.
- **Data safety:** projects export and import; a safe-updater page avoids replacing a version while another window holds unsaved work; learner storage is never cleared by an update.
- **Release discipline:** preview first, production after approval, rollback to the previous deployment, evidence folder per release.

## Evidence
- Releases hn-v56 (8 Nov 2026) to hn-v61 (9 Nov 2026) are documented with deployment, source commit and rollback targets. [E14](../evidence/README.md#e14)
- hn-v61: clean install, build and 213 unit tests passed, plus browser suites for safe update, projects, page-editor slices, on-device speech and recording playlists (9 Nov 2026). [E11](../evidence/README.md#e11)
- Public: the web app and installer page respond (checked 10 Nov 2026). The installer page documents the package id, version code and APK checksum.
- Repository history: about 120 commits to the app folder between 3 and 9 Nov 2026.

## Status (what exists, what does not)
Working beta for one user; a UX redesign was under way as of 8 Nov 2026. Not measured: number of users (there is no usage data), store listing, iOS app (iOS and browser use the weaker OCR engine). Installation on the owner's phone of the latest beta was not verified. It is not a product with customers.

## What I would do for a client
Write the practice loop and its data-loss rules first, pick the OCR engine by measuring your own pages, and ship behind a preview-then-promote flow with a rollback id and a regression test for every data-loss bug.

# Playbook: gate before publish (sanitized)

Used for every short video the studio builds. The rule is simple: a piece is "done" only when a script says so.

1. Build in a dated folder: script, facts table (each row has a source), cover text, caption, final encode.
2. Run the gate on the ENCODED file (not the editor project). It checks, each as PASS / FAIL / N/A:
   kill switch absent, format status (proven or not), card legibility (contrast floor by size and weight),
   caption-to-voice sync, safe zones for the platform UI, motion QC for animated beats, facts sourced,
   own-work share and credits, no restricted locations, cover wording, caption present, footage checks.
3. "Not evidenced" counts as FAIL. A stale QC file (hash of the video does not match) counts as FAIL.
4. A proven format with every gate PASS may post; anything else becomes a draft for a human to review.
5. Every gate run is registered in the library (name, version, result) so the history is searchable.
6. After posting, read the 48 h and day-7 numbers and write the learning back to the format row.
Owner of the rule file: one person edits the list of proven formats, with the evidence line.

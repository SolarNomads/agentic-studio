# Playbook: deploy card (sanitized)

A site change goes live only with a one-page card and a named yes for that exact change.

Fields, one line each:
- Approval: who approved, in their words, with date
- Scope: what changes, and "nothing else"
- Diff: files changed versus the deployed branch
- Tests: pass / fail; pre-existing failures named
- Deploy command
- Rollback: previous deployment id and the command to re-promote it
- Live checks: how "done" is verified on the live URL

Steps: write card -> get the yes -> run offline checks (build, indexing invariants, required URLs,
link counts) -> deploy -> run the same checks live -> record deployment id, previous id, result.
Done means verified live (a header, a page text, an API field), not "code written".

# Ashram Atlas: a sourced directory with measured search and click behaviour

[Back to overview](../README.md)

## Problem
Travellers looking for ashram stays find outdated blog posts. A directory is only worth publishing if every field is from an official source and "unknown" is shown as unknown.

## System built
- **Static site generator** (Python standard library) from one JSON file per ashram. Fields come from official pages only; anything not published renders as "Not published - contact ashram"; the build fails loudly on missing sources. Licensed images only, with attribution fields.
- **Deploy checks:** `deploy_check.py` (required URLs, link counts, product link id, private-path guards) and `index_check.py` (indexing invariants; with `--live` it fetches every sitemap URL with a crawler user agent and checks headers, 404s and redirects). Both run before and after a deploy; a deploy needs a one-page card with a rollback id ([playbook](../samples/playbooks/deploy-card.md)).
- **Click tracking:** every outbound commercial link is rewritten to a first-party redirect that logs the click and then redirects to the unchanged destination. Owner-cookie and automated user agents are redirected but not logged ([sample](../samples/owner_bot_filter.mjs)). No personal data in the log.
- **Route-pack product:** a 36-page printable guide with a facts table (84 rows after verification), official hours and sources per row, a changelog, and an independent review pass. Status: ready to upload; not yet on sale.
- **Search Console reads:** a script reads clicks and impressions into a metrics CSV.

## Evidence
- Public site, checked 10 Nov 2026: 42 ashram profiles and 153 URLs in the public sitemap. [E6](../evidence/README.md#e6)
- Google Search Console clicks per 7 days: 25 (21-27 Oct 2026) to 73 (2-8 Nov 2026); impressions 1,404 to 4,355 over the same windows. Small numbers on a young site; the direction is the point. [E5](../evidence/README.md#e5)
- A regression on 10 Nov (two deploys dropped approved content) was caught by review, repaired by a later deploy, and `deploy_check.py` was added to prevent a repeat.
- Revenue: none yet (pre-revenue). Affiliate programs are applied for or in setup.

## What I would do for a client
Define the source-of-truth rule for each field, make the build fail on violations, put checks before and after every deploy, and instrument outbound links from day one with a bot and owner filter so click numbers can be trusted.

#!/usr/bin/env python3
"""Extract aggregate Search Console numbers (clicks, impressions per window) from the site metrics log.
Usage: extract_search_console.py SRC_CSV  -> writes evidence/search_console.csv (latest reading per site/window)."""
import csv, sys
from pathlib import Path
rows = list(csv.DictReader(open(sys.argv[1], newline="")))
last = {}
for r in sorted(rows, key=lambda r: r["read_at_utc"]):
    if r["source"] == "gsc" and r["metric"] in ("clicks", "impressions") and r["window"].startswith(("7d:", "28d:")):
        last[(r["site"], r["window"], r["metric"])] = r
wins = sorted({(s, w) for s, w, _ in last})
out = Path(__file__).resolve().parent.parent / "evidence" / "search_console.csv"
with open(out, "w", newline="") as f:
    w = csv.writer(f); w.writerow(["site", "window", "clicks", "impressions", "read_at_utc"])
    for s, win in wins:
        c, i = last.get((s, win, "clicks")), last.get((s, win, "impressions"))
        if c and i: w.writerow([s, win, c["value"], i["value"], c["read_at_utc"]])
print(open(out).read())

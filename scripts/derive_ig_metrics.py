#!/usr/bin/env python3
"""Re-derive the Instagram figures used in this portfolio, and draw the charts.

Two steps, both stdlib-only:

  extract SRC_DIR   read the private metric logs (ig_account.csv, ig.csv) and write the
                    aggregate extracts in evidence/ (account-level numbers and per-reel
                    public counters; nothing else is copied).
  report            read ONLY evidence/*.csv, print every headline figure with its date
                    range, and write assets/ig-growth.svg.

Anyone can run `report` on a clone of this repo and get the same numbers.
"""
import csv
import datetime as dt
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EV = ROOT / "evidence"


def num(v):
    try:
        return int(float(v))
    except (TypeError, ValueError):
        return None


def extract(src):
    src = Path(src)
    acct = list(csv.DictReader(open(src / "ig_account.csv", newline="")))
    reels = list(csv.DictReader(open(src / "ig.csv", newline="")))
    EV.mkdir(exist_ok=True)

    # 1. follower readings: every distinct (timestamp, followers) pair from both logs and the raw daily snapshots
    pts = {}
    for fp in sorted((src / "raw").glob("ig_2026*.json")):
        d = json.load(open(fp))
        if num(d.get("followers")) is not None and d.get("read_at"):
            pts[d["read_at"][:16] + "Z"] = num(d["followers"])
    for r in acct:
        if num(r["followers"]) is not None:
            pts[r["read_at"][:16] + "Z"] = num(r["followers"])
    for r in reels:
        if num(r["followers"]) is not None:
            pts.setdefault(r["read_at"][:16] + "Z", num(r["followers"]))
    with open(EV / "ig_followers.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["read_at_utc", "followers"])
        for k in sorted(pts):
            w.writerow([k, pts[k]])

    # 2. account insights, 7-day window, only rows that carry values
    cols = ["views", "viewers", "interactions", "profile_visits", "link_taps"]
    d30 = {r["read_at"]: r["views_nonfollowers_pct"] for r in acct if r["window"] == "d30"}
    with open(EV / "ig_account_7d.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["read_at_utc"] + cols + ["nonfollower_views_pct_7d", "nonfollower_views_pct_30d"])
        for r in acct:
            if r["window"] == "d7" and num(r["views"]) is not None:
                w.writerow([r["read_at"][:16] + "Z"] + [num(r[c]) for c in cols]
                           + [r["views_nonfollowers_pct"], d30.get(r["read_at"], "")])

    # 3. per-reel public counters, latest reading per reel
    latest = {}
    for r in sorted(reels, key=lambda r: r["read_at"]):
        latest[r["code"]] = r
    with open(EV / "ig_reels_latest.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["reel_url", "posted_utc_date", "views", "likes", "saves", "shares", "read_at_utc"])
        for r in sorted(latest.values(), key=lambda r: -(num(r["views"]) or 0)):
            if r["kind"] != "reel":
                continue
            w.writerow([r["url"], r["posted"][:10], num(r["views"]), num(r["likes"]),
                        num(r["saves"]), num(r["shares"]), r["read_at"][:16] + "Z"])
    print("wrote", [p.name for p in sorted(EV.glob("ig_*.csv"))])


def ts(s):
    return dt.datetime.strptime(s, "%Y-%m-%dT%H:%MZ")


def svg(fol, views, path):
    W, H, L, R = 760, 330, 56, 20
    t0, t1 = ts(fol[0][0]), ts(fol[-1][0])
    span = (t1 - t0).total_seconds()
    X = lambda t: L + (ts(t) - t0).total_seconds() / span * (W - L - R)

    def panel(top, h, pts, color, title, fmt):
        ymax = max(v for _, v in pts) * 1.08
        Y = lambda v: top + h - v / ymax * h
        out = [f'<text x="{L}" y="{top - 8}" font-size="13" font-weight="600" fill="#222">{title}</text>',
               f'<line x1="{L}" y1="{top + h}" x2="{W - R}" y2="{top + h}" stroke="#bbb"/>']
        for frac in (0.5, 1.0):
            v = ymax / 1.08 * frac
            y = Y(v)
            out.append(f'<line x1="{L}" y1="{y:.1f}" x2="{W - R}" y2="{y:.1f}" stroke="#eee"/>')
            out.append(f'<text x="{L - 6}" y="{y + 4:.1f}" font-size="11" text-anchor="end" fill="#555">{fmt(v)}</text>')
        d = " ".join(f"{X(t):.1f},{Y(v):.1f}" for t, v in pts)
        out.append(f'<polyline points="{d}" fill="none" stroke="{color}" stroke-width="2"/>')
        for t, v in pts:
            out.append(f'<circle cx="{X(t):.1f}" cy="{Y(v):.1f}" r="2.5" fill="{color}"/>')
        t, v = pts[-1]
        out.append(f'<text x="{X(t) - 4:.1f}" y="{Y(v) - 8:.1f}" font-size="11" text-anchor="end" fill="{color}">{fmt(v)}</text>')
        return out

    k = lambda v: f"{v / 1000:.0f}k" if v >= 10000 else f"{v:,.0f}"
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="Helvetica,Arial,sans-serif">',
             '<rect width="100%" height="100%" fill="#fff"/>']
    parts += panel(34, 110, fol, "#1b6ca8", "Followers (each dot = one reading)", k)
    parts += panel(196, 90, views, "#b5541c", "Account views, trailing 7 days (as reported by the platform)", k)
    d0, d1 = t0.strftime("%d %b %Y"), t1.strftime("%d %b %Y")
    parts.append(f'<text x="{L}" y="{H - 10}" font-size="11" fill="#555">{d0} to {d1} (UTC). Source: evidence/ig_followers.csv, evidence/ig_account_7d.csv</text>')
    parts.append("</svg>")
    Path(path).write_text("\n".join(parts), encoding="utf-8")


def report():
    fol = [(r["read_at_utc"], int(r["followers"])) for r in csv.DictReader(open(EV / "ig_followers.csv"))]
    acc = list(csv.DictReader(open(EV / "ig_account_7d.csv")))
    reels = list(csv.DictReader(open(EV / "ig_reels_latest.csv")))
    out = {}
    out["followers_first"] = fol[0]
    out["followers_last"] = fol[-1]
    f3 = next(p for p in fol if p[0].startswith("2026-11-03T12:35"))
    out["followers_3nov"] = f3
    out["gain_3nov_to_last"] = fol[-1][1] - f3[1]
    out["gain_pct"] = round((fol[-1][1] - f3[1]) / f3[1] * 100, 1)
    out["days_between"] = round((ts(fol[-1][0]) - ts(f3[0])).total_seconds() / 86400, 1)
    a = [(r["read_at_utc"], int(r["views"])) for r in acc]
    out["views7d_latest"] = a[-1]
    out["views7d_peak"] = max(a, key=lambda p: p[1])
    out["views7d_first"] = a[0]
    last = acc[-1]
    out["nonfollower_pct_7d_30d"] = (last["nonfollower_views_pct_7d"], last["nonfollower_views_pct_30d"], last["read_at_utc"])
    out["days_first_to_last"] = round((ts(fol[-1][0]) - ts(fol[0][0])).total_seconds() / 86400, 1)
    out["profile_visits_7d_latest"] = int(last["profile_visits"])
    out["link_taps_7d_latest"] = int(last["link_taps"])
    out["reels_tracked"] = len(reels)
    out["reels_over_10k"] = sum(1 for r in reels if int(r["views"] or 0) >= 10000)
    out["top_reels"] = [(r["reel_url"], r["posted_utc_date"], int(r["views"])) for r in reels[:5]]
    out["sum_reel_views_lifetime"] = sum(int(r["views"] or 0) for r in reels)
    print(json.dumps(out, indent=1))
    # one daily reading (the last of each UTC day) for the chart's 7-day views line
    perday = {}
    for t, v in a:
        perday[t[:10]] = (t, v)
    svg(fol, sorted(perday.values()), ROOT / "assets" / "ig-growth.svg")
    print("wrote assets/ig-growth.svg")


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "extract":
        extract(sys.argv[2])
    elif len(sys.argv) == 2 and sys.argv[1] == "report":
        report()
    else:
        sys.exit(__doc__)

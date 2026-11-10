#!/usr/bin/env python3
"""Evidence-Based Management scorecard from a CSV of measurements. Stdlib only.

CSV columns: period, kva (CV|UV|T2M|A2I), measure, value, direction (higher|lower). Periods sort as text
(use 2026-01, 2026-Q1, 2026-W05...). Usage: python ebm_scorecard.py ebm.csv [--threshold 5] [--delimiter ,]
Signal: improving / worsening when the change vs previous period exceeds --threshold percent, else flat.
"""
import argparse
import csv
import sys
from collections import OrderedDict, defaultdict

if hasattr(sys.stdout, "reconfigure"):  # Windows consoles default to a legacy code page
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

KVA_NAMES = OrderedDict([("CV", "Current Value"), ("UV", "Unrealized Value"),
                         ("T2M", "Time to Market"), ("A2I", "Ability to Innovate")])


def pct(new, old):
    if old in (None, 0) or new is None:
        return None
    return 100.0 * (new - old) / abs(old)


def signal(change, direction, threshold):
    if change is None:
        return "n/a"
    if abs(change) < threshold:
        return "→ flat"
    better = change > 0 if direction == "higher" else change < 0
    return "▲ improving" if better else "▼ worsening"


def num(v):
    try:
        return float(str(v).replace(",", ".").replace(" ", ""))
    except ValueError:
        return None


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv")
    ap.add_argument("--threshold", type=float, default=5.0)
    ap.add_argument("--delimiter", default=None)
    a = ap.parse_args(argv)
    with open(a.csv, encoding="utf-8-sig", newline="") as f:
        sample = f.read(2048)
        f.seek(0)
        d = a.delimiter or (";" if sample.count(";") > sample.count(",") else ",")
        rows = list(csv.DictReader(f, delimiter=d))
    series = defaultdict(dict)
    meta = {}
    for r in rows:
        kva = (r.get("kva") or "").strip().upper()
        m = (r.get("measure") or "").strip()
        if kva not in KVA_NAMES or not m:
            print("skip row with unknown kva or empty measure: %s" % r, file=sys.stderr)
            continue
        series[(kva, m)][r["period"].strip()] = num(r.get("value"))
        meta[(kva, m)] = (r.get("direction") or "higher").strip().lower()
    summary = defaultdict(lambda: {"▲ improving": 0, "▼ worsening": 0, "→ flat": 0, "n/a": 0})
    print("## EBM scorecard\n")
    for kva, name in KVA_NAMES.items():
        measures = [k for k in series if k[0] == kva]
        if not measures:
            print("### %s (%s): no measure tracked\n" % (name, kva))
            continue
        print("### %s (%s)\n" % (name, kva))
        print("| Measure | Baseline | Previous | Latest | vs previous | vs baseline | Signal |")
        print("|---|---|---|---|---|---|---|")
        for key in sorted(measures, key=lambda k: k[1]):
            pts = sorted(series[key].items())
            base, latest = pts[0], pts[-1]
            prev = pts[-2] if len(pts) > 1 else None
            ch_prev = pct(latest[1], prev[1]) if prev else None
            ch_base = pct(latest[1], base[1]) if len(pts) > 1 else None
            sig = signal(ch_prev, meta[key], a.threshold)
            summary[kva][sig] += 1
            print("| %s (%s is better) | %s (%s) | %s | %s (%s) | %s | %s | %s |" % (
                key[1], meta[key], base[1], base[0], "%s (%s)" % (prev[1], prev[0]) if prev else "-",
                latest[1], latest[0], ("%+.1f %%" % ch_prev) if ch_prev is not None else "-",
                ("%+.1f %%" % ch_base) if ch_base is not None else "-", sig))
        print()
    print("### Summary by key value area\n")
    print("| KVA | Improving | Worsening | Flat | Not enough data |\n|---|---|---|---|---|")
    for kva, name in KVA_NAMES.items():
        s = summary[kva]
        print("| %s | %d | %d | %d | %d |" % (name, s["▲ improving"], s["▼ worsening"], s["→ flat"], s["n/a"]))
    missing = [n for k, n in KVA_NAMES.items() if not any(key[0] == k for key in series)]
    if missing:
        print("\nKey value areas without any measure: %s. EBM needs at least one measure per area." % ", ".join(missing))
    return 0


if __name__ == "__main__":
    sys.exit(main())

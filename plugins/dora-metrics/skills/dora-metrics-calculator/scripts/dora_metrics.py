#!/usr/bin/env python3
"""Compute the five DORA metrics from CSV exports. Stdlib only.

Deployments CSV (one row per deployment):
  --time-col   deployment timestamp (required)
  --env-col / --env         keep rows whose environment equals --env (case-insensitive)
  --failed-col              truthy (yes/true/1/x/failed) if the deployment caused a failure needing remediation
  --restored-col            timestamp when service was restored after that failure
  --rework-col              truthy if the deployment was unplanned work to fix a defect
  --commit-col              first commit (or PR creation) time of the change deployed
Optional changes CSV (one row per change): --changes FILE --change-commit-col C --change-deploy-col D
Options: --period month|week, --since YYYY-MM-DD, --until YYYY-MM-DD, --delimiter
"""
import argparse
import csv
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from statistics import median

if hasattr(sys.stdout, "reconfigure"):  # Windows consoles default to a legacy code page
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

TRUTHY = {"1", "true", "yes", "y", "x", "failed", "failure", "oui", "o"}
FORMATS = ["%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d",
           "%d/%m/%Y %H:%M:%S", "%d/%m/%Y %H:%M", "%d/%m/%Y", "%m/%d/%Y %I:%M %p"]


def ts(s):
    s = (s or "").strip()
    if not s:
        return None
    t = s.replace("Z", "+00:00")
    try:
        d = datetime.fromisoformat(t)
        return d.replace(tzinfo=None) - (d.utcoffset() or timedelta(0)) if d.tzinfo else d
    except ValueError:
        pass
    for f in FORMATS:
        try:
            return datetime.strptime(s, f)
        except ValueError:
            continue
    return None


def read(path, delim):
    with open(path, encoding="utf-8-sig", newline="") as f:
        sample = f.read(4096)
        f.seek(0)
        d = delim or (";" if sample.count(";") > sample.count(",") else ",")
        return list(csv.DictReader(f, delimiter=d))


def bucket(d, period):
    if period == "week":
        y, w, _ = d.isocalendar()
        return "%d-W%02d" % (y, w)
    return d.strftime("%Y-%m")


def days_in(key, period):
    if period == "week":
        return 7
    y, m = map(int, key.split("-"))
    nxt = datetime(y + (m == 12), m % 12 + 1, 1)
    return (nxt - datetime(y, m, 1)).days


def fmt_h(hours):
    if hours is None:
        return "-"
    return "%.1f h" % hours if hours < 48 else "%.1f d" % (hours / 24)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--deployments", required=True)
    ap.add_argument("--time-col", required=True)
    ap.add_argument("--env-col")
    ap.add_argument("--env")
    ap.add_argument("--failed-col")
    ap.add_argument("--restored-col")
    ap.add_argument("--rework-col")
    ap.add_argument("--commit-col")
    ap.add_argument("--changes")
    ap.add_argument("--change-commit-col")
    ap.add_argument("--change-deploy-col")
    ap.add_argument("--period", choices=["month", "week"], default="month")
    ap.add_argument("--since")
    ap.add_argument("--until")
    ap.add_argument("--delimiter")
    a = ap.parse_args(argv)
    since = ts(a.since) if a.since else None
    until = ts(a.until) + timedelta(days=1) if a.until else None

    def in_range(d):
        return d and (not since or d >= since) and (not until or d < until)

    deps = defaultdict(int)
    fails = defaultdict(int)
    rework = defaultdict(int)
    recover = defaultdict(list)
    lead = defaultdict(list)
    rows = read(a.deployments, a.delimiter)
    if rows and a.time_col not in rows[0]:
        print("column '%s' not found; columns: %s" % (a.time_col, ", ".join(rows[0])), file=sys.stderr)
        return 2
    for r in rows:
        if a.env_col and a.env and (r.get(a.env_col) or "").strip().lower() != a.env.lower():
            continue
        d = ts(r.get(a.time_col))
        if not in_range(d):
            continue
        k = bucket(d, a.period)
        deps[k] += 1
        failed = a.failed_col and (r.get(a.failed_col) or "").strip().lower() in TRUTHY
        if failed:
            fails[k] += 1
            rest = ts(r.get(a.restored_col)) if a.restored_col else None
            if rest and rest >= d:
                recover[k].append((rest - d).total_seconds() / 3600)
        if a.rework_col and (r.get(a.rework_col) or "").strip().lower() in TRUTHY:
            rework[k] += 1
        if a.commit_col:
            c = ts(r.get(a.commit_col))
            if c and c <= d:
                lead[k].append((d - c).total_seconds() / 3600)
    if a.changes:
        for r in read(a.changes, a.delimiter):
            c, d = ts(r.get(a.change_commit_col)), ts(r.get(a.change_deploy_col))
            if c and d and d >= c and in_range(d):
                lead[bucket(d, a.period)].append((d - c).total_seconds() / 3600)

    keys = sorted(set(deps) | set(lead))
    print("## DORA metrics per %s\n" % a.period)
    print("| Period | Deployments | Deploys / day | Change lead time (median) | Change fail rate | Recovery time (median) | Rework rate |")
    print("|---|---|---|---|---|---|---|")
    for k in keys:
        n = deps[k]
        print("| %s | %d | %.2f | %s | %s | %s | %s |" % (
            k, n, n / days_in(k, a.period), fmt_h(median(lead[k]) if lead[k] else None),
            ("%.0f %%" % (100.0 * fails[k] / n)) if n and a.failed_col else "-",
            fmt_h(median(recover[k]) if recover[k] else None),
            ("%.0f %%" % (100.0 * rework[k] / n)) if n and a.rework_col else "-"))
    n = sum(deps.values())
    all_lead = [x for v in lead.values() for x in v]
    all_rec = [x for v in recover.values() for x in v]
    print("\n**Whole window**: %d deployments; change lead time median %s (n=%d); change fail rate %s; "
          "recovery time median %s (n=%d); rework rate %s." % (
              n, fmt_h(median(all_lead) if all_lead else None), len(all_lead),
              ("%.1f %%" % (100.0 * sum(fails.values()) / n)) if n and a.failed_col else "-",
              fmt_h(median(all_rec) if all_rec else None), len(all_rec),
              ("%.1f %%" % (100.0 * sum(rework.values()) / n)) if n and a.rework_col else "-"))
    print("\nThroughput = deployment frequency, change lead time, failed deployment recovery time; "
          "instability = change fail rate, deployment rework rate. Compare with the latest DORA report.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

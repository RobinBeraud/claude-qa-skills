#!/usr/bin/env python3
"""Quality flow metrics from an Azure DevOps or Jira CSV export. Stdlib only.

Required: --created COLUMN and --type COLUMN (bugs are rows whose type is in --bug-types).
Optional: --closed, --state, --severity, --found-in + --prod-values, --reopened (count column),
          --closed-states, --as-of YYYY-MM-DD, --delimiter.
Prints Markdown tables: monthly flow and open backlog by severity and age.
"""
import argparse
import csv
import sys
from collections import Counter, defaultdict
from datetime import datetime, date
from statistics import median

FORMATS = ["%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d",
           "%d/%m/%Y %H:%M:%S", "%d/%m/%Y %H:%M", "%d/%m/%Y", "%m/%d/%Y %I:%M %p", "%m/%d/%Y"]


def parse_date(s):
    s = (s or "").strip()
    if not s:
        return None
    if "T" in s and ("+" in s[10:] or s.endswith("Z")):
        try:
            return datetime.fromisoformat(s.replace("Z", "+00:00")).date()
        except ValueError:
            pass
    for f in FORMATS:
        try:
            return datetime.strptime(s, f).date()
        except ValueError:
            continue
    return None


def month(d):
    return d.strftime("%Y-%m")


def age_bucket(days):
    if days < 30:
        return "<30 d"
    if days < 90:
        return "30-90 d"
    if days < 180:
        return "90-180 d"
    return ">180 d"


def compute(rows, a):
    bug_types = {t.strip().lower() for t in a.bug_types.split(",")}
    prod_values = {v.strip().lower() for v in a.prod_values.split(",")} if a.prod_values else set()
    closed_states = {s.strip().lower() for s in a.closed_states.split(",")}
    as_of = datetime.strptime(a.as_of, "%Y-%m-%d").date() if a.as_of else date.today()
    created = Counter()
    closed = Counter()
    ttf = defaultdict(list)
    escaped = Counter()
    reopened = Counter()
    open_sev = Counter()
    open_age = Counter()
    skipped = 0
    for r in rows:
        if (r.get(a.type) or "").strip().lower() not in bug_types:
            continue
        c = parse_date(r.get(a.created))
        if not c:
            skipped += 1
            continue
        created[month(c)] += 1
        if a.found_in and (r.get(a.found_in) or "").strip().lower() in prod_values:
            escaped[month(c)] += 1
        if a.reopened:
            try:
                if float(r.get(a.reopened) or 0) > 0:
                    reopened[month(c)] += 1
            except ValueError:
                pass
        d = parse_date(r.get(a.closed)) if a.closed else None
        state = (r.get(a.state) or "").strip().lower() if a.state else ""
        is_closed = bool(d) or (state in closed_states)
        if d:
            closed[month(d)] += 1
            ttf[month(d)].append((d - c).days)
        if not is_closed and c <= as_of:
            sev = (r.get(a.severity) or "unset").strip() if a.severity else "all"
            open_sev[sev or "unset"] += 1
            open_age[age_bucket((as_of - c).days)] += 1
    return created, closed, ttf, escaped, reopened, open_sev, open_age, skipped, as_of


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv")
    ap.add_argument("--type", required=True)
    ap.add_argument("--created", required=True)
    ap.add_argument("--closed")
    ap.add_argument("--state")
    ap.add_argument("--severity")
    ap.add_argument("--found-in")
    ap.add_argument("--prod-values", default="")
    ap.add_argument("--reopened")
    ap.add_argument("--bug-types", default="Bug,Defect,Bogue,Anomalie")
    ap.add_argument("--closed-states", default="closed,done,resolved,fermé,terminé,removed")
    ap.add_argument("--as-of")
    ap.add_argument("--delimiter", default=None)
    a = ap.parse_args(argv)
    with open(a.csv, encoding="utf-8-sig", newline="") as f:
        sample = f.read(4096)
        f.seek(0)
        delim = a.delimiter or (";" if sample.count(";") > sample.count(",") else ",")
        rows = list(csv.DictReader(f, delimiter=delim))
    if rows and a.type not in rows[0]:
        print("column '%s' not found; columns are: %s" % (a.type, ", ".join(rows[0].keys())), file=sys.stderr)
        return 2
    created, closed, ttf, escaped, reopened, open_sev, open_age, skipped, as_of = compute(rows, a)
    months = sorted(set(created) | set(closed))
    print("## Bug flow per month\n")
    head = "| Month | Created | Closed | Net | Median days to close"
    head += " | Escaped to prod | Escape rate" if a.found_in else ""
    head += " | Reopened" if a.reopened else ""
    print(head + " |")
    print("|---" * head.count("|") + "|")
    for m in months:
        line = "| %s | %d | %d | %+d | %s" % (m, created[m], closed[m], created[m] - closed[m],
                                             ("%.0f" % median(ttf[m])) if ttf[m] else "-")
        if a.found_in:
            line += " | %d | %s" % (escaped[m], ("%.0f %%" % (100.0 * escaped[m] / created[m])) if created[m] else "-")
        if a.reopened:
            line += " | %d" % reopened[m]
        print(line + " |")
    print("\n## Open bugs on %s: %d\n" % (as_of.isoformat(), sum(open_sev.values())))
    print("| Severity | Open |\n|---|---|")
    for k, v in sorted(open_sev.items()):
        print("| %s | %d |" % (k, v))
    print("\n| Age | Open |\n|---|---|")
    for k in ["<30 d", "30-90 d", "90-180 d", ">180 d"]:
        print("| %s | %d |" % (k, open_age[k]))
    if skipped:
        print("\n%d bug row(s) skipped: unreadable creation date" % skipped, file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())

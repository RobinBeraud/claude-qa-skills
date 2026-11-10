#!/usr/bin/env python3
"""Open pull request backlog report from an exported JSON list (Azure DevOps, GitHub or GitLab). Stdlib only.

  az repos pr list --status active --top 1000 -o json > prs.json
  gh pr list --state open --limit 1000 --json number,title,author,createdAt,updatedAt,isDraft,reviewRequests,additions,deletions > prs.json
  glab mr list --output json > prs.json

  python stale_prs.py prs.json --as-of 2026-11-10 --stale-days 30
"""
import argparse
import datetime as dt
import json
import sys
from collections import Counter
from statistics import median

if hasattr(sys.stdout, "reconfigure"):  # Windows consoles default to a legacy code page
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BUCKETS = [(7, "< 7 days"), (30, "7-30 days"), (90, "30-90 days"), (365, "90-365 days"), (10 ** 9, "> 1 year")]


def ts(s):
    if not s:
        return None
    s = s.replace("Z", "+00:00")
    if "." in s:  # Azure DevOps has 7 decimals, fromisoformat on old Pythons accepts up to 6
        head, tail = s.split(".", 1)
        frac, sign, tz = tail, "", ""
        for sep in ("+", "-"):
            if sep in tail:
                frac, tz = tail.split(sep, 1)
                sign = sep
                break
        s = head + "." + frac[:6].ljust(6, "0") + (sign + tz if sign else "")
    d = dt.datetime.fromisoformat(s)
    return d.replace(tzinfo=None) if d.tzinfo is None else d.astimezone(dt.timezone.utc).replace(tzinfo=None)


def name_of(x):
    if isinstance(x, dict):
        return x.get("displayName") or x.get("name") or x.get("login") or x.get("username") or x.get("uniqueName") or "?"
    return str(x) if x else "?"


def normalise(items):
    """Return a list of {id, title, author, created, updated, draft, reviewers, size} whatever the source."""
    if isinstance(items, dict):
        items = items.get("value") or items.get("items") or []
    out = []
    for p in items:
        if "pullRequestId" in p:  # Azure DevOps
            out.append({"id": p["pullRequestId"], "title": p.get("title", ""), "author": name_of(p.get("createdBy")),
                        "created": ts(p.get("creationDate")), "updated": None, "draft": bool(p.get("isDraft")),
                        "reviewers": [name_of(r) for r in p.get("reviewers", []) if not r.get("isContainer")],
                        "votes": [r.get("vote", 0) for r in p.get("reviewers", [])],
                        "target": (p.get("targetRefName") or "").replace("refs/heads/", ""), "size": None,
                        "repo": (p.get("repository") or {}).get("name", "")})
        elif "iid" in p or "web_url" in p:  # GitLab
            out.append({"id": p.get("iid"), "title": p.get("title", ""), "author": name_of(p.get("author")),
                        "created": ts(p.get("created_at")), "updated": ts(p.get("updated_at")),
                        "draft": bool(p.get("draft") or p.get("work_in_progress")),
                        "reviewers": [name_of(r) for r in p.get("reviewers", [])], "votes": [],
                        "target": p.get("target_branch", ""), "size": None, "repo": ""})
        else:  # GitHub (gh --json)
            add, dele = p.get("additions"), p.get("deletions")
            out.append({"id": p.get("number"), "title": p.get("title", ""), "author": name_of(p.get("author")),
                        "created": ts(p.get("createdAt")), "updated": ts(p.get("updatedAt")), "draft": bool(p.get("isDraft")),
                        "reviewers": [name_of(r) for r in p.get("reviewRequests", [])], "votes": [],
                        "target": p.get("baseRefName", ""), "size": (add + dele) if add is not None and dele is not None else None,
                        "repo": ""})
    return [p for p in out if p["created"]]


def report(prs, as_of, stale_days=30):
    for p in prs:
        p["age_days"] = (as_of - p["created"]).days
        p["idle_days"] = (as_of - p["updated"]).days if p["updated"] else None
    buckets = Counter()
    for p in prs:
        for limit, label in BUCKETS:
            if p["age_days"] < limit:
                buckets[label] += 1
                break
    ages = [p["age_days"] for p in prs]
    idle = [p for p in prs if p["idle_days"] is not None and p["idle_days"] >= stale_days]
    no_reviewer = [p for p in prs if not p["reviewers"]]
    by_reviewer = Counter(r for p in prs for r in p["reviewers"])
    return {"open": len(prs), "drafts": sum(p["draft"] for p in prs), "median_age": median(ages) if ages else None,
            "buckets": [(label, buckets.get(label, 0)) for _, label in BUCKETS],
            "idle": sorted(idle, key=lambda p: -p["idle_days"]), "no_reviewer": no_reviewer,
            "by_author": Counter(p["author"] for p in prs).most_common(10), "by_reviewer": by_reviewer.most_common(10),
            "oldest": sorted(prs, key=lambda p: -p["age_days"])[:15],
            "has_updates": any(p["updated"] for p in prs)}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("json")
    ap.add_argument("--as-of", help="reference date YYYY-MM-DD (default: today, UTC)")
    ap.add_argument("--stale-days", type=int, default=30)
    a = ap.parse_args(argv)
    with open(a.json, encoding="utf-8-sig") as f:
        prs = normalise(json.load(f))
    as_of = dt.datetime.fromisoformat(a.as_of) if a.as_of else dt.datetime.utcnow()
    r = report(prs, as_of, a.stale_days)
    print("## Open pull requests as of %s\n" % as_of.date())
    if not prs:
        print("No open pull request found in the file.")
        return 0
    print("%d open, %d drafts, median age %.0f days, %d without any reviewer\n" % (r["open"], r["drafts"], r["median_age"], len(r["no_reviewer"])))
    print("| Age | PRs |\n|---|---|")
    for label, n in r["buckets"]:
        print("| %s | %d %s |" % (label, n, "#" * min(n, 40)))
    if r["has_updates"]:
        print("\n### Idle for %d+ days (%d)\n" % (a.stale_days, len(r["idle"])))
        for p in r["idle"][:20]:
            print("- #%s %s (by %s, idle %d d, age %d d%s)" % (p["id"], p["title"], p["author"], p["idle_days"], p["age_days"], ", draft" if p["draft"] else ""))
    else:
        print("\n(No last-update date in this export, e.g. Azure DevOps lists: idle time not computed, age only.)")
    print("\n### Open PRs per author\n\n" + ", ".join("%s %d" % kv for kv in r["by_author"]))
    if r["by_reviewer"]:
        print("\n### Review load (open PRs waiting per reviewer)\n\n" + ", ".join("%s %d" % kv for kv in r["by_reviewer"]))
    print("\n### Oldest\n\n| PR | Title | Author | Age (d) | Target | Draft |\n|---|---|---|---|---|---|")
    for p in r["oldest"]:
        print("| %s | %s | %s | %d | %s | %s |" % (p["id"], p["title"].replace("|", "\\|")[:70], p["author"], p["age_days"], p["target"], "yes" if p["draft"] else ""))
    print("\nDecide per PR with its author: merge, rebase, split, hand over, or close with a reason.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

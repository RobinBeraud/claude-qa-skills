#!/usr/bin/env python3
"""Which fixes of a source branch are missing from target branches? Stdlib only, needs git.

Uses `git cherry` (patch-id: a cherry-picked commit with the same change counts as present), then two
softer signals for commits whose patch differs after conflict resolution: a "cherry picked from commit"
trailer naming them, or the same work-item reference (AB#123, PROJ-123) in the target's history.

  python backport_check.py --repo . --source release/12.4 --targets release/13.0,main --since 2026-01-01
  python backport_check.py --repo . --source main --targets release/12.4 --grep "AB#" --format md
"""
import argparse
import json
import re
import subprocess
import sys

if hasattr(sys.stdout, "reconfigure"):  # Windows consoles default to a legacy code page
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REF_RE = re.compile(r"\bAB#\d+\b|\b[A-Z][A-Z0-9]{1,9}-\d+\b|(?<![\w/])#\d+\b")
PICKED_RE = re.compile(r"cherry picked from commit ([0-9a-f]{7,40})")


def git(repo, *args):
    try:
        return subprocess.run(["git", "-C", repo] + list(args), capture_output=True, text=True, check=True,
                              encoding="utf-8", errors="replace").stdout
    except subprocess.CalledProcessError as e:
        raise SystemExit("error: git %s failed: %s" % (" ".join(args[:2]), (e.stderr or "").strip()))


def commits(repo, rev_range, since=None):
    args = ["log", "--no-merges", "--format=%H%x1f%h%x1f%ad%x1f%an%x1f%s%x1f%b%x1e", "--date=short"]
    if since:
        args.append("--since=" + since)
    out = []
    for rec in git(repo, *(args + [rev_range])).split("\x1e"):
        rec = rec.strip("\n")
        if not rec:
            continue
        sha, short, date, author, subject, body = (rec.split("\x1f") + [""] * 6)[:6]
        out.append({"sha": sha, "short": short, "date": date, "author": author, "subject": subject, "body": body})
    return out


def refs_of(text, grep=None):
    found = set(REF_RE.findall(text))
    if grep:
        found = {r for r in found if grep in r}
    return found


def classify(missing, target_msgs, grep=None):
    """missing: source commits with no patch-equivalent in target. target_msgs: full messages of target commits."""
    picked = set()
    target_refs = set()
    for m in target_msgs:
        picked |= {s for s in PICKED_RE.findall(m)}
        target_refs |= refs_of(m, grep)
    out = []
    for c in missing:
        refs = refs_of(c["subject"] + "\n" + c["body"], grep)
        if any(c["sha"].startswith(p) or p.startswith(c["sha"][:len(p)]) for p in picked):
            status = "backported (cherry-pick trailer, patch differs)"
        elif refs and refs <= target_refs:
            status = "probably backported (same work item in target)"
        elif refs & target_refs:
            status = "partly backported (some work items in target)"
        else:
            status = "MISSING"
        out.append(dict(c, refs=sorted(refs), status=status))
    return out


def check(repo, source, target, since=None, grep=None):
    missing_shas = [l[2:].split(" ", 1)[0] for l in git(repo, "cherry", target, source).splitlines() if l.startswith("+ ")]
    in_range = {c["sha"]: c for c in commits(repo, "%s..%s" % (target, source), since)}
    missing = [in_range[s] for s in missing_shas if s in in_range]
    target_msgs = [c["subject"] + "\n" + c["body"] for c in commits(repo, target, since)]
    return classify(missing, target_msgs, grep)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", default=".")
    ap.add_argument("--source", required=True, help="branch whose fixes must be present elsewhere")
    ap.add_argument("--targets", required=True, help="comma-separated branches to check")
    ap.add_argument("--since", help="only source commits after this date")
    ap.add_argument("--grep", help="keep only work-item references containing this text, e.g. AB#")
    ap.add_argument("--only-missing", action="store_true")
    ap.add_argument("--format", choices=["text", "md", "json"], default="text")
    a = ap.parse_args(argv)
    report = {t.strip(): check(a.repo, a.source, t.strip(), a.since, a.grep) for t in a.targets.split(",") if t.strip()}
    if a.format == "json":
        print(json.dumps(report, indent=2))
        return 1 if any(c["status"] == "MISSING" for v in report.values() for c in v) else 0
    any_missing = False
    for target, rows in report.items():
        if a.only_missing:
            rows = [r for r in rows if r["status"] == "MISSING"]
        n_missing = sum(r["status"] == "MISSING" for r in rows)
        any_missing = any_missing or n_missing > 0
        print("%s%s -> %s: %d commit(s) without an identical change, %d clearly missing" % (
            "### " if a.format == "md" else "", a.source, target, len(rows), n_missing))
        if a.format == "md" and rows:
            print("\n| Commit | Date | Author | Subject | Work items | Status |\n|---|---|---|---|---|---|")
            for r in rows:
                print("| %s | %s | %s | %s | %s | %s |" % (r["short"], r["date"], r["author"], r["subject"].replace("|", "\\|"), ", ".join(r["refs"]), r["status"]))
        else:
            for r in rows:
                print("  %-9s %s %-40.40s %-14s %s" % (r["short"], r["date"], r["subject"], ",".join(r["refs"]), r["status"]))
        print()
    print("Patch-equivalent commits (clean cherry-picks) are already filtered out by git cherry.")
    return 1 if any_missing else 0


if __name__ == "__main__":
    sys.exit(main())

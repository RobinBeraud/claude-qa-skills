#!/usr/bin/env python3
"""Lint Conventional Commit subjects and generate grouped release notes from git history. Stdlib only.

Azure DevOps squash merges ("Merged PR 123: fix(api): ...") are understood: the prefix is removed
before parsing, and the PR number is kept as a reference.

  python changelog.py lint --repo . --range origin/main..HEAD
  python changelog.py notes --repo . --range v12.3.0..v12.4.0 --format md
"""
import argparse
import re
import subprocess
import sys

if hasattr(sys.stdout, "reconfigure"):  # Windows consoles default to a legacy code page
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

TYPES = ["feat", "fix", "perf", "refactor", "revert", "docs", "test", "build", "ci", "chore", "style"]
TITLES = {"breaking": "Breaking changes", "feat": "Features", "fix": "Bug fixes", "perf": "Performance",
          "refactor": "Refactoring", "revert": "Reverts", "docs": "Documentation", "test": "Tests",
          "build": "Build", "ci": "CI", "chore": "Chores", "style": "Style", "other": "Other changes"}
CC_RE = re.compile(r"^(?P<type>[a-z]+)(?:\((?P<scope>[^()\r\n]+)\))?(?P<bang>!)?: (?P<desc>\S.*)$")
PR_PREFIX = re.compile(r"^Merged PR (?P<pr>\d+):\s*")
MERGE_RE = re.compile(r"^Merge (branch|pull request|remote-tracking branch)\b")
REF_RE = re.compile(r"\bAB#\d+\b|\b[A-Z][A-Z0-9]{1,9}-\d+\b|(?<![\w/])#\d+\b|!\d+\b")


def parse(subject, body=""):
    pr = None
    m = PR_PREFIX.match(subject)
    if m:
        pr = m.group("pr")
        subject = subject[m.end():]
    c = CC_RE.match(subject)
    refs = sorted(set(REF_RE.findall(subject + "\n" + body)))
    if pr:
        refs.append("PR %s" % pr)
    if not c or c.group("type") not in TYPES:
        return {"ok": False, "type": "other", "scope": None, "desc": subject, "breaking": "BREAKING CHANGE" in body, "refs": refs}
    return {"ok": True, "type": c.group("type"), "scope": c.group("scope"), "desc": c.group("desc"),
            "breaking": bool(c.group("bang")) or "BREAKING CHANGE" in body or "BREAKING-CHANGE" in body, "refs": refs}


def lint_subject(subject, max_len=72):
    problems = []
    s = PR_PREFIX.sub("", subject)
    if MERGE_RE.match(subject):
        return problems
    c = CC_RE.match(s)
    if not c:
        problems.append("not '<type>(<scope>): <description>'")
    elif c.group("type") not in TYPES:
        problems.append("unknown type '%s' (use %s)" % (c.group("type"), ", ".join(TYPES)))
    else:
        d = c.group("desc")
        if d.endswith("."):
            problems.append("description ends with a dot")
        if d[:1].isupper() and not d.split(" ")[0].isupper():
            problems.append("description should start in lower case")
    if len(s) > max_len:
        problems.append("longer than %d characters (%d)" % (max_len, len(s)))
    return problems


def log(repo, rng):
    try:
        out = subprocess.run(["git", "-C", repo, "log", "--no-merges", "--format=%h%x1f%s%x1f%b%x1e", rng],
                             capture_output=True, text=True, check=True, encoding="utf-8", errors="replace").stdout
    except subprocess.CalledProcessError as e:
        raise SystemExit("error: git log failed: %s" % (e.stderr or "").strip())
    rows = []
    for rec in out.split("\x1e"):
        rec = rec.strip("\n")
        if rec:
            h, s, b = (rec.split("\x1f") + ["", ""])[:3]
            rows.append((h, s, b))
    return rows


def notes(rows):
    groups = {}
    for h, s, b in rows:
        if MERGE_RE.match(s):
            continue
        p = parse(s, b)
        key = "breaking" if p["breaking"] else p["type"]
        groups.setdefault(key, []).append(dict(p, sha=h))
    order = ["breaking"] + TYPES + ["other"]
    return [(k, groups[k]) for k in order if k in groups]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("lint", "notes"):
        p = sub.add_parser(name)
        p.add_argument("--repo", default=".")
        p.add_argument("--range", required=True, help="git range, e.g. origin/main..HEAD or v1.2.0..v1.3.0")
        if name == "lint":
            p.add_argument("--max-length", type=int, default=72)
        else:
            p.add_argument("--format", choices=["md", "text"], default="md")
            p.add_argument("--title", default="")
    a = ap.parse_args(argv)
    rows = log(a.repo, a.range)
    if a.cmd == "lint":
        bad = [(h, s, lint_subject(s, a.max_length)) for h, s, _ in rows]
        bad = [x for x in bad if x[2]]
        for h, s, probs in bad:
            print("%s  %s\n          -> %s" % (h, s, "; ".join(probs)))
        print("%d commit(s) checked, %d to fix" % (len(rows), len(bad)))
        return 1 if bad else 0
    title = a.title or "Changes in %s" % a.range
    print(("## %s\n" if a.format == "md" else "%s\n") % title)
    refs = set()
    for key, items in notes(rows):
        print(("### %s\n" if a.format == "md" else "%s:") % TITLES[key])
        for it in items:
            refs |= set(it["refs"])
            scope = ("**%s**: " % it["scope"]) if it["scope"] and a.format == "md" else (it["scope"] + ": " if it["scope"] else "")
            print("- %s%s%s (%s)" % (scope, it["desc"], (" " + ", ".join(it["refs"])) if it["refs"] else "", it["sha"]))
        print()
    if refs:
        print("Referenced work items: " + ", ".join(sorted(refs)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

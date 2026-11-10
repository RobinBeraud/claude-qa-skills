#!/usr/bin/env python3
"""Hotspots from git history: files ranked by change frequency x size, authors, and co-change coupling.
Stdlib only, needs git.

  python hotspots.py --repo . --since 2025-01-01 --top 25
  python hotspots.py --repo . --since 12.months --path src/Billing --format md
"""
import argparse
import fnmatch
import json
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict
from itertools import combinations

if hasattr(sys.stdout, "reconfigure"):  # Windows consoles default to a legacy code page
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DEFAULT_EXCLUDE = ["*.lock", "package-lock.json", "packages.lock.json", "yarn.lock", "pnpm-lock.yaml", "*.Designer.cs",
                   "*.designer.cs", "*.g.cs", "*ModelSnapshot.cs", "*.min.js", "*.min.css", "*.map", "*.snap", "*.resx",
                   "*.xlf", "*.svg", "*.png", "*.jpg", "*.dll", "*.exe", "*.pdf", "*.csproj", "*.sln", "*.json", "*.md"]
SEP = "\x1fCOMMIT\x1f"


def excluded(path, patterns):
    name = path.rsplit("/", 1)[-1]
    return any(fnmatch.fnmatch(path, p) or fnmatch.fnmatch(name, p) for p in patterns)


def clean_path(p):
    p = re.sub(r"\{[^{}]* => ([^{}]*)\}", r"\1", p)
    if " => " in p:
        p = p.split(" => ", 1)[1]
    return p.replace("//", "/")


def parse_log(text, patterns):
    """Return list of commits: {author, date, files: {path: churn}}."""
    commits = []
    for block in text.split(SEP)[1:]:
        lines = block.strip("\n").splitlines()
        if not lines:
            continue
        head = lines[0].split("\x1f")
        author, date = (head + ["", ""])[:2]
        files = {}
        for l in lines[1:]:
            parts = l.split("\t", 2)
            if len(parts) != 3:
                continue
            path = clean_path(parts[2])
            if excluded(path, patterns):
                continue
            churn = 0 if parts[0] == "-" else int(parts[0]) + int(parts[1])
            files[path] = files.get(path, 0) + churn
        commits.append({"author": author, "date": date, "files": files})
    return commits


def compute(commits, line_counts, top=25, max_files_per_commit=40, min_pair=3):
    n_commits, authors, churn, last = Counter(), defaultdict(set), Counter(), {}
    pairs = Counter()
    for c in commits:
        for f, ch in c["files"].items():
            n_commits[f] += 1
            authors[f].add(c["author"])
            churn[f] += ch
            if c["date"] > last.get(f, ""):
                last[f] = c["date"]
        fs = sorted(c["files"])
        if 2 <= len(fs) <= max_files_per_commit:
            for a, b in combinations(fs, 2):
                pairs[(a, b)] += 1
    rows = []
    for f, n in n_commits.items():
        lines = line_counts.get(f)
        if lines is None:  # file deleted or renamed away since
            continue
        rows.append({"path": f, "commits": n, "authors": len(authors[f]), "lines": lines, "churn": churn[f],
                     "last_change": last.get(f, ""), "raw": n * lines})
    top_raw = max((r["raw"] for r in rows), default=1) or 1
    for r in rows:
        r["score"] = round(100 * r["raw"] / top_raw, 1)
        del r["raw"]
    rows.sort(key=lambda r: -r["score"])
    coupling = []
    for (a, b), k in pairs.most_common():
        if k < min_pair:
            break
        if a not in line_counts or b not in line_counts:
            continue
        degree = k / min(n_commits[a], n_commits[b])
        coupling.append({"a": a, "b": b, "together": k, "degree": round(degree, 2),
                         "cross_module": a.split("/")[:-1][:2] != b.split("/")[:-1][:2]})
    coupling.sort(key=lambda c: (-c["together"], -c["degree"]))
    return {"commits": len(commits), "files": len(rows), "hotspots": rows[:top], "coupling": coupling[:top]}


def count_lines(repo, paths):
    out = {}
    for p in paths:
        fp = os.path.join(repo, p)
        if os.path.isfile(fp):
            try:
                with open(fp, "rb") as f:
                    out[p] = sum(1 for _ in f)
            except OSError:
                pass
    return out


def git_log(repo, since, path):
    cmd = ["git", "-C", repo, "log", "--no-merges", "--numstat", "-M", "--date=short",
           "--format=" + SEP + "%an\x1f%ad"]
    if since:
        cmd.append("--since=" + since.replace(".", " ") if re.fullmatch(r"\d+\.\w+", since) else "--since=" + since)
    if path:
        cmd += ["--", path]
    try:
        return subprocess.run(cmd, capture_output=True, text=True, check=True, encoding="utf-8", errors="replace").stdout
    except subprocess.CalledProcessError as e:
        raise SystemExit("error: git failed: %s" % (e.stderr or e).strip())


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", default=".")
    ap.add_argument("--since", default="12 months ago", help="git date: 2025-01-01, '12 months ago', 12.months")
    ap.add_argument("--path", help="restrict to a folder")
    ap.add_argument("--top", type=int, default=25)
    ap.add_argument("--exclude", default="", help="extra comma-separated glob patterns to ignore")
    ap.add_argument("--min-pair", type=int, default=3, help="minimum commits together to report a coupling")
    ap.add_argument("--format", choices=["text", "md", "json"], default="text")
    a = ap.parse_args(argv)
    patterns = DEFAULT_EXCLUDE + [p for p in a.exclude.split(",") if p]
    commits = parse_log(git_log(a.repo, a.since, a.path), patterns)
    files = {f for c in commits for f in c["files"]}
    r = compute(commits, count_lines(a.repo, files), a.top, min_pair=a.min_pair)
    if a.format == "json":
        print(json.dumps(r, indent=2))
        return 0
    print("Hotspots since %s%s: %d commits, %d files still present\n" % (a.since, (" in " + a.path) if a.path else "", r["commits"], r["files"]))
    if a.format == "md":
        print("| Score | File | Commits | Authors | Lines | Last change |\n|---|---|---|---|---|---|")
        for h in r["hotspots"]:
            print("| %.0f | %s | %d | %d | %d | %s |" % (h["score"], h["path"], h["commits"], h["authors"], h["lines"], h["last_change"]))
        if r["coupling"]:
            print("\n**Files that change together**\n\n| File A | File B | Together | Degree | Cross-module |\n|---|---|---|---|---|")
            for c in r["coupling"]:
                print("| %s | %s | %d | %.0f%% | %s |" % (c["a"], c["b"], c["together"], 100 * c["degree"], "yes" if c["cross_module"] else ""))
    else:
        for h in r["hotspots"]:
            print("%5.0f  %-70s %4d commits %3d authors %6d lines  %s" % (h["score"], h["path"], h["commits"], h["authors"], h["lines"], h["last_change"]))
        if r["coupling"]:
            print("\nFiles that change together:")
            for c in r["coupling"]:
                print("  %3d x  %.0f%%  %s <-> %s%s" % (c["together"], 100 * c["degree"], c["a"], c["b"], "  [cross-module]" if c["cross_module"] else ""))
    print("\nScore = commits x current lines, 100 = top file. Generated, lock, binary, json and md files are excluded.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

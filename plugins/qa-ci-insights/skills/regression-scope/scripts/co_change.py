#!/usr/bin/env python3
"""Rank the test files most related to the files changed in a branch, from git history. Stdlib only.

Usage (inside a git repository):
  python co_change.py [--base origin/main] [--head HEAD] [--history 1500] [--top 30] [--files a.py b.cs]
Score per test file = 3 x name match + number of past commits where it changed with a changed source file.
Commits touching more than --max-files files (default 50) are ignored as bulk/noise.
"""
import argparse
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict

if hasattr(sys.stdout, "reconfigure"):  # Windows consoles default to a legacy code page
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

TEST_HINT = re.compile(r"(^|/)(tests?|specs?|__tests__|e2e)(/|$)|(_test|_spec|Tests?|Spec|\.test|\.spec)\.\w+$|(^|/)test_[^/]+$", re.I)


def is_test(path):
    return bool(TEST_HINT.search(path))


def stem(path):
    s = os.path.splitext(os.path.basename(path))[0].lower()
    s = re.sub(r"^(test_|tests_)", "", s)
    s = re.sub(r"(_test|_tests|_spec|tests|test|spec|\.test|\.spec)$", "", s)
    return s.strip("._-")


def git(*args):
    return subprocess.run(["git"] + list(args), capture_output=True, text=True, check=True).stdout


def history(n, max_files):
    out = git("log", "-n", str(n), "--name-only", "--pretty=format:@@%H")
    commits, cur = [], []
    for line in out.splitlines():
        if line.startswith("@@"):
            if cur:
                commits.append(cur)
            cur = []
        elif line.strip():
            cur.append(line.strip())
    if cur:
        commits.append(cur)
    return [c for c in commits if len(c) <= max_files]


def rank(changed, commits, all_tests, top):
    sources = [f for f in changed if not is_test(f)]
    scores = defaultdict(float)
    reasons = defaultdict(list)
    stems = {stem(s): s for s in sources}
    for t in all_tests:
        if stem(t) in stems and stem(t):
            scores[t] += 3
            reasons[t].append("name matches %s" % stems[stem(t)])
    co = Counter()
    src_set = set(sources)
    for files in commits:
        fs = set(files)
        if fs & src_set:
            for t in fs:
                if is_test(t):
                    co[t] += 1
    for t, c in co.items():
        scores[t] += c
        reasons[t].append("changed together %d time(s)" % c)
    ranked = sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))[:top]
    untested = [s for s in sources if not any(stem(s) == stem(t) for t, _ in ranked)
                and not any(s in files and any(is_test(x) for x in files) for files in commits)]
    return ranked, reasons, untested


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base", default="origin/main")
    ap.add_argument("--head", default="HEAD")
    ap.add_argument("--history", type=int, default=1500)
    ap.add_argument("--max-files", type=int, default=50)
    ap.add_argument("--top", type=int, default=30)
    ap.add_argument("--files", nargs="*", help="changed files (skip git diff)")
    a = ap.parse_args(argv)
    try:
        changed = a.files if a.files else [l for l in git("diff", "--name-only", "%s...%s" % (a.base, a.head)).splitlines() if l]
        all_files = git("ls-files").splitlines()
        commits = history(a.history, a.max_files)
    except subprocess.CalledProcessError as e:
        print("git failed: %s" % (e.stderr or e), file=sys.stderr)
        return 2
    all_tests = [f for f in all_files if is_test(f)]
    ranked, reasons, untested = rank(changed, commits, all_tests, a.top)
    print("Changed files: %d (%d tests)" % (len(changed), sum(1 for f in changed if is_test(f))))
    print("\n| Score | Test file | Why |\n|---|---|---|")
    for t, s in ranked:
        print("| %.0f | %s | %s |" % (s, t, "; ".join(reasons[t])))
    if untested:
        print("\nChanged source files with no related test found:")
        for s in untested:
            print("- %s" % s)
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Measure a branch's diff against a pull request size budget. Stdlib only, needs git.

Generated and lock files are counted apart, so a 3,000-line lock file does not hide a 120-line change
(or the reverse). Suggests a split by area when the budget is exceeded.

  python pr_size.py --base origin/main
  python pr_size.py --base origin/develop --budget 300 --format md
"""
import argparse
import fnmatch
import json
import re
import subprocess
import sys

if hasattr(sys.stdout, "reconfigure"):  # Windows consoles default to a legacy code page
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

GENERATED = [
    "package-lock.json", "yarn.lock", "pnpm-lock.yaml", "packages.lock.json", "poetry.lock", "Cargo.lock", "go.sum",
    "*.Designer.cs", "*.designer.cs", "*.g.cs", "*.g.i.cs", "*.generated.*", "*ModelSnapshot.cs", "*.snap",
    "*.verified.*", "*.min.js", "*.min.css", "*.map", "*.svg", "dist/*", "*/dist/*", "*/wwwroot/lib/*",
    "*/Migrations/*.Designer.cs", "*.resx", "*.xlf",
]


def is_generated(path, extra=()):
    name = path.rsplit("/", 1)[-1]
    return any(fnmatch.fnmatch(path, p) or fnmatch.fnmatch(name, p) for p in list(GENERATED) + list(extra))


def clean_path(p):
    p = re.sub(r"\{[^{}]* => ([^{}]*)\}", r"\1", p)
    if " => " in p:
        p = p.split(" => ", 1)[1]
    return p.replace("//", "/")


def area_of(path, depth=2):
    parts = path.split("/")
    if len(parts) == 1:
        return "(root)"
    if parts[0] in ("src", "source", "app", "apps", "packages", "libs", "projects", "tests", "test") and len(parts) > 2:
        return "/".join(parts[:depth])
    return parts[0]


def analyse(numstat, budget=400, extra_generated=()):
    files = []
    for line in numstat.splitlines():
        if not line.strip():
            continue
        add, dele, path = line.split("\t", 2)
        path = clean_path(path)
        binary = add == "-"
        a, d = (0, 0) if binary else (int(add), int(dele))
        files.append({"path": path, "added": a, "deleted": d, "binary": binary, "generated": is_generated(path, extra_generated)})
    code = [f for f in files if not f["generated"] and not f["binary"]]
    gen = [f for f in files if f["generated"]]
    changed = sum(f["added"] + f["deleted"] for f in code)
    areas = {}
    for f in code:
        ar = areas.setdefault(area_of(f["path"]), {"lines": 0, "files": 0})
        ar["lines"] += f["added"] + f["deleted"]
        ar["files"] += 1
    if changed <= budget * 0.5:
        verdict = "small"
    elif changed <= budget:
        verdict = "ok"
    elif changed <= budget * 2:
        verdict = "large"
    else:
        verdict = "too large"
    return {"files": len(files), "code_files": len(code), "changed_lines": changed,
            "added": sum(f["added"] for f in code), "deleted": sum(f["deleted"] for f in code),
            "generated_files": len(gen), "generated_lines": sum(f["added"] + f["deleted"] for f in gen),
            "binary_files": sum(f["binary"] for f in files), "areas": dict(sorted(areas.items(), key=lambda kv: -kv[1]["lines"])),
            "budget": budget, "verdict": verdict, "largest": sorted(code, key=lambda f: -(f["added"] + f["deleted"]))[:8],
            "generated_list": [f["path"] for f in gen]}


def git_numstat(repo, base, head):
    try:
        mb = subprocess.run(["git", "-C", repo, "merge-base", base, head], capture_output=True, text=True, check=True).stdout.strip()
        out = subprocess.run(["git", "-C", repo, "diff", "--numstat", "-M", mb, head], capture_output=True, text=True,
                             check=True, encoding="utf-8", errors="replace").stdout
    except subprocess.CalledProcessError as e:
        raise SystemExit("error: git failed: %s" % (e.stderr or e).strip())
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", default=".")
    ap.add_argument("--base", default="origin/main", help="target branch (default origin/main)")
    ap.add_argument("--head", default="HEAD")
    ap.add_argument("--budget", type=int, default=400, help="changed lines budget, generated files excluded (default 400)")
    ap.add_argument("--generated", default="", help="extra comma-separated glob patterns to treat as generated")
    ap.add_argument("--format", choices=["text", "md", "json"], default="text")
    a = ap.parse_args(argv)
    r = analyse(git_numstat(a.repo, a.base, a.head), a.budget, [p for p in a.generated.split(",") if p])
    if a.format == "json":
        print(json.dumps(r, indent=2))
        return 0
    md = a.format == "md"
    h = "### " if md else ""
    print("%sPR size vs %s: %d changed lines in %d files (+%d / -%d), budget %d -> %s" % (
        h, a.base, r["changed_lines"], r["code_files"], r["added"], r["deleted"], r["budget"], r["verdict"].upper()))
    if r["generated_files"]:
        print("Generated or lock files counted apart: %d files, %d lines (list them in the PR description)" % (r["generated_files"], r["generated_lines"]))
    if r["binary_files"]:
        print("Binary files: %d" % r["binary_files"])
    print("\n%sAreas touched" % h)
    for name, ar in r["areas"].items():
        print("%s %-40s %6d lines  %3d files" % ("-" if md else " ", name, ar["lines"], ar["files"]))
    print("\n%sLargest files" % h)
    for f in r["largest"]:
        print("%s %-60s +%d -%d" % ("-" if md else " ", f["path"], f["added"], f["deleted"]))
    if r["verdict"] in ("large", "too large"):
        print("\n%sSplit suggestion" % h)
        print("Over budget. Candidate PRs, one per area (refactors and renames first, behaviour changes next):")
        acc, n = 0, 1
        for name, ar in r["areas"].items():
            print("  PR %d: %s (%d lines)" % (n, name, ar["lines"]))
            n += 1
            acc += ar["lines"]
        print("If one area alone exceeds the budget, slice it vertically behind a feature flag.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

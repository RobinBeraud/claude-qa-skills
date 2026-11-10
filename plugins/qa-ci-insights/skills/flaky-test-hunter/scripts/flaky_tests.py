#!/usr/bin/env python3
"""Detect flaky tests from several JUnit XML reports (one per CI run). Stdlib only.

Usage: python flaky_tests.py <folder-or-files...> [--min-runs 3] [--format md|csv|json]
Runs are ordered by path name. A run is one XML file, or one sub-folder holding several XML files.
A test is flaky when it both passed and failed across runs. Exit code 0 always (report tool).
"""
import argparse
import csv
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict


def runs_from(paths):
    runs = []
    for p in paths:
        if os.path.isdir(p):
            entries = sorted(os.listdir(p))
            subdirs = [e for e in entries if os.path.isdir(os.path.join(p, e))]
            if subdirs:
                for d in subdirs:
                    files = [os.path.join(p, d, f) for f in sorted(os.listdir(os.path.join(p, d))) if f.endswith(".xml")]
                    if files:
                        runs.append((d, files))
            else:
                runs += [(f, [os.path.join(p, f)]) for f in entries if f.endswith(".xml")]
        else:
            runs.append((os.path.basename(p), [p]))
    return runs


def results(files):
    out = {}
    for f in files:
        try:
            root = ET.parse(f).getroot()
        except ET.ParseError:
            print("skip unreadable %s" % f, file=sys.stderr)
            continue
        for tc in root.iter("testcase"):
            name = "%s::%s" % (tc.get("classname", ""), tc.get("name", ""))
            status, msg = "pass", ""
            for tag in ("failure", "error"):
                el = tc.find(tag)
                if el is not None:
                    status = "fail"
                    msg = (el.get("message") or (el.text or "")).strip().splitlines()[0][:160] if (el.get("message") or el.text) else tag
            if tc.find("skipped") is not None:
                status = "skip"
            # a test reported twice in one run (retries): any pass counts as "flaky inside the run"
            prev = out.get(name)
            if prev and prev[0] != status and "skip" not in (prev[0], status):
                status = "flip-in-run"
            out[name] = (status, msg or (prev[1] if prev else ""))
    return out


def normalise(msg):
    return re.sub(r"\d+", "N", msg)


def analyse(runs, min_runs):
    hist = defaultdict(list)
    msgs = defaultdict(Counter)
    for _, files in runs:
        for name, (status, msg) in results(files).items():
            hist[name].append(status)
            if msg and status in ("fail", "flip-in-run"):
                msgs[name][normalise(msg)] += 1
    rows = []
    for name, seq in hist.items():
        seq2 = [s for s in seq if s != "skip"]
        if len(seq2) < min_runs:
            continue
        fails = sum(1 for s in seq2 if s in ("fail", "flip-in-run"))
        passes = sum(1 for s in seq2 if s == "pass")
        in_run = seq2.count("flip-in-run")
        if not (in_run or (fails and passes)):
            continue
        flips = sum(1 for a, b in zip(seq2, seq2[1:]) if a != b)
        rows.append({"test": name, "runs": len(seq2), "failures": fails, "flips": flips,
                     "flip_rate": round(flips / max(1, len(seq2) - 1), 2), "retried_in_run": in_run,
                     "top_message": msgs[name].most_common(1)[0][0] if msgs[name] else ""})
    rows.sort(key=lambda r: (-r["flip_rate"], -r["failures"], r["test"]))
    return rows


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--min-runs", type=int, default=3)
    ap.add_argument("--format", choices=["md", "csv", "json"], default="md")
    a = ap.parse_args(argv)
    runs = runs_from(a.paths)
    rows = analyse(runs, a.min_runs)
    if a.format == "json":
        json.dump(rows, sys.stdout, indent=2)
        print()
    elif a.format == "csv":
        w = csv.DictWriter(sys.stdout, fieldnames=["test", "runs", "failures", "flips", "flip_rate", "retried_in_run", "top_message"])
        w.writeheader()
        w.writerows(rows)
    else:
        print("%d run(s) analysed, %d flaky test(s)\n" % (len(runs), len(rows)))
        if rows:
            print("| Test | Runs | Failures | Flips | Flip rate | Retried in run | Most frequent message |")
            print("|---|---|---|---|---|---|---|")
            for r in rows:
                print("| %s | %d | %d | %d | %.2f | %d | %s |" % (r["test"], r["runs"], r["failures"], r["flips"],
                                                                r["flip_rate"], r["retried_in_run"], r["top_message"].replace("|", "/")))
    return 0


if __name__ == "__main__":
    sys.exit(main())

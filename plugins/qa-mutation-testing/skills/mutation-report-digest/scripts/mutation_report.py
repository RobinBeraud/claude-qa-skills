#!/usr/bin/env python3
"""Digest a mutation testing report. Stdlib only.

Supports the Stryker JSON format (mutation-testing-report-schema: StrykerJS, Stryker.NET, Stryker4s)
and PIT mutations.xml. Usage: python mutation_report.py <report.json|mutations.xml> [--top 15]
Score = detected / (detected + undetected), detected = Killed + Timeout, undetected = Survived + NoCoverage
(CompileError, RuntimeError and Ignored mutants are excluded).
"""
import argparse
import json
import sys
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict

if hasattr(sys.stdout, "reconfigure"):  # Windows consoles default to a legacy code page
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DETECTED = {"Killed", "Timeout"}
UNDETECTED = {"Survived", "NoCoverage"}


def from_stryker(data):
    out = []
    for path, f in data.get("files", {}).items():
        src = f.get("source", "").splitlines()
        for m in f.get("mutants", []):
            line = m.get("location", {}).get("start", {}).get("line", 0)
            out.append({"file": path, "line": line, "status": m.get("status", "?"),
                        "mutator": m.get("mutatorName", "?"), "replacement": m.get("replacement", ""),
                        "code": src[line - 1].strip() if 0 < line <= len(src) else ""})
    return out


def from_pit(root):
    status_map = {"KILLED": "Killed", "SURVIVED": "Survived", "NO_COVERAGE": "NoCoverage", "TIMED_OUT": "Timeout",
                  "MEMORY_ERROR": "Killed", "RUN_ERROR": "RuntimeError", "NON_VIABLE": "CompileError"}
    out = []
    for m in root.iter("mutation"):
        mut = (m.findtext("mutator") or "?").split(".")[-1]
        out.append({"file": m.findtext("sourceFile") or "?", "line": int(m.findtext("lineNumber") or 0),
                    "status": status_map.get(m.get("status", ""), m.get("status", "?")), "mutator": mut,
                    "replacement": m.findtext("description") or "", "code": ""})
    return out


def load(path):
    if path.lower().endswith(".xml"):
        return from_pit(ET.parse(path).getroot())
    with open(path, encoding="utf-8") as fh:
        return from_stryker(json.load(fh))


def score(muts):
    d = sum(1 for m in muts if m["status"] in DETECTED)
    u = sum(1 for m in muts if m["status"] in UNDETECTED)
    return (100.0 * d / (d + u)) if d + u else None, d, u


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("report")
    ap.add_argument("--top", type=int, default=15)
    a = ap.parse_args(argv)
    muts = load(a.report)
    if not muts:
        print("no mutant found in %s" % a.report)
        return 1
    total, d, u = score(muts)
    status = Counter(m["status"] for m in muts)
    print("## Mutation report digest\n")
    print("Mutation score: **%.1f %%** (%d detected, %d undetected, %d mutants in total)" % (total or 0, d, u, len(muts)))
    print("Statuses: " + ", ".join("%s %d" % kv for kv in status.most_common()) + "\n")
    by_file = defaultdict(list)
    for m in muts:
        by_file[m["file"]].append(m)
    rows = []
    for f, ms in by_file.items():
        s, fd, fu = score(ms)
        rows.append((fu, f, s, sum(1 for m in ms if m["status"] == "Survived"), sum(1 for m in ms if m["status"] == "NoCoverage")))
    rows.sort(key=lambda r: (-r[0], r[1]))
    print("| File | Score | Survived | No coverage |\n|---|---|---|---|")
    for fu, f, s, sv, nc in rows[:a.top]:
        print("| %s | %s | %d | %d |" % (f, ("%.0f %%" % s) if s is not None else "-", sv, nc))
    mut = Counter(m["mutator"] for m in muts if m["status"] in UNDETECTED)
    if mut:
        print("\n### Undetected mutants by mutator\n")
        for k, v in mut.most_common():
            print("- %s: %d" % (k, v))
    surv = [m for m in muts if m["status"] in UNDETECTED]
    surv.sort(key=lambda m: (m["file"], m["line"]))
    if surv:
        print("\n### First undetected mutants\n")
        for m in surv[:a.top]:
            detail = ("`%s` -> `%s`" % (m["code"], m["replacement"])) if m["code"] else m["replacement"]
            print("- %s:%d [%s, %s] %s" % (m["file"], m["line"], m["status"], m["mutator"], detail))
    return 0


if __name__ == "__main__":
    sys.exit(main())

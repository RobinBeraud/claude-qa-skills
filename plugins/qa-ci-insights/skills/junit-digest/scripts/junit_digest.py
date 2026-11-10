#!/usr/bin/env python3
"""Digest JUnit/xUnit XML reports: totals, failures grouped by message, slowest tests and suites. Stdlib only.

Usage: python junit_digest.py <files-or-folders...> [--top 10]
Exit code 1 when at least one failure or error is present (usable as a CI gate).
"""
import argparse
import os
import re
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict


def files_of(paths):
    out = []
    for p in paths:
        if os.path.isdir(p):
            for root, _, fs in os.walk(p):
                out += [os.path.join(root, f) for f in sorted(fs) if f.endswith(".xml")]
        else:
            out.append(p)
    return out


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


def first_line(el, tag):
    text = el.get("message") or el.text or tag
    return text.strip().splitlines()[0][:200] if text.strip() else tag


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--top", type=int, default=10)
    a = ap.parse_args(argv)
    total = passed = failed = errors = skipped = 0
    duration = 0.0
    groups = defaultdict(list)
    tests, suites = [], defaultdict(float)
    for f in files_of(a.paths):
        try:
            root = ET.parse(f).getroot()
        except ET.ParseError:
            print("skip unreadable %s" % f, file=sys.stderr)
            continue
        for tc in root.iter("testcase"):
            total += 1
            t = num(tc.get("time"))
            duration += t
            name = "%s::%s" % (tc.get("classname", ""), tc.get("name", ""))
            tests.append((t, name))
            suites[tc.get("classname", "") or os.path.basename(f)] += t
            fail, err = tc.find("failure"), tc.find("error")
            if fail is not None or err is not None:
                el = fail if fail is not None else err
                if fail is not None:
                    failed += 1
                else:
                    errors += 1
                key = re.sub(r"0x[0-9a-fA-F]+|\d+", "N", first_line(el, "failure"))
                groups[key].append(name)
            elif tc.find("skipped") is not None:
                skipped += 1
            else:
                passed += 1
    print("## Test digest\n")
    print("| Tests | Passed | Failed | Errors | Skipped | Duration |")
    print("|---|---|---|---|---|---|")
    print("| %d | %d | %d | %d | %d | %.1f s |\n" % (total, passed, failed, errors, skipped, duration))
    if groups:
        print("### Failures grouped by message (%d group(s))\n" % len(groups))
        for key, names in sorted(groups.items(), key=lambda kv: -len(kv[1])):
            print("- **%d x** `%s`" % (len(names), key))
            for n in names[:5]:
                print("  - %s" % n)
            if len(names) > 5:
                print("  - ... and %d more" % (len(names) - 5))
        print()
    print("### Slowest tests\n")
    for t, n in sorted(tests, reverse=True)[:a.top]:
        print("- %.2f s  %s" % (t, n))
    print("\n### Slowest suites\n")
    for n, t in sorted(suites.items(), key=lambda kv: -kv[1])[:a.top]:
        print("- %.2f s  %s" % (t, n))
    return 1 if failed or errors else 0


if __name__ == "__main__":
    sys.exit(main())

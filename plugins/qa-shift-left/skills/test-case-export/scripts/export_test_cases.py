#!/usr/bin/env python3
"""Convert test cases (JSON or Markdown) to CSV for Azure DevOps Test Plans or Jira Xray. Stdlib only.

JSON: [{"title": ..., "priority": 2, "area": "...", "steps": [{"action": ..., "expected": ...}]}]
Markdown: '## <title>' per test, optional 'Priority: 2' / 'Area: X' lines, then a table
          '| Action | Expected |' (header and separator rows are skipped).
Usage: python export_test_cases.py cases.json|cases.md --target azure|xray > out.csv
"""
import argparse
import csv
import json
import re
import sys

if hasattr(sys.stdout, "reconfigure"):  # Windows consoles default to a legacy code page
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def parse_markdown(text):
    cases, cur, header_seen = [], None, False
    for line in text.splitlines():
        m = re.match(r"^##\s+(.*)", line)
        if m:
            cur = {"title": m.group(1).strip(), "priority": "", "area": "", "steps": []}
            cases.append(cur)
            header_seen = False
            continue
        if cur is None:
            continue
        m = re.match(r"^\s*(Priority|Area)\s*:\s*(.*)$", line, re.I)
        if m:
            cur[m.group(1).lower()] = m.group(2).strip()
            continue
        if line.strip().startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
                continue
            if not header_seen:
                header_seen = True
                if cells and cells[0].lower() in ("action", "step", "steps"):
                    continue
            if len(cells) >= 2:
                cur["steps"].append({"action": cells[0], "expected": cells[1]})
    return cases


def load(path):
    text = open(path, encoding="utf-8").read()
    if path.lower().endswith(".json"):
        return json.loads(text)
    return parse_markdown(text)


def to_azure(cases, out):
    w = csv.writer(out)
    w.writerow(["ID", "Work Item Type", "Title", "Test Step", "Step Action", "Step Expected",
                "Priority", "Area Path"])
    for c in cases:
        steps = c.get("steps") or [{"action": "", "expected": ""}]
        for i, s in enumerate(steps, 1):
            first = i == 1
            w.writerow(["", "Test Case" if first else "", c["title"] if first else "", i,
                        s.get("action", ""), s.get("expected", ""),
                        c.get("priority", "") if first else "", c.get("area", "") if first else ""])


def to_xray(cases, out):
    w = csv.writer(out)
    w.writerow(["Test ID", "Summary", "Priority", "Action", "Data", "Expected Result"])
    for n, c in enumerate(cases, 1):
        for s in c.get("steps") or [{"action": "", "expected": ""}]:
            w.writerow([n, c["title"], c.get("priority", ""), s.get("action", ""), s.get("data", ""),
                        s.get("expected", "")])


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--target", choices=["azure", "xray"], default="azure")
    a = ap.parse_args(argv)
    cases = load(a.file)
    if not cases:
        print("no test case found", file=sys.stderr)
        return 1
    (to_azure if a.target == "azure" else to_xray)(cases, sys.stdout)
    print("%d test case(s), %d step(s) exported for %s" % (len(cases), sum(len(c.get('steps', [])) for c in cases),
                                                          a.target), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())

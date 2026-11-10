#!/usr/bin/env python3
"""Lint Gherkin .feature files for common BDD smells (stdlib only).

Usage: python gherkin_lint.py <file-or-folder> [...]
Errors: scenario without When / Then, outline without Examples, placeholder missing from Examples.
Warnings: several When, UI-level steps, vague outcomes, duplicate scenario names, long steps,
          When inside Background.
Exit code 1 when at least one error is found.
"""
import os
import re
import sys

UI_WORDS = re.compile(r"\b(click|clicks|clicked|button|type[sd]? into|scroll|tab|dropdown|checkbox|"
                      r"navigate to|page|field|textbox|xpath|css)\b", re.I)
VAGUE = re.compile(r"\b(correctly|properly|works|as expected|appropriate|should work|etc\.?|ok)\b", re.I)
STEP = re.compile(r"^\s*(Given|When|Then|And|But|\*)\s+(.*)$")
HEAD = re.compile(r"^\s*(Feature|Rule|Background|Scenario Outline|Scenario Template|Scenario|Example|Examples|Scenarios):\s*(.*)$")


def lint_file(path):
    issues = []
    lines = open(path, encoding="utf-8").read().splitlines()
    blocks, cur = [], None
    for no, raw in enumerate(lines, 1):
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith("@"):
            continue
        h = HEAD.match(line)
        if h:
            kind = h.group(1)
            if kind in ("Examples", "Scenarios"):
                if cur is not None:
                    cur["examples"] = True
                    cur["in_examples"] = True
                continue
            if kind in ("Feature", "Rule"):
                cur = None
                continue
            cur = {"kind": kind, "name": h.group(2), "line": no, "steps": [], "examples": False,
                   "in_examples": False, "header": None}
            blocks.append(cur)
            continue
        if cur is None:
            continue
        if cur.get("in_examples") and line.startswith("|"):
            if cur["header"] is None:
                cur["header"] = [c.strip() for c in line.strip("|").split("|")]
            continue
        s = STEP.match(line)
        if s:
            cur["in_examples"] = False
            cur["steps"].append((no, s.group(1), s.group(2)))

    names = {}
    for b in blocks:
        where = "%s:%d" % (path, b["line"])
        if b["kind"] == "Background":
            if any(k == "When" for _, k, _ in b["steps"]):
                issues.append(("WARN", where, "Background contains a When: keep it to Given steps"))
            continue
        effective, last = [], None
        for no, k, text in b["steps"]:
            kk = last if k in ("And", "But", "*") and last else k
            effective.append((no, kk, text, k))
            if k in ("Given", "When", "Then"):
                last = k
        whens = [e for e in effective if e[1] == "When"]
        thens = [e for e in effective if e[1] == "Then"]
        if not whens:
            issues.append(("ERROR", where, "scenario '%s' has no When step" % b["name"]))
        elif len(whens) > 1:
            issues.append(("WARN", where, "scenario '%s' has %d When/And-actions: one behaviour per scenario"
                           % (b["name"], len(whens))))
        if not thens:
            issues.append(("ERROR", where, "scenario '%s' has no Then step" % b["name"]))
        for no, kk, text, k in effective:
            if UI_WORDS.search(text):
                issues.append(("WARN", "%s:%d" % (path, no), "UI-level step, describe behaviour instead: '%s'" % text))
            if kk == "Then" and VAGUE.search(text):
                issues.append(("WARN", "%s:%d" % (path, no), "vague outcome, use an observable value: '%s'" % text))
            if len(text) > 120:
                issues.append(("WARN", "%s:%d" % (path, no), "step longer than 120 characters"))
        if b["kind"] in ("Scenario Outline", "Scenario Template"):
            if not b["examples"]:
                issues.append(("ERROR", where, "outline '%s' has no Examples table" % b["name"]))
            else:
                used = set(re.findall(r"<([^>]+)>", " ".join(t for _, _, t in b["steps"]) + " " + b["name"]))
                header = set(b["header"] or [])
                for ph in sorted(used - header):
                    issues.append(("ERROR", where, "placeholder <%s> not in Examples header" % ph))
        key = b["name"].strip().lower()
        if key in names:
            issues.append(("WARN", where, "duplicate scenario name (also line %d)" % names[key]))
        names[key] = b["line"]
    return issues


def main(argv):
    targets = argv or ["."]
    files = []
    for t in targets:
        if os.path.isdir(t):
            for root, _, fs in os.walk(t):
                files += [os.path.join(root, f) for f in fs if f.endswith(".feature")]
        else:
            files.append(t)
    all_issues = []
    for f in sorted(files):
        all_issues += lint_file(f)
    for level, where, msg in all_issues:
        print("%s %s %s" % (where, level, msg))
    errors = sum(1 for i in all_issues if i[0] == "ERROR")
    print("%d file(s), %d error(s), %d warning(s)" % (len(files), errors, len(all_issues) - errors))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

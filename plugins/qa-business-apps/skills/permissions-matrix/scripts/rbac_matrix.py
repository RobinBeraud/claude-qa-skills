#!/usr/bin/env python3
"""Generate RBAC test cases from a roles x actions matrix, or compare expected vs observed. Stdlib only.

Matrix CSV: first column 'action', one column per role, cells 'allow' or 'deny' (also yes/no, 1/0, x/-).
  python rbac_matrix.py generate matrix.csv            -> Markdown test cases
  python rbac_matrix.py compare  matrix.csv observed.csv -> mismatches, exit 1 if any
"""
import argparse
import csv
import sys

if hasattr(sys.stdout, "reconfigure"):  # Windows consoles default to a legacy code page
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ALLOW = {"allow", "yes", "y", "1", "x", "true", "oui", "o"}
DENY = {"deny", "no", "n", "0", "-", "false", "non", ""}


def load(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f))
    header, body = rows[0], rows[1:]
    roles = [h.strip() for h in header[1:]]
    matrix = {}
    for r in body:
        if not r or not r[0].strip():
            continue
        action = r[0].strip()
        for role, cell in zip(roles, r[1:] + [""] * (len(roles) - len(r[1:]))):
            v = cell.strip().lower()
            if v in ALLOW:
                matrix[(role, action)] = True
            elif v in DENY:
                matrix[(role, action)] = False
            else:
                raise SystemExit("unreadable cell '%s' for %s / %s" % (cell, role, action))
    return roles, matrix


def generate(path):
    roles, m = load(path)
    print("# Permission test cases (%d roles, %d checks)\n" % (len(roles), len(m)))
    n = 0
    for role in roles:
        print("## Role: %s\n" % role)
        print("| # | Action | Expected | UI check | API check |\n|---|---|---|---|---|")
        for (r, action), allowed in sorted(m.items(), key=lambda kv: kv[0][1]):
            if r != role:
                continue
            n += 1
            if allowed:
                print("| %d | %s | ALLOWED | action visible and succeeds | request succeeds (2xx), change persisted |" % (n, action))
            else:
                print("| %d | %s | DENIED | action hidden or disabled; direct URL refused | 403 (or 404), nothing persisted, attempt logged |" % (n, action))
        print()
    return 0


def compare(expected_path, observed_path):
    roles_e, exp = load(expected_path)
    roles_o, obs = load(observed_path)
    issues = 0
    for key, should in sorted(exp.items()):
        if key not in obs:
            print("MISSING     %-15s %-30s not tested" % key)
            issues += 1
            continue
        if obs[key] != should:
            kind = "SECURITY  " if obs[key] and not should else "FUNCTIONAL"
            print("%s  %-15s %-30s expected %s, observed %s" % (kind, key[0], key[1],
                                                              "allow" if should else "deny", "allow" if obs[key] else "deny"))
            issues += 1
    print("\n%d check(s), %d issue(s)" % (len(exp), issues))
    return 1 if issues else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("generate")
    g.add_argument("matrix")
    c = sub.add_parser("compare")
    c.add_argument("expected")
    c.add_argument("observed")
    a = ap.parse_args(argv)
    return generate(a.matrix) if a.cmd == "generate" else compare(a.expected, a.observed)


if __name__ == "__main__":
    sys.exit(main())

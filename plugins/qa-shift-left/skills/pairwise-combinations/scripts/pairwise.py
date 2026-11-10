#!/usr/bin/env python3
"""Greedy all-pairs (pairwise) test set generator, stdlib only.

Input JSON: {"parameters": {"name": [values...], ...},
             "exclude": [{"param": value, "other": value}, ...],   # optional constraints
             "seed": 1}                                            # optional
Usage: python pairwise.py params.json [--format md|csv|json] [--tries 60]
Exit code 1 if a reachable pair is left uncovered (should not happen).
"""
import argparse
import csv
import itertools
import json
import random
import sys

if hasattr(sys.stdout, "reconfigure"):  # Windows consoles default to a legacy code page
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def violates(row, rules):
    for rule in rules:
        if all(k in row and row[k] == v for k, v in rule.items()):
            return True
    return False


def all_pairs(params, rules):
    names = list(params)
    pairs, impossible = set(), set()
    for i, j in itertools.combinations(range(len(names)), 2):
        a, b = names[i], names[j]
        for va in params[a]:
            for vb in params[b]:
                p = ((a, va), (b, vb))
                if violates({a: va, b: vb}, rules):
                    impossible.add(p)
                else:
                    pairs.add(p)
    return pairs, impossible


def pairs_of(row, names):
    out = set()
    for i, j in itertools.combinations(range(len(names)), 2):
        a, b = names[i], names[j]
        out.add(((a, row[a]), (b, row[b])))
    return out


def build_row(params, rules, uncovered, seed_pair, rnd):
    names = list(params)
    (a, va), (b, vb) = seed_pair
    row = {a: va, b: vb}
    rest = [n for n in names if n not in row]
    rnd.shuffle(rest)
    for n in rest:
        best, best_gain = None, -1
        values = list(params[n])
        rnd.shuffle(values)
        for v in values:
            row[n] = v
            if violates(row, rules):
                del row[n]
                continue
            gain = sum(1 for m in row if m != n and
                       (tuple(sorted([(m, row[m]), (n, v)], key=lambda t: names.index(t[0]))) in uncovered))
            del row[n]
            if gain > best_gain:
                best, best_gain = v, gain
        if best is None:
            return None
        row[n] = best
    return row


def generate(params, rules, seed=1, tries=60):
    names = list(params)
    rnd = random.Random(seed)
    uncovered, impossible = all_pairs(params, rules)
    total = len(uncovered)
    rows = []
    while uncovered:
        best_row, best_gain = None, 0
        ordered = sorted(uncovered, key=lambda p: (names.index(p[0][0]), str(p)))
        seed_pair = ordered[0]
        for _ in range(tries):
            row = build_row(params, rules, uncovered, seed_pair, rnd)
            if row is None:
                continue
            gain = len(pairs_of(row, names) & uncovered)
            if gain > best_gain:
                best_row, best_gain = row, gain
        if best_row is None:
            # seed pair cannot appear in any valid full row (constraint on 3+ parameters)
            impossible.add(seed_pair)
            uncovered.discard(seed_pair)
            total -= 1
            continue
        rows.append({n: best_row[n] for n in names})
        uncovered -= pairs_of(best_row, names)
    return rows, total, impossible


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--format", choices=["md", "csv", "json"], default="md")
    ap.add_argument("--tries", type=int, default=60)
    a = ap.parse_args(argv)
    spec = json.load(open(a.file, encoding="utf-8"))
    params = spec["parameters"]
    rules = spec.get("exclude", [])
    rows, covered, impossible = generate(params, rules, spec.get("seed", 1), a.tries)
    full = 1
    for v in params.values():
        full *= len(v)
    names = list(params)
    check = set().union(*(pairs_of(r, names) for r in rows)) if rows else set()
    reachable, _ = all_pairs(params, rules)
    missing = reachable - check - impossible
    if a.format == "json":
        json.dump(rows, sys.stdout, ensure_ascii=False, indent=2)
        print()
    elif a.format == "csv":
        w = csv.DictWriter(sys.stdout, fieldnames=names)
        w.writeheader()
        w.writerows(rows)
    else:
        print("| # | " + " | ".join(names) + " |")
        print("|---|" + "---|" * len(names))
        for i, r in enumerate(rows, 1):
            print("| %d | %s |" % (i, " | ".join(str(r[n]) for n in names)))
    print("\n%d rows instead of %d (full product); %d pairs covered; %d impossible pairs excluded by constraints"
          % (len(rows), full, covered, len(impossible)), file=sys.stderr)
    if missing:
        print("UNCOVERED pairs: %s" % sorted(missing), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

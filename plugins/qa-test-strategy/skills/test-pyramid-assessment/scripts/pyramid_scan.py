#!/usr/bin/env python3
"""Measure the shape of a repository's test suite (unit / integration-api / e2e). Stdlib only.

Usage: python pyramid_scan.py [repo_dir] [--format md|json]
Heuristic: files are found by test naming conventions; each file is classified e2e if it imports a
browser/E2E tool or lives under an e2e folder, integration/api if it uses HTTP clients, test
containers or databases or lives under integration/api folders, unit otherwise. Test cases are
counted with language-specific patterns. Check a sample before concluding.
"""
import argparse
import json
import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):  # Windows consoles default to a legacy code page
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SKIP_DIRS = {".git", "node_modules", "dist", "build", "target", "bin", "obj", ".venv", "venv", "vendor",
             "__pycache__", ".next", "coverage", ".gradle", ".idea"}
TEST_FILE = re.compile(r"(^test_.*\.py$|.*_test\.py$|.*\.(test|spec)\.(js|jsx|ts|tsx|mjs|cjs)$|.*(Test|Tests|IT|Spec)\.(java|kt|cs)$|.*_test\.go$|.*Test\.php$|.*\.feature$|.*\.cy\.(js|ts)$)")
E2E = re.compile(r"(@playwright/test|playwright|cypress|selenium|webdriver|appium|puppeteer|testcafe|nightwatch|from\s+splinter|Microsoft\.Playwright|OpenQA\.Selenium)", re.I)
INTEG = re.compile(r"(supertest|requests\.|httpx|TestClient|WebApplicationFactory|MockMvc|RestAssured|testcontainers|Testcontainers|sqlalchemy|psycopg|pymysql|SqlConnection|DbContext|@SpringBootTest|@DataJpaTest|HttpClient|axios|fetch\(|wiremock|WireMock|pact|nock\()", re.I)
CASE_PATTERNS = {
    ".py": re.compile(r"^\s*(async\s+)?def\s+test_", re.M),
    ".js": re.compile(r"\b(it|test)(\.each\([^)]*\))?\s*\(", re.M),
    ".java": re.compile(r"@(Test|ParameterizedTest|RepeatedTest)\b"),
    ".kt": re.compile(r"@(Test|ParameterizedTest)\b"),
    ".cs": re.compile(r"\[(Fact|Theory|Test|TestCase|TestMethod)[\](]"),
    ".go": re.compile(r"^func\s+Test\w+\(", re.M),
    ".php": re.compile(r"(function\s+test\w+|@test)"),
    ".feature": re.compile(r"^\s*Scenario( Outline)?:", re.M),
}
for ext in (".jsx", ".ts", ".tsx", ".mjs", ".cjs"):
    CASE_PATTERNS[ext] = CASE_PATTERNS[".js"]


def classify(path, text):
    p = path.replace("\\", "/").lower()
    if path.endswith(".feature") or "/e2e/" in p or "/end-to-end/" in p or p.endswith((".cy.js", ".cy.ts")) or E2E.search(text):
        return "e2e"
    if re.search(r"/(integration|integration-tests|it|api|component|contract)s?/", p) or p.endswith("it.java") or INTEG.search(text):
        return "integration"
    return "unit"


def scan(root):
    levels = {k: {"files": 0, "cases": 0} for k in ("unit", "integration", "e2e")}
    samples = {k: [] for k in levels}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
        for fn in filenames:
            if not TEST_FILE.match(fn):
                continue
            full = os.path.join(dirpath, fn)
            try:
                text = open(full, encoding="utf-8", errors="ignore").read()
            except OSError:
                continue
            ext = os.path.splitext(fn)[1].lower()
            level = classify(os.path.relpath(full, root), text)
            pat = CASE_PATTERNS.get(ext)
            cases = len(pat.findall(text)) if pat else 0
            levels[level]["files"] += 1
            levels[level]["cases"] += max(cases, 1)
            if len(samples[level]) < 5:
                samples[level].append(os.path.relpath(full, root).replace("\\", "/"))
    return levels, samples


def diagnose(levels):
    total = sum(v["cases"] for v in levels.values())
    if not total:
        return "No test found."
    u, i, e = (100.0 * levels[k]["cases"] / total for k in ("unit", "integration", "e2e"))
    if e >= u:
        return "Ice-cream cone: as many or more end-to-end cases than unit cases. Push logic checks down to unit and API level."
    if i < 5 and u > 0:
        return "Missing middle: almost no integration/API tests. Units may pass while wiring breaks; add API and contract tests."
    if u >= 60 and e <= 15:
        return "Pyramid shape: most checks at unit level, few end-to-end."
    if i >= u:
        return "Trophy shape: integration-heavy. Fine for thin-logic services; keep complex logic covered by unit tests."
    return "Mixed shape: check whether end-to-end tests duplicate checks that lower levels could do."


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("root", nargs="?", default=".")
    ap.add_argument("--format", choices=["md", "json"], default="md")
    a = ap.parse_args(argv)
    levels, samples = scan(a.root)
    total = sum(v["cases"] for v in levels.values())
    if a.format == "json":
        json.dump({"levels": levels, "samples": samples, "diagnosis": diagnose(levels)}, sys.stdout, indent=2)
        print()
        return 0
    print("## Test pyramid of %s\n" % os.path.abspath(a.root))
    print("| Level | Files | Test cases | Share |\n|---|---|---|---|")
    for k in ("e2e", "integration", "unit"):
        share = 100.0 * levels[k]["cases"] / total if total else 0
        bar = "█" * int(round(share / 5))
        print("| %s | %d | %d | %4.1f %% %s |" % (k, levels[k]["files"], levels[k]["cases"], share, bar))
    print("\n**Diagnosis**: %s\n" % diagnose(levels))
    print("Sample files per level (verify the heuristic):")
    for k, v in samples.items():
        if v:
            print("- %s: %s" % (k, ", ".join(v)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Unit tests for the bundled skill scripts. Run: python -m unittest discover -s tests -v (stdlib only)."""
import contextlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(rel):
    path = os.path.join(ROOT, "plugins", rel)
    spec = importlib.util.spec_from_file_location(os.path.basename(path)[:-3], path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run(mod, argv):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = mod.main(argv)
    return code, out.getvalue(), err.getvalue()


def write(d, name, text):
    p = os.path.join(d, name)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(text)
    return p


class FrTestData(unittest.TestCase):
    m = load("qa-shift-left/skills/test-data-fr/scripts/fr_test_data.py")

    def test_known_identifiers(self):
        self.assertEqual(self.m.validate("732829320"), ("SIREN", True))
        self.assertEqual(self.m.validate("FR44732829320"), ("VAT FR", True))
        self.assertEqual(self.m.validate("FR7630006000011234567890189"), ("IBAN", True))
        self.assertEqual(self.m.validate("123456789")[1], False)

    def test_generated_companies_are_valid_and_deterministic(self):
        code, out1, _ = run(self.m, ["companies", "--count", "25", "--seed", "3", "--format", "json"])
        _, out2, _ = run(self.m, ["companies", "--count", "25", "--seed", "3", "--format", "json"])
        self.assertEqual(out1, out2)
        for c in json.loads(out1):
            for key in ("siren", "siret", "vat_number", "iban"):
                self.assertTrue(self.m.validate(c[key])[1], (key, c[key]))
            self.assertTrue(c["siret"].startswith(c["siren"]))

    def test_invoice_rounding(self):
        _, out, _ = run(self.m, ["invoices", "--count", "40", "--format", "json"])
        from decimal import Decimal, ROUND_HALF_UP
        for inv in json.loads(out):
            net, rate = Decimal(inv["net"]), Decimal(inv["vat_rate"]) / 100
            self.assertEqual(Decimal(inv["vat"]), (net * rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
            self.assertEqual(Decimal(inv["gross"]), net + Decimal(inv["vat"]))


class Pairwise(unittest.TestCase):
    m = load("qa-shift-left/skills/pairwise-combinations/scripts/pairwise.py")

    def test_all_pairs_covered_with_constraints(self):
        params = {"browser": ["Chrome", "Firefox", "Safari"], "os": ["Win", "Mac", "Linux"],
                  "role": ["a", "b", "c", "d"], "lang": ["fr", "es"]}
        rules = [{"browser": "Safari", "os": "Win"}, {"browser": "Safari", "os": "Linux"}]
        rows, covered, impossible = self.m.generate(params, rules, seed=2)
        names = list(params)
        got = set().union(*(self.m.pairs_of(r, names) for r in rows))
        reachable, _ = self.m.all_pairs(params, rules)
        self.assertEqual(reachable - got, set())
        self.assertFalse(any(self.m.violates(r, rules) for r in rows))
        self.assertLess(len(rows), 3 * 3 * 4 * 2)


class GherkinLint(unittest.TestCase):
    m = load("qa-shift-left/skills/gherkin-scenarios/scripts/gherkin_lint.py")

    def test_detects_smells(self):
        with tempfile.TemporaryDirectory() as d:
            write(d, "a.feature", """Feature: Fees
  Scenario: Click
    Given I am on the invoices page
    When I click the Pay button
    And I click Confirm
    Then it works correctly
  Scenario Outline: Fee
    Given an invoice of <amount> EUR
    When the job runs
    Then the fee is <fee>
  Scenario: No outcome
    Given an invoice
    When the job runs
""")
            code, out, _ = run(self.m, [d])
        self.assertEqual(code, 1)
        self.assertIn("UI-level step", out)
        self.assertIn("vague outcome", out)
        self.assertIn("has no Examples table", out)
        self.assertIn("has no Then step", out)
        self.assertIn("2 When/And-actions", out)

    def test_clean_file_passes(self):
        with tempfile.TemporaryDirectory() as d:
            write(d, "b.feature", """Feature: Fees
  Scenario Outline: Fee depends on days overdue
    Given an unpaid invoice of <amount> EUR due on 2026-03-31
    When the fee job runs on <run_date>
    Then the late fee is <fee> EUR
    Examples:
      | amount | run_date   | fee   |
      | 100.00 | 2026-04-01 | 40.00 |
""")
            code, out, _ = run(self.m, [d])
        self.assertEqual(code, 0, out)


class ExportCases(unittest.TestCase):
    m = load("qa-shift-left/skills/test-case-export/scripts/export_test_cases.py")

    def test_markdown_to_azure(self):
        with tempfile.TemporaryDirectory() as d:
            p = write(d, "c.md", """## Late fee applied
Priority: 2
| Action | Expected |
|---|---|
| Create invoice | Saved |
| Run job | Fee added |
""")
            code, out, _ = run(self.m, [p, "--target", "azure"])
        lines = out.strip().splitlines()
        self.assertEqual(code, 0)
        self.assertTrue(lines[0].startswith("ID,Work Item Type,Title,Test Step"))
        self.assertIn("Test Case,Late fee applied,1,Create invoice,Saved,2", lines[1])
        self.assertIn(",,,2,Run job,Fee added", lines[2])


JUNIT = """<testsuite name="s">
  <testcase classname="Billing" name="fee" time="{t}">{fee}</testcase>
  <testcase classname="Billing" name="stable" time="0.1"/>
</testsuite>"""


class Flaky(unittest.TestCase):
    m = load("qa-ci-insights/skills/flaky-test-hunter/scripts/flaky_tests.py")

    def test_flip_detection(self):
        with tempfile.TemporaryDirectory() as d:
            for i, fail in enumerate([False, True, False, True]):
                write(d, "run%d.xml" % i, JUNIT.format(t=1, fee='<failure message="Timeout 3000ms"/>' if fail else ""))
            code, out, _ = run(self.m, [d, "--format", "json"])
        rows = json.loads(out)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["test"], "Billing::fee")
        self.assertEqual(rows[0]["flips"], 3)
        self.assertEqual(rows[0]["top_message"], "Timeout Nms")


class Digest(unittest.TestCase):
    m = load("qa-ci-insights/skills/junit-digest/scripts/junit_digest.py")

    def test_groups_and_exit_code(self):
        with tempfile.TemporaryDirectory() as d:
            write(d, "r.xml", JUNIT.format(t=2, fee='<failure message="expected 40 got 39"/>'))
            code, out, _ = run(self.m, [d])
        self.assertEqual(code, 1)
        self.assertIn("| 2 | 1 | 1 | 0 | 0 |", out)
        self.assertIn("expected N got N", out)


class QaMetrics(unittest.TestCase):
    m = load("qa-release/skills/qa-flow-metrics/scripts/qa_metrics.py")

    def test_monthly_flow_and_backlog(self):
        csv_text = ("ID;Work Item Type;Created Date;Closed Date;State;Severity;Found In\n"
                    "1;Bug;2026-01-05;2026-01-15;Closed;2 - High;Production\n"
                    "2;Bug;12/01/2026;;Active;3 - Medium;Test\n"
                    "3;Product Backlog Item;2026-01-07;;New;;\n"
                    "4;Bug;2026-02-02;2026-02-03;Closed;2 - High;Test\n")
        with tempfile.TemporaryDirectory() as d:
            p = write(d, "e.csv", csv_text)
            code, out, _ = run(self.m, [p, "--type", "Work Item Type", "--created", "Created Date", "--closed", "Closed Date",
                                        "--state", "State", "--severity", "Severity", "--found-in", "Found In",
                                        "--prod-values", "Production", "--as-of", "2026-03-01"])
        self.assertEqual(code, 0)
        self.assertIn("| 2026-01 | 2 | 1 | +1 | 10 | 1 | 50 % |", out)
        self.assertIn("| 2026-02 | 1 | 1 | +0 | 1 | 0 | 0 % |", out)
        self.assertIn("## Open bugs on 2026-03-01: 1", out)
        self.assertIn("| 30-90 d | 1 |", out)


CII = """<?xml version="1.0" encoding="UTF-8"?>
<rsm:CrossIndustryInvoice xmlns:rsm="urn:un:unece:uncefact:data:standard:CrossIndustryInvoice:100"
 xmlns:ram="urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100"
 xmlns:udt="urn:un:unece:uncefact:data:standard:UnqualifiedDataType:100">
 <rsm:ExchangedDocument><ram:ID>FAC-1</ram:ID><ram:IssueDateTime><udt:DateTimeString format="102">20260301</udt:DateTimeString></ram:IssueDateTime></rsm:ExchangedDocument>
 <rsm:SupplyChainTradeTransaction>
  <ram:IncludedSupplyChainTradeLineItem><ram:SpecifiedLineTradeSettlement><ram:SpecifiedTradeSettlementLineMonetarySummation><ram:LineTotalAmount>100.00</ram:LineTotalAmount></ram:SpecifiedTradeSettlementLineMonetarySummation></ram:SpecifiedLineTradeSettlement></ram:IncludedSupplyChainTradeLineItem>
  <ram:IncludedSupplyChainTradeLineItem><ram:SpecifiedLineTradeSettlement><ram:SpecifiedTradeSettlementLineMonetarySummation><ram:LineTotalAmount>50.00</ram:LineTotalAmount></ram:SpecifiedTradeSettlementLineMonetarySummation></ram:SpecifiedLineTradeSettlement></ram:IncludedSupplyChainTradeLineItem>
  <ram:ApplicableHeaderTradeAgreement>
   <ram:SellerTradeParty><ram:Name>Alver Conseil SAS</ram:Name><ram:SpecifiedTaxRegistration><ram:ID schemeID="VA">FR44732829320</ram:ID></ram:SpecifiedTaxRegistration></ram:SellerTradeParty>
   <ram:BuyerTradeParty><ram:Name>Lisdan SARL</ram:Name></ram:BuyerTradeParty>
  </ram:ApplicableHeaderTradeAgreement>
  <ram:ApplicableHeaderTradeSettlement>
   <ram:InvoiceCurrencyCode>EUR</ram:InvoiceCurrencyCode>
   <ram:ApplicableTradeTax><ram:CalculatedAmount>30.00</ram:CalculatedAmount><ram:TypeCode>VAT</ram:TypeCode><ram:BasisAmount>150.00</ram:BasisAmount><ram:CategoryCode>S</ram:CategoryCode><ram:RateApplicablePercent>20</ram:RateApplicablePercent></ram:ApplicableTradeTax>
   <ram:SpecifiedTradeSettlementHeaderMonetarySummation>
    <ram:LineTotalAmount>150.00</ram:LineTotalAmount><ram:TaxBasisTotalAmount>150.00</ram:TaxBasisTotalAmount>
    <ram:TaxTotalAmount currencyID="EUR">{tax}</ram:TaxTotalAmount><ram:GrandTotalAmount>180.00</ram:GrandTotalAmount>
    <ram:TotalPrepaidAmount>0.00</ram:TotalPrepaidAmount><ram:DuePayableAmount>180.00</ram:DuePayableAmount>
   </ram:SpecifiedTradeSettlementHeaderMonetarySummation>
  </ram:ApplicableHeaderTradeSettlement>
 </rsm:SupplyChainTradeTransaction>
</rsm:CrossIndustryInvoice>"""


class CiiCheck(unittest.TestCase):
    m = load("qa-business-apps/skills/einvoice-consistency/scripts/cii_check.py")

    def test_consistent_invoice(self):
        with tempfile.TemporaryDirectory() as d:
            code, out, _ = run(self.m, [write(d, "ok.xml", CII.format(tax="30.00"))])
        self.assertEqual(code, 0, out)
        self.assertIn("BR-CO-10  OK", out)

    def test_wrong_tax_total(self):
        with tempfile.TemporaryDirectory() as d:
            code, out, _ = run(self.m, [write(d, "bad.xml", CII.format(tax="29.99"))])
        self.assertEqual(code, 1)
        self.assertIn("BR-CO-14  FAIL", out)
        self.assertIn("BR-CO-15  FAIL", out)

    def test_pdf_with_compressed_xml(self):
        import zlib
        body = zlib.compress(CII.format(tax="30.00").encode())
        pdf = b"%PDF-1.7\n1 0 obj<<>>\nstream\n" + body + b"\nendstream\nendobj\n%%EOF"
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "f.pdf")
            with open(p, "wb") as fh:
                fh.write(pdf)
            code, out, _ = run(self.m, [p])
        self.assertEqual(code, 0, out)


class Rbac(unittest.TestCase):
    m = load("qa-business-apps/skills/permissions-matrix/scripts/rbac_matrix.py")

    def test_compare_flags_security(self):
        with tempfile.TemporaryDirectory() as d:
            e = write(d, "e.csv", "action,admin,viewer\ninvoice.delete,allow,deny\ninvoice.read,allow,allow\n")
            o = write(d, "o.csv", "action,admin,viewer\ninvoice.delete,allow,allow\ninvoice.read,allow,deny\n")
            code, out, _ = run(self.m, ["compare", e, o])
            gcode, gout, _ = run(self.m, ["generate", e])
        self.assertEqual(code, 1)
        self.assertIn("SECURITY", out)
        self.assertIn("FUNCTIONAL", out)
        self.assertEqual(gcode, 0)
        self.assertIn("DENIED", gout)


class CoChange(unittest.TestCase):
    m = load("qa-ci-insights/skills/regression-scope/scripts/co_change.py")

    def test_ranks_related_tests(self):
        with tempfile.TemporaryDirectory() as d:
            def g(*a):
                subprocess.run(["git", "-C", d] + list(a), check=True, capture_output=True)
            g("init", "-q")
            g("config", "user.email", "t@example.com")
            g("config", "user.name", "t")
            write(d, "src/invoice.py", "a=1\n")
            write(d, "tests/test_invoice.py", "x=1\n")
            write(d, "tests/test_export.py", "y=1\n")
            g("add", "-A")
            g("commit", "-qm", "init")
            write(d, "src/invoice.py", "a=2\n")
            write(d, "tests/test_export.py", "y=2\n")
            g("add", "-A")
            g("commit", "-qm", "change together")
            cwd = os.getcwd()
            os.chdir(d)
            try:
                code, out, _ = run(self.m, ["--files", "src/invoice.py"])
            finally:
                os.chdir(cwd)
        self.assertEqual(code, 0)
        self.assertIn("tests/test_invoice.py", out)
        self.assertIn("tests/test_export.py", out)
        self.assertIn("name matches src/invoice.py", out)


if __name__ == "__main__":
    unittest.main()

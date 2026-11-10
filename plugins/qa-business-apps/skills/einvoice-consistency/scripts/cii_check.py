#!/usr/bin/env python3
"""Check the arithmetic and key fields of a UN/CEFACT CII e-invoice (XML) or Factur-X PDF. Stdlib only.

Usage: python cii_check.py invoice.xml|invoice.pdf [--tolerance 0] [--vat-tolerance 0.01]
Implements a subset of EN 16931 business rules (BR-CO-10, 13, 14, 15, 16, 17) plus field presence.
Not a replacement for the official Schematron validation. Exit code 1 when any check fails.
"""
import argparse
import re
import sys
import zlib
import xml.etree.ElementTree as ET
from decimal import Decimal, ROUND_HALF_UP

RAM = "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100"
RSM = "urn:un:unece:uncefact:data:standard:CrossIndustryInvoice:100"
UDT = "urn:un:unece:uncefact:data:standard:UnqualifiedDataType:100"
NS = {"ram": RAM, "rsm": RSM, "udt": UDT}
CENT = Decimal("0.01")


def xml_from_pdf(data):
    """Best effort: find a (possibly Flate-compressed) stream holding a CrossIndustryInvoice."""
    for m in re.finditer(rb"stream\r?\n(.*?)\r?\nendstream", data, re.S):
        raw = m.group(1)
        for candidate in (raw, None):
            try:
                body = candidate if candidate is not None else zlib.decompress(raw)
            except zlib.error:
                continue
            if b"CrossIndustryInvoice" in body:
                start = body.find(b"<?xml")
                return body[start if start >= 0 else 0:]
    return None


def dec(el):
    if el is None or el.text is None:
        return None
    return Decimal(el.text.strip())


def find(root, path):
    return root.find(path, NS)


def check(root, tol, vat_tol=Decimal("0.01")):
    results = []

    def rule(rid, ok, detail):
        results.append((rid, ok, detail))

    hs = "rsm:SupplyChainTradeTransaction/ram:ApplicableHeaderTradeSettlement"
    summ = find(root, hs + "/ram:SpecifiedTradeSettlementHeaderMonetarySummation")
    if summ is None:
        rule("STRUCT", False, "no SpecifiedTradeSettlementHeaderMonetarySummation found (is this CII?)")
        return results

    def s(tag):
        return dec(summ.find("ram:" + tag, NS))

    line_total, allow, charge = s("LineTotalAmount"), s("AllowanceTotalAmount") or Decimal(0), s("ChargeTotalAmount") or Decimal(0)
    basis, grand = s("TaxBasisTotalAmount"), s("GrandTotalAmount")
    prepaid, due = s("TotalPrepaidAmount") or Decimal(0), s("DuePayableAmount")
    tax_totals = [dec(e) for e in summ.findall("ram:TaxTotalAmount", NS)]
    tax_total = tax_totals[0] if tax_totals else None

    lines = root.findall("rsm:SupplyChainTradeTransaction/ram:IncludedSupplyChainTradeLineItem", NS)
    line_amounts = [dec(l.find("ram:SpecifiedLineTradeSettlement/ram:SpecifiedTradeSettlementLineMonetarySummation/ram:LineTotalAmount", NS)) for l in lines]
    if lines and line_total is not None and None not in line_amounts:
        total = sum(line_amounts, Decimal(0))
        rule("BR-CO-10", abs(total - line_total) <= tol, "sum of %d line(s) = %s, LineTotalAmount = %s" % (len(lines), total, line_total))
    if None not in (line_total, basis):
        exp = line_total - allow + charge
        rule("BR-CO-13", abs(exp - basis) <= tol, "LineTotal - Allowances + Charges = %s, TaxBasisTotal = %s" % (exp, basis))
    breakdown = root.findall(hs + "/ram:ApplicableTradeTax", NS)
    if breakdown and tax_total is not None:
        tsum = sum((dec(t.find("ram:CalculatedAmount", NS)) or Decimal(0) for t in breakdown), Decimal(0))
        rule("BR-CO-14", abs(tsum - tax_total) <= tol, "sum of VAT breakdown = %s, TaxTotalAmount = %s" % (tsum, tax_total))
    for t in breakdown:
        b, r, c = dec(t.find("ram:BasisAmount", NS)), dec(t.find("ram:RateApplicablePercent", NS)), dec(t.find("ram:CalculatedAmount", NS))
        cat = (t.findtext("ram:CategoryCode", default="?", namespaces=NS) or "?").strip()
        if None not in (b, r, c):
            exp = (b * r / 100).quantize(CENT, rounding=ROUND_HALF_UP)
            rule("BR-CO-17", abs(exp - c) <= vat_tol, "VAT %s %s%%: %s x rate = %s, CalculatedAmount = %s" % (cat, r, b, exp, c))
    if None not in (basis, tax_total, grand):
        exp = basis + tax_total
        rule("BR-CO-15", abs(exp - grand) <= tol, "TaxBasisTotal + TaxTotal = %s, GrandTotal = %s" % (exp, grand))
    if None not in (grand, due):
        exp = grand - prepaid
        rule("BR-CO-16", abs(exp - due) <= tol, "GrandTotal - Prepaid = %s, DuePayable = %s" % (exp, due))

    def present(rid, path, label):
        el = find(root, path)
        rule(rid, el is not None and (el.text or "").strip() != "", "%s %s" % (label, "present" if el is not None and (el.text or "").strip() else "MISSING"))

    present("BT-1", "rsm:ExchangedDocument/ram:ID", "invoice number")
    present("BT-2", "rsm:ExchangedDocument/ram:IssueDateTime/udt:DateTimeString", "issue date")
    ha = "rsm:SupplyChainTradeTransaction/ram:ApplicableHeaderTradeAgreement"
    present("BT-27", ha + "/ram:SellerTradeParty/ram:Name", "seller name")
    present("BT-44", ha + "/ram:BuyerTradeParty/ram:Name", "buyer name")
    present("BT-5", hs + "/ram:InvoiceCurrencyCode", "currency")
    if tax_total and tax_total != 0:
        vat = [e for e in root.findall(ha + "/ram:SellerTradeParty/ram:SpecifiedTaxRegistration/ram:ID", NS) if e.get("schemeID") == "VA"]
        rule("BT-31", bool(vat), "seller VAT identifier %s" % ("present" if vat else "MISSING while VAT is charged"))
    return results


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--tolerance", default="0", help="allowed difference on document totals (EN 16931: exact)")
    ap.add_argument("--vat-tolerance", default="0.01", help="allowed difference on basis x rate per VAT category")
    a = ap.parse_args(argv)
    data = open(a.file, "rb").read()
    if data[:5] == b"%PDF-":
        xml = xml_from_pdf(data)
        if xml is None:
            print("No CII XML found in the PDF (embedded file may use an unsupported encoding). Extract it and pass the XML.")
            return 2
        data = xml
    try:
        root = ET.fromstring(data)
    except ET.ParseError as e:
        print("XML parse error: %s" % e)
        return 2
    res = check(root, Decimal(a.tolerance), Decimal(a.vat_tolerance))
    fails = 0
    for rid, ok, detail in res:
        fails += not ok
        print("%-9s %-4s %s" % (rid, "OK" if ok else "FAIL", detail))
    print("\n%d check(s), %d failure(s)" % (len(res), fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Fake but checksum-valid French business test data (stdlib only).

  companies --count N --seed S --format csv|json   invented companies with SIREN, SIRET, VAT, IBAN
  invoices  --count N --seed S --format csv|json   invoices with French VAT rates, half-up rounding
  validate  ID [ID ...]                             check SIREN / SIRET / FR VAT / IBAN checksums
"""
import argparse
import csv
import json
import random
import sys
from datetime import date, timedelta
from decimal import Decimal, ROUND_HALF_UP

CITIES = [("75002", "Paris"), ("69002", "Lyon"), ("33000", "Bordeaux"), ("13001", "Marseille"),
          ("31000", "Toulouse"), ("44000", "Nantes"), ("59000", "Lille"), ("67000", "Strasbourg"),
          ("35000", "Rennes"), ("06000", "Nice"), ("34000", "Montpellier"), ("21000", "Dijon")]
SYLLABLES = ["al", "ver", "nor", "ta", "lis", "mon", "cor", "ba", "ris", "dan", "tel", "gro", "fi", "lu", "sa"]
SUFFIXES = ["Conseil", "Industries", "Services", "Distribution", "Logistique", "Solutions", "& Fils"]
FORMS = ["SAS", "SARL", "SA", "SASU", "EURL"]
VAT_RATES = [Decimal("0.20"), Decimal("0.10"), Decimal("0.055"), Decimal("0.021")]
CENT = Decimal("0.01")


# ---------- checksums ----------
def luhn_ok(digits):
    total = 0
    for i, ch in enumerate(reversed(digits)):
        n = int(ch)
        if i % 2 == 1:
            n *= 2
            if n > 9:
                n -= 9
        total += n
    return total % 10 == 0


def luhn_complete(prefix):
    """Append the digit that makes prefix + digit Luhn-valid."""
    for d in "0123456789":
        if luhn_ok(prefix + d):
            return prefix + d
    raise ValueError(prefix)


def vat_from_siren(siren):
    key = (12 + 3 * (int(siren) % 97)) % 97
    return "FR%02d%s" % (key, siren)


def rib_key(bank, branch, account):
    return 97 - ((89 * int(bank) + 15 * int(branch) + 3 * int(account)) % 97)


def iban_numeric(s):
    return "".join(str(int(c, 36)) for c in s)


def iban_ok(iban):
    iban = iban.replace(" ", "").upper()
    if len(iban) < 15 or not iban[:2].isalpha():
        return False
    return int(iban_numeric(iban[4:] + iban[:4])) % 97 == 1


def make_iban_fr(bank, branch, account):
    bban = "%s%s%s%02d" % (bank, branch, account, rib_key(bank, branch, account))
    check = 98 - int(iban_numeric(bban + "FR00")) % 97
    return "FR%02d%s" % (check, bban)


# ---------- generators ----------
def make_siren(rnd):
    return luhn_complete("%d%07d" % (rnd.randint(1, 9), rnd.randint(0, 9999999)))


def make_siret(rnd, siren):
    return luhn_complete(siren + "%04d" % rnd.randint(1, 999))


def company(rnd):
    name = "".join(rnd.choice(SYLLABLES) for _ in range(rnd.randint(2, 3))).capitalize()
    siren = make_siren(rnd)
    postcode, city = rnd.choice(CITIES)
    bank, branch = "%05d" % rnd.randint(10000, 30099), "%05d" % rnd.randint(0, 99999)
    account = "%011d" % rnd.randint(0, 10 ** 11 - 1)
    return {"name": "%s %s %s" % (name, rnd.choice(SUFFIXES), rnd.choice(FORMS)), "siren": siren,
            "siret": make_siret(rnd, siren), "vat_number": vat_from_siren(siren),
            "iban": make_iban_fr(bank, branch, account), "postcode": postcode, "city": city}


def invoice(rnd, n):
    issued = date(2026, 1, 1) + timedelta(days=rnd.randint(0, 300))
    net = (Decimal(rnd.randint(100, 2_000_000)) / 100).quantize(CENT)
    rate = rnd.choice(VAT_RATES)
    vat = (net * rate).quantize(CENT, rounding=ROUND_HALF_UP)
    return {"number": "FAC-2026-%05d" % n, "issue_date": issued.isoformat(),
            "due_date": (issued + timedelta(days=rnd.choice([30, 45, 60]))).isoformat(),
            "net": str(net), "vat_rate": str(rate * 100).rstrip("0").rstrip("."), "vat": str(vat),
            "gross": str(net + vat), "currency": "EUR"}


# ---------- validation ----------
def validate(value):
    v = value.replace(" ", "").upper()
    if v.isdigit() and len(v) == 9:
        return "SIREN", luhn_ok(v)
    if v.isdigit() and len(v) == 14:
        return "SIRET", luhn_ok(v)
    if v.startswith("FR") and len(v) == 13 and v[4:].isdigit():
        return "VAT FR", v[2:4].isdigit() and vat_from_siren(v[4:]) == v and luhn_ok(v[4:])
    if len(v) >= 15 and v[:2].isalpha() and v[2:4].isdigit():
        return "IBAN", iban_ok(v)
    return "UNKNOWN", False


def emit(rows, fmt):
    if fmt == "json":
        json.dump(rows, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return
    w = csv.DictWriter(sys.stdout, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    for name in ("companies", "invoices"):
        sp = sub.add_parser(name)
        sp.add_argument("--count", type=int, default=10)
        sp.add_argument("--seed", type=int, default=42)
        sp.add_argument("--format", choices=["csv", "json"], default="csv")
    sv = sub.add_parser("validate")
    sv.add_argument("ids", nargs="+")
    a = p.parse_args(argv)
    if a.cmd == "validate":
        bad = 0
        for i in a.ids:
            kind, ok = validate(i)
            bad += not ok
            print("%-30s %-7s %s" % (i, kind, "OK" if ok else "INVALID"))
        return 1 if bad else 0
    rnd = random.Random(a.seed)
    rows = [company(rnd) for _ in range(a.count)] if a.cmd == "companies" else \
        [invoice(rnd, n + 1) for n in range(a.count)]
    emit(rows, a.format)
    return 0


if __name__ == "__main__":
    sys.exit(main())

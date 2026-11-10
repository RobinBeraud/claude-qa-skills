#!/usr/bin/env python3
"""Scan for secrets before they reach the repository: staged changes, a branch diff, or a folder.
Stdlib only. Prints masked values; exit code 1 when something is found (pre-commit friendly).
A line containing "secret-scan: ignore" (or "pragma: allowlist secret") is skipped: use it for test fixtures.

  python secret_scan.py --staged
  python secret_scan.py --diff origin/main
  python secret_scan.py --path . --format md
"""
import argparse
import json
import os
import re
import subprocess
import sys

if hasattr(sys.stdout, "reconfigure"):  # Windows consoles default to a legacy code page
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SKIP_DIRS = {".git", "node_modules", "bin", "obj", ".vs", ".venv", "venv", "dist", "packages", "__pycache__"}
SKIP_EXT = (".png", ".jpg", ".jpeg", ".gif", ".ico", ".pdf", ".zip", ".dll", ".exe", ".pdb", ".nupkg", ".woff", ".woff2")
PLACEHOLDER = re.compile(r"^(\$\{?|\$\(|<|\{\{|%|#\{)|^(x+|\*+|changeme|change_me|password|secret|example|dummy|test|null|none|todo|redacted|your[-_].*|<.*>)$", re.I)

RULES = [
    ("private_key", r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP |ENCRYPTED )?PRIVATE KEY(?: BLOCK)?-----"),
    ("aws_access_key", r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"),
    ("azure_storage_key", r"AccountKey=(?P<val>[A-Za-z0-9+/]{80,}={0,2})"),
    ("azure_sas_signature", r"[?&]sig=(?P<val>[A-Za-z0-9%+/]{30,}={0,2})"),
    ("github_token", r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{36,}\b|\bgithub_pat_[A-Za-z0-9_]{22,}\b"),
    ("gitlab_token", r"\bglpat-[A-Za-z0-9_-]{20,}"),
    ("slack_token", r"\bxox[abprs]-[A-Za-z0-9-]{10,}"),
    ("slack_webhook", r"https://hooks\.slack\.com/services/[A-Za-z0-9/]{20,}"),
    ("google_api_key", r"\bAIza[0-9A-Za-z_-]{35}\b"),
    ("npm_token", r"\bnpm_[A-Za-z0-9]{36}\b"),
    ("anthropic_key", r"\bsk-ant-[A-Za-z0-9_-]{20,}"),
    ("openai_key", r"\bsk-(?:proj-|svcacct-|admin-)?[A-Za-z0-9_-]{20,}"),
    ("jwt", r"\beyJ[A-Za-z0-9_-]{8,}\.eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}"),
    ("connection_string_password", r"(?i)\b(?:password|pwd)\s*=\s*(?P<val>[^;\"'\s<>]{4,})\s*(?:;|$|\"|')"),
    ("assignment", r"(?i)[\"']?\b(?:[a-z0-9_.-]*?(?:password|passwd|secret|api[_-]?key|access[_-]?key|client[_-]?secret|auth[_-]?token|private[_-]?key))\b[\"']?\s*[:=]\s*[\"'](?P<val>[^\"'\s]{8,})[\"']"),
]
COMPILED = [(k, re.compile(p)) for k, p in RULES]
ALLOW = re.compile(r"secret-scan:\s*ignore|pragma:\s*allowlist secret", re.I)


def mask(v):
    v = v.strip()
    return "*" * len(v) if len(v) <= 8 else v[:4] + "*" * min(len(v) - 6, 12) + v[-2:]


def scan_line(line):
    found, taken = [], []
    for kind, rx in COMPILED:
        for m in rx.finditer(line):
            span = m.span("val") if "val" in rx.groupindex else m.span()
            if any(not (span[1] <= a or span[0] >= b) for a, b in taken):
                continue
            value = line[span[0]:span[1]]
            if "val" in rx.groupindex and PLACEHOLDER.search(value):
                continue
            taken.append(span)
            found.append({"kind": kind, "excerpt": value if kind == "private_key" else mask(value)})
    return found


def scan_text(text, path):
    out = []
    for n, line in enumerate(text.splitlines(), 1):
        if ALLOW.search(line):
            continue
        for f in scan_line(line):
            out.append(dict(f, file=path, line=n))
    return out


def scan_diff(diff):
    """Scan only added lines of a unified diff (git diff -U0), keeping file and new line numbers."""
    out, path, lineno = [], None, 0
    for raw in diff.splitlines():
        if raw.startswith("+++ "):
            p = raw[4:]
            path = None if p == "/dev/null" else (p[2:] if p.startswith("b/") else p)
        elif raw.startswith("@@"):
            m = re.search(r"\+(\d+)", raw)
            lineno = int(m.group(1)) if m else 0
        elif raw.startswith("+") and path:
            for f in ([] if ALLOW.search(raw) else scan_line(raw[1:])):
                out.append(dict(f, file=path, line=lineno))
            lineno += 1
        elif raw.startswith(" "):
            lineno += 1
    return out


def scan_path(root):
    out = []
    files = [root] if os.path.isfile(root) else []
    for dirpath, dirs, fs in ([] if files else os.walk(root)):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        files += [os.path.join(dirpath, f) for f in fs]
    for fp in files:
        if fp.lower().endswith(SKIP_EXT):
            continue
        try:
            with open(fp, "rb") as f:
                raw = f.read(5_000_000)
        except OSError:
            continue
        if b"\x00" in raw[:2048]:
            continue
        out += scan_text(raw.decode("utf-8", errors="replace"), (os.path.relpath(fp, root) if not os.path.isfile(root) else fp).replace(os.sep, "/"))
    return out


def git(*args):
    try:
        return subprocess.run(["git"] + list(args), capture_output=True, text=True, check=True, encoding="utf-8", errors="replace").stdout
    except subprocess.CalledProcessError as e:
        raise SystemExit("error: git failed: %s" % (e.stderr or "").strip())


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--staged", action="store_true", help="scan staged changes (pre-commit)")
    g.add_argument("--diff", metavar="REF", help="scan lines added since REF (merge base with HEAD)")
    g.add_argument("--path", help="scan files under a folder or a single file")
    ap.add_argument("--format", choices=["text", "md", "json"], default="text")
    a = ap.parse_args(argv)
    if a.staged:
        found = scan_diff(git("diff", "--cached", "-U0", "--no-color"))
    elif a.diff:
        found = scan_diff(git("diff", "-U0", "--no-color", a.diff + "...HEAD"))
    else:
        found = scan_path(a.path)
    if a.format == "json":
        print(json.dumps(found, indent=2))
    elif a.format == "md":
        print("| File | Line | Kind | Masked value |\n|---|---|---|---|")
        for f in found:
            print("| %s | %d | %s | `%s` |" % (f["file"], f["line"], f["kind"], f["excerpt"]))
        print("\n%d potential secret(s)." % len(found))
    else:
        for f in found:
            print("%s:%d  %-28s %s" % (f["file"], f["line"], f["kind"], f["excerpt"]))
        print("%d potential secret(s)%s" % (len(found), ". Revoke and rotate any real one before anything else." if found else "."))
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())

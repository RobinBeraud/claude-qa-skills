#!/usr/bin/env python3
"""Inventory a .NET repository: projects, target frameworks and support status, package version drift,
packages.config leftovers, and a leaves-first migration order. Stdlib only, reads files, never builds.

  python csproj_scan.py path/to/repo --format md
  python csproj_scan.py . --format json > inventory.json
"""
import argparse
import json
import os
import re
import sys
import xml.etree.ElementTree as ET

if hasattr(sys.stdout, "reconfigure"):  # Windows consoles default to a legacy code page
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJECT_EXT = (".csproj", ".vbproj", ".fsproj")
SKIP_DIRS = {".git", "bin", "obj", "node_modules", "packages", ".vs", ".idea"}

# Support status as known in November 2026 (check https://dotnet.microsoft.com/platform/support/policy)
MODERN = {"net10.0": "supported (LTS, until 2028-11)", "net9.0": "end of support 2026-11-10",
          "net8.0": "end of support 2026-11-10", "net7.0": "out of support", "net6.0": "out of support",
          "net5.0": "out of support"}
FRAMEWORK_SUPPORTED = {"net462", "net47", "net471", "net472", "net48", "net481"}


def tag(el):
    return el.tag.split("}", 1)[-1]


def children(root, name):
    return [e for e in root.iter() if tag(e) == name]


def normalise_tfm(t):
    t = t.strip()
    m = re.fullmatch(r"v(\d)\.(\d)(?:\.(\d))?", t)  # old-style TargetFrameworkVersion v4.7.2
    if m:
        return "net" + "".join(g for g in m.groups() if g)
    return t.lower()


def classify(tfm):
    base = tfm.split("-", 1)[0]
    if base.startswith("netstandard"):
        return ".NET Standard", "supported (library target)"
    if base.startswith("netcoreapp"):
        return ".NET Core", "out of support"
    m = re.fullmatch(r"net(\d+)\.(\d+)", base)
    if m:
        return ".NET", MODERN.get(base, "supported" if int(m.group(1)) >= 10 else "out of support")
    if re.fullmatch(r"net\d{2,3}", base):
        return ".NET Framework", "supported with Windows" if base in FRAMEWORK_SUPPORTED else "out of support"
    return "other", "unknown"


def read_xml(path):
    try:
        return ET.parse(path).getroot()
    except (ET.ParseError, OSError):
        return None


def parse_project(path):
    root = read_xml(path)
    if root is None:
        return None
    sdk = bool(root.get("Sdk")) or any(tag(e) == "Sdk" for e in root)
    tfms = []
    for name in ("TargetFrameworks", "TargetFramework", "TargetFrameworkVersion"):
        for e in children(root, name):
            if e.text and "$(" not in e.text:
                tfms += [normalise_tfm(x) for x in e.text.split(";") if x.strip()]
    out_type = next((e.text for e in children(root, "OutputType") if e.text), "Library")
    refs = []
    for e in children(root, "ProjectReference"):
        inc = e.get("Include")
        if inc:
            refs.append(os.path.normpath(os.path.join(os.path.dirname(path), inc.replace("\\", os.sep))))
    pkgs = {}
    for e in children(root, "PackageReference"):
        name = e.get("Include") or e.get("Update")
        if not name:
            continue
        ver = e.get("Version") or e.get("VersionOverride")
        if ver is None:
            v = [c.text for c in e if tag(c) in ("Version", "VersionOverride") and c.text]
            ver = v[0] if v else None
        pkgs[name] = ver
    pc = os.path.join(os.path.dirname(path), "packages.config")
    legacy_pc = False
    if os.path.isfile(pc):
        r = read_xml(pc)
        if r is not None:
            legacy_pc = True
            for e in children(r, "package"):
                if e.get("id"):
                    pkgs.setdefault(e.get("id"), e.get("version"))
    return {"path": path, "name": os.path.splitext(os.path.basename(path))[0], "sdk_style": sdk, "tfms": sorted(set(tfms)),
            "output_type": out_type, "references": refs, "packages": pkgs, "packages_config": legacy_pc}


def central_versions(repo):
    versions, enabled = {}, False
    for dirpath, dirs, files in os.walk(repo):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if f in ("Directory.Packages.props", "Directory.Build.props"):
                r = read_xml(os.path.join(dirpath, f))
                if r is None:
                    continue
                for e in children(r, "ManagePackageVersionsCentrally"):
                    enabled = enabled or (e.text or "").strip().lower() == "true"
                for e in children(r, "PackageVersion"):
                    if e.get("Include"):
                        versions[e.get("Include")] = e.get("Version")
    return enabled, versions


def migration_order(projects):
    by_path = {os.path.normcase(p["path"]): p for p in projects}
    deps = {k: [os.path.normcase(r) for r in p["references"] if os.path.normcase(r) in by_path] for k, p in by_path.items()}
    order, state = [], {}

    def visit(k, stack):
        if state.get(k) == 2:
            return
        if state.get(k) == 1:
            return  # cycle: keep going, reported by the caller
        state[k] = 1
        for d in deps[k]:
            visit(d, stack + [k])
        state[k] = 2
        order.append(by_path[k]["name"])

    for k in sorted(by_path):
        visit(k, [])
    return order


def scan(repo):
    projects = []
    for dirpath, dirs, files in os.walk(repo):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if f.endswith(PROJECT_EXT):
                p = parse_project(os.path.join(dirpath, f))
                if p:
                    projects.append(p)
    cpm, central = central_versions(repo)
    usage = {}
    for p in projects:
        for name, ver in p["packages"].items():
            ver = ver or central.get(name) or "(central/unspecified)"
            usage.setdefault(name, {}).setdefault(ver, []).append(p["name"])
    drift = {n: v for n, v in usage.items() if len(v) > 1}
    tf_summary = {}
    for p in projects:
        for t in p["tfms"] or ["(inherited or unknown)"]:
            fam, status = classify(t) if t[0] != "(" else ("unknown", "set in Directory.Build.props?")
            tf_summary.setdefault(t, {"family": fam, "status": status, "projects": []})["projects"].append(p["name"])
    return {"projects": projects, "central_package_management": cpm, "drift": drift, "frameworks": tf_summary,
            "migration_order": migration_order(projects), "packages_count": len(usage)}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("repo", nargs="?", default=".")
    ap.add_argument("--format", choices=["md", "json"], default="md")
    a = ap.parse_args(argv)
    r = scan(a.repo)
    if a.format == "json":
        print(json.dumps(r, indent=2, default=str))
        return 0
    ps = r["projects"]
    print("## .NET inventory of %s\n" % os.path.abspath(a.repo))
    print("%d projects, %d SDK-style, %d still on packages.config, %d distinct packages, central package management: %s\n" % (
        len(ps), sum(p["sdk_style"] for p in ps), sum(p["packages_config"] for p in ps), r["packages_count"],
        "yes" if r["central_package_management"] else "no"))
    print("### Target frameworks\n\n| Target | Family | Support | Projects |\n|---|---|---|---|")
    for t, v in sorted(r["frameworks"].items()):
        names = v["projects"]
        print("| %s | %s | %s | %d: %s%s |" % (t, v["family"], v["status"], len(names), ", ".join(names[:6]), " ..." if len(names) > 6 else ""))
    if r["drift"]:
        print("\n### Package version drift (same package, several versions)\n\n| Package | Versions (projects) |\n|---|---|")
        for n, vers in sorted(r["drift"].items()):
            print("| %s | %s |" % (n, "; ".join("%s (%d)" % (v, len(p)) for v, p in sorted(vers.items()))))
    legacy = [p["name"] for p in ps if not p["sdk_style"]]
    if legacy:
        print("\n### Old-style projects to convert to SDK style\n\n" + ", ".join(legacy))
    print("\n### Migration order (leaves first)\n\n" + " -> ".join(r["migration_order"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())

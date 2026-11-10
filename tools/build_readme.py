#!/usr/bin/env python3
"""Rebuild the skills catalogue in README.md (between the CATALOG markers) and the skill-count badge.

Run after adding or editing a skill:  python tools/build_readme.py
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TITLES = {
    "qa-test-strategy": "🗺️ Test strategy: decide what quality means and how to get it",
    "qa-unit-testing": "🧪 Unit testing and TDD",
    "qa-mutation-testing": "🧬 Mutation testing: do the tests really check anything?",
    "dora-metrics": "📊 DORA metrics: software delivery performance",
    "evidence-based-management": "🎯 Evidence-Based Management: value, not output",
    "qa-shift-left": "🧭 Shift-left: test before the code exists",
    "qa-automation": "🤖 Automation that stays green for the right reasons",
    "qa-explore-and-report": "🔎 Explore and report",
    "qa-ci-insights": "📈 CI insights",
    "qa-release": "🚀 Release with evidence",
    "qa-ai-era": "🧠 Quality in the age of coding agents",
    "qa-business-apps": "🏦 Business software: ERP, accounting, e-invoicing, SaaS",
    "dev-workflow": "🧭 Developer workflow: explore, plan, debug, prove, ship small PRs",
    "dev-dotnet": "🟣 .NET and C#: inventory, upgrade, modern C#, tests, EF Core, NuGet",
    "dev-web": "🌐 Web front-end: Angular, TypeScript, accessibility (RGAA), i18n",
    "dev-data": "🗄️ Data: SQL Server, schema changes, multi-tenant, GDPR",
    "dev-legacy": "🏚️ Legacy code: hotspots, characterisation tests, strangler fig, TFVC, backports",
    "dev-delivery": "🚚 Delivery: Azure Pipelines, work items, changelog, stale PRs, flags, incidents",
    "dev-security": "🔐 Secure development: code review, threat model, defaults, supply chain, secrets",
}


def desc_of(path):
    text = open(path, encoding="utf-8").read()
    m = re.search(r"^description:\s*(.*)$", text, re.M)
    v = m.group(1).strip()
    return json.loads(v) if v.startswith('"') else v


def short(d):
    first = re.split(r"(?<=[.])\s+Use ", d, maxsplit=1)[0]
    return first if len(first) <= 190 else first[:187].rsplit(" ", 1)[0] + "..."


def main():
    mp = json.load(open(os.path.join(ROOT, ".claude-plugin", "marketplace.json"), encoding="utf-8"))
    out, total = [], 0
    for entry in mp["plugins"]:
        base = os.path.join(ROOT, entry["source"])
        skills = sorted(os.listdir(os.path.join(base, "skills")))
        total += len(skills)
        out.append("### %s\n" % TITLES.get(entry["name"], entry["name"]))
        out.append("Plugin **`%s`** (%d skills): `/plugin install %s@%s`\n" % (entry["name"], len(skills), entry["name"], mp["name"]))
        out.append("| Skill | What it does | Script |\n|---|---|---|")
        for s in skills:
            sd = os.path.join(base, "skills", s)
            has_script = os.path.isdir(os.path.join(sd, "scripts"))
            rel = os.path.relpath(os.path.join(sd, "SKILL.md"), ROOT).replace(os.sep, "/")
            out.append("| [%s](%s) | %s | %s |" % (s, rel, short(desc_of(os.path.join(sd, "SKILL.md"))), "🐍" if has_script else ""))
        out.append("")
    readme = os.path.join(ROOT, "README.md")
    text = open(readme, encoding="utf-8").read()
    text = re.sub(r"<!-- CATALOG:START -->.*<!-- CATALOG:END -->",
                  "<!-- CATALOG:START -->\n" + "\n".join(out) + "\n<!-- CATALOG:END -->", text, flags=re.S)
    text = re.sub(r"skills-\d+-", "skills-%d-" % total, text)
    text = re.sub(r"plugins-\d+-", "plugins-%d-" % len(mp["plugins"]), text)
    open(readme, "w", encoding="utf-8", newline="\n").write(text)
    print("README catalogue: %d plugins, %d skills" % (len(mp["plugins"]), total))


if __name__ == "__main__":
    main()

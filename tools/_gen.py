"""Tiny helper used by the per-plugin generator files in tools/gen_*.py.

Each generator declares PLUGIN, PLUGIN_DESC and SKILLS = {name: (description, body)} and calls
write_plugin(). Kept in the repo so a maintainer can regenerate or bulk-edit skills, but the
SKILL.md files themselves are the source of truth once committed.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERSION = "1.2.0"


def write_plugin(plugin, plugin_desc, skills, keywords=()):
    base = os.path.join(ROOT, "plugins", plugin)
    os.makedirs(os.path.join(base, ".claude-plugin"), exist_ok=True)
    manifest = {
        "name": plugin,
        "description": plugin_desc,
        "version": VERSION,
        "author": {"name": "Robin Béraud-Sudreau", "url": "https://coach-agile.com"},
        "homepage": "https://github.com/RobinBeraud/claude-qa-skills",
        "license": "MIT",
        "keywords": ["qa", "testing", "quality"] + list(keywords),
    }
    with open(os.path.join(base, ".claude-plugin", "plugin.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
        f.write("\n")
    for name, (desc, body) in skills.items():
        d = os.path.join(base, "skills", name)
        os.makedirs(d, exist_ok=True)
        desc = " ".join(desc.split())
        # JSON string syntax is a valid YAML double-quoted scalar: safe with ": " inside the text
        text = "---\nname: %s\ndescription: %s\n---\n\n%s" % (name, json.dumps(desc, ensure_ascii=False), body.strip() + "\n")
        with open(os.path.join(d, "SKILL.md"), "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
    print("%s: %d skills" % (plugin, len(skills)))

#!/usr/bin/env python3
"""Validate the repository: marketplace entries, plugin manifests and every SKILL.md. Stdlib only.

Checks: marketplace.json parses, each entry's source exists and its plugin.json name equals the entry
name; each SKILL.md starts with front matter holding name + description; name == folder, lowercase
letters/digits/hyphens, <= 64 chars; description <= 1024 chars (Agent Skills spec), mentions when to
use it; body < 500 lines; scripts referenced as ${CLAUDE_SKILL_DIR}/... exist.
Exit code 1 on any error.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def front_matter(text):
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---\n", 4)
    if end < 0:
        return None, text
    fm = {}
    for line in text[4:end].splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            v = v.strip()
            if v.startswith('"'):
                v = json.loads(v)
            elif ": " in v or v.startswith(("'", "[", "{", "&", "*", "!", "|", ">")):
                fm.setdefault("_errors", []).append("%s: unquoted value containing YAML syntax, quote it" % k.strip())
            fm[k.strip()] = v
    return fm, text[end + 5:]


def main():
    errors, skills = [], 0
    mp_path = os.path.join(ROOT, ".claude-plugin", "marketplace.json")
    mp = json.load(open(mp_path, encoding="utf-8"))
    for key in ("name", "owner", "plugins"):
        if key not in mp:
            errors.append("marketplace.json: missing '%s'" % key)
    listed = set()
    for entry in mp.get("plugins", []):
        src = os.path.normpath(os.path.join(ROOT, entry["source"]))
        listed.add(os.path.basename(src))
        man = os.path.join(src, ".claude-plugin", "plugin.json")
        if not os.path.isfile(man):
            errors.append("%s: plugin.json not found at %s" % (entry["name"], man))
            continue
        pj = json.load(open(man, encoding="utf-8"))
        if pj.get("name") != entry["name"]:
            errors.append("%s: plugin.json name '%s' differs from marketplace entry" % (entry["name"], pj.get("name")))
        sdir = os.path.join(src, "skills")
        for skill in sorted(os.listdir(sdir)):
            p = os.path.join(sdir, skill, "SKILL.md")
            if not os.path.isfile(p):
                errors.append("%s/%s: SKILL.md missing" % (entry["name"], skill))
                continue
            skills += 1
            text = open(p, encoding="utf-8").read()
            fm, body = front_matter(text)
            where = "%s/%s" % (entry["name"], skill)
            if fm is None:
                errors.append("%s: no front matter on line 1" % where)
                continue
            for msg in fm.get("_errors", []):
                errors.append("%s: %s" % (where, msg))
            name, desc = fm.get("name", ""), fm.get("description", "")
            if name != skill:
                errors.append("%s: name '%s' != folder" % (where, name))
            if not NAME_RE.match(name) or len(name) > 64:
                errors.append("%s: invalid name" % where)
            if not desc or len(desc) > 1024:
                errors.append("%s: description missing or > 1024 chars (%d)" % (where, len(desc)))
            if "use " not in desc.lower():
                errors.append("%s: description should say when to use the skill" % where)
            if body.count("\n") >= 500:
                errors.append("%s: body has 500+ lines" % where)
            for ref in re.findall(r"\$\{CLAUDE_SKILL_DIR\}/([\w./-]+)", body):
                if not os.path.isfile(os.path.join(sdir, skill, ref)):
                    errors.append("%s: referenced file %s not found" % (where, ref))
    on_disk = set(os.listdir(os.path.join(ROOT, "plugins")))
    for orphan in sorted(on_disk - listed):
        errors.append("plugins/%s is not listed in marketplace.json" % orphan)
    for e in errors:
        print("ERROR " + e)
    print("%d plugin(s), %d skill(s), %d error(s)" % (len(mp.get("plugins", [])), skills, len(errors)))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

# Contributing

## Add a skill

1. Pick the plugin that fits (`plugins/<plugin>/skills/`) and create `<skill-name>/SKILL.md` (lowercase, hyphens).
2. Front matter on line 1, description **quoted**:
   ```yaml
   ---
   name: skill-name
   description: "What it does, in one sentence. Use when <trigger situations>."
   ---
   ```
   The description is what Claude reads to decide when to load the skill: put the use case first, include trigger words testers actually say, stay under 1,024 characters.
3. Body: purpose in one line, then **Steps** (imperative, concrete), **Output** (exact format), and pitfalls. Under 500 lines; move long references to a sibling `reference.md`.
4. Scripts go in `scripts/`, Python **standard library only**, referenced as `${CLAUDE_SKILL_DIR}/scripts/<file>`, with a test in `tests/test_scripts.py`.
5. Answer in the user's language; never invent business rules or results; never use real personal data.

## Check before pushing

```bash
python tools/validate_skills.py
python -m unittest discover -s tests -v
claude plugin validate .
python tools/build_readme.py   # README catalogue
python tools/build_site.py     # docs/index.html (GitHub Pages)
```

Bump `version` in the plugin's `plugin.json` when you change its skills, so installed copies update.

---
name: secrets-hygiene
description: "Keep secrets out of code, history and logs: scan a diff, staged files or a whole repository with a bundled stdlib scanner (cloud keys, tokens, connection strings with passwords, private keys), move secrets to Key Vault, user secrets or pipeline variable groups, and handle a leaked secret properly: revoke and rotate first, then clean history. Use before committing or pushing, when reviewing configuration files, when a secret was committed, or when setting up a new project's configuration."
---

# Secrets hygiene

## Scan
```bash
python "${CLAUDE_SKILL_DIR}/scripts/secret_scan.py" --staged                 # before a commit
python "${CLAUDE_SKILL_DIR}/scripts/secret_scan.py" --diff origin/main       # a branch
python "${CLAUDE_SKILL_DIR}/scripts/secret_scan.py" --path . --format md     # whole working tree
```
Detects cloud and SaaS keys (AWS, Azure storage, GitHub, GitLab, Slack, OpenAI, Anthropic), private keys, JWTs, connection strings with `Password=`, and generic `secret/password/apikey = value` assignments, skipping obvious placeholders. Prints masked values only; exit 1 if anything is found (usable as a pre-commit hook). Test fixtures that must contain fake secrets: add `secret-scan: ignore` on the line.

## Where secrets belong
| Context | Store |
|---|---|
| Local development (.NET) | `dotnet user-secrets` (outside the repo) |
| Azure-hosted apps | Key Vault + managed identity (no secret at all) |
| Pipelines | variable groups linked to Key Vault, secret variables |
| Front-end | nothing secret, ever: it ships to the browser |

## A secret was committed
1. **Revoke and rotate it now.** Assume it is compromised: history, forks, CI logs and caches keep it.
2. Check access logs of that credential for misuse.
3. Then clean history if policy requires (`git filter-repo`, coordinated force-push), and add the pattern to the scanner/pre-commit.
4. Write a short incident note (see `dev-delivery:incident-review`).

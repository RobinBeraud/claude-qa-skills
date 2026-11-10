---
name: typescript-strict
description: "Turn on TypeScript strictness in an existing codebase without a big-bang: measure errors per flag, enable flags one at a time (noImplicitAny, strictNullChecks, ...), fix by folder with a ratchet so the error count only goes down, and ban new any. Use when a TypeScript or Angular project has strict mode off, when runtime undefined errors are frequent, or when reviewing type safety."
---

# TypeScript strictness

## Measure
```bash
npx tsc --noEmit -p tsconfig.json --strict 2>&1 | grep -c "error TS"
```
Count errors per flag by enabling them one at a time in a scratch `tsconfig.strict.json` that `extends` the main one.

## Order (easiest value first)
1. `noImplicitAny`, 2. `strictNullChecks` (most bugs found), 3. `strictFunctionTypes`, `strictBindCallApply`, 4. `noImplicitOverride`, `noUncheckedIndexedAccess` (optional, strong), 5. full `strict`. Angular: also `strictTemplates`.

## Ratchet
- Enable the flag in a separate config checked in CI for already-clean folders; widen the list folder by folder.
- Or record the current error count in CI and fail when it grows.
- Lint rule `@typescript-eslint/no-explicit-any` as error for new code.

## Fixing
- Model the data: interfaces for API responses (generate from OpenAPI when possible).
- `undefined` handled at the boundary (parse/validate API data, e.g. with zod), not with `!` everywhere.
- `unknown` + narrowing instead of `any` for truly unknown input.

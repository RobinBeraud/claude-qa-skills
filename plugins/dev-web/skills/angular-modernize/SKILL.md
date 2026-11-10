---
name: angular-modernize
description: "Modernise an Angular application step by step: version-by-version upgrades with ng update, standalone components, signals and the new control flow, inject() function, typed reactive forms, OnPush change detection, and removal of deprecated modules, each through official migration schematics with tests between steps. Use when upgrading Angular, migrating NgModules or RxJS-heavy state to signals, or reviewing Angular code for modern patterns."
---

# Angular modernisation

## Upgrade path
1. One major version at a time: check https://angular.dev/update-guide for the exact steps of your versions.
2. `ng update @angular/core@<next> @angular/cli@<next>`; then the libraries (Material, NgRx...), which must support that version.
3. Build, unit tests, e2e smoke tests, commit. Next major.

## Official migrations (each its own PR)
```bash
ng generate @angular/core:standalone          # NgModules -> standalone (run its 3 modes in order)
ng generate @angular/core:control-flow        # *ngIf/*ngFor -> @if/@for (track is required)
ng generate @angular/core:inject              # constructor injection -> inject()
ng generate @angular/core:signal-input-migration
ng generate @angular/core:signal-queries-migration
```

## Patterns
- State in components: signals (`signal`, `computed`, `effect` sparingly); RxJS for event streams and HTTP, bridged with `toSignal`.
- `ChangeDetectionStrategy.OnPush` for new components.
- Typed reactive forms; no `any` in form models.
- `@defer` for heavy, below-the-fold parts.
- Lazy-loaded routes per feature; no shared mega-module.

## Rules
Never mix a framework upgrade with a refactor in the same PR. Keep e2e tests on the critical journeys green at every step.

---
name: dotnet-upgrade
description: "Plan and run an incremental upgrade from .NET Framework or an old .NET version to the current LTS: assessment (APIs, packages, blockers like System.Web, WCF, WebForms), SDK-style conversion, multi-targeting, side-by-side migration with YARP or System.Web adapters, test safety net and release plan. Use when asked to migrate to .NET 10 or another modern version, modernise a .NET Framework application, or leave an unsupported runtime."
---

# .NET upgrade

Big-bang rewrites fail; incremental upgrades ship.

**Target**: the current LTS. As of November 2026 that is **.NET 10** (supported until November 2028); .NET 8 and .NET 9 reach end of support on 10 November 2026, .NET 5/6/7 and .NET Core are already out of support. .NET Framework 4.6.2-4.8.1 stays supported with Windows but gets no new features. Check https://dotnet.microsoft.com/platform/support/policy before planning.

## 1. Assess
- Inventory with `dotnet-solution-inventory` (frameworks, packages, reference graph).
- Run the .NET Upgrade Assistant analysis or the API portability analyzers; list unsupported APIs.
- Packages: does each have a modern version? Abandoned ones need a replacement.
- Blockers: `System.Web` (MVC 5, WebForms), WCF server (-> CoreWCF or gRPC/REST), `AppDomain`, Remoting, `BinaryFormatter`, Windows-only APIs (OK if you stay on Windows: `net10.0-windows`).

## 2. Safety net
Characterisation tests on critical flows before touching anything (see `qa-automation:characterization-tests`). CI must build both old and new targets.

## 3. Convert, leaves first
1. `packages.config` -> `PackageReference`.
2. Old csproj -> SDK-style (`try-convert` or Upgrade Assistant), still targeting `net48`; build, test, commit.
3. Libraries: multi-target `<TargetFrameworks>net48;net10.0</TargetFrameworks>`, fix with `#if NET` only where needed.
4. Applications last. For web apps: **side-by-side** (new ASP.NET Core app in front with YARP proxying unmigrated routes to the old app; System.Web adapters to share session/auth) and move routes one by one.

## 4. Release
Ship each step. Monitor errors and performance against the old version. Remove the old target when nothing depends on it.

## Red flags
Upgrading everything in one branch; "we will write tests after"; replacing libraries and the framework at the same time.

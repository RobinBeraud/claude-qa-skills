---
name: testability-refactoring
description: "Make hard-to-test or legacy code unit-testable with safe, small refactorings (Michael Feathers' seams): extract method, inject dependencies, wrap static and global calls, introduce an interface, pass the clock and random source, separate pure logic from I/O; protected by characterization tests first. Use when code cannot be unit tested because of statics, singletons, new-ed dependencies, time, or database calls in the middle of logic."
---

# Testability refactoring

## Steps
1. **Protect first**: write characterization tests around the current behaviour (`characterization-tests` skill) at the highest convenient level.
2. **Find the seam** that blocks testing:
   | Obstacle | Seam |
   |---|---|
   | `new Service()` inside the method | Constructor/parameter injection |
   | Static/global call (`DateTime.Now`, `Config.get`) | Wrap in an interface or pass a function/clock |
   | Logic mixed with SQL/HTTP | Extract the pure calculation into its own function |
   | Huge method | Extract method, then test the extracted piece |
   | Hidden singleton | Introduce a parameter with the singleton as default |
3. Apply **one** refactoring at a time, run the tests after each.
4. Write unit tests on the newly exposed pure logic.
5. Keep behaviour identical: no "while I'm here" changes.

## Output
Sequence of refactorings with diffs, tests after each step, and the new unit tests.

---
name: test-doubles-chooser
description: "Choose and write the right test double (dummy, stub, spy, mock, fake) for each collaborator of the unit under test, avoid over-mocking, and prefer fakes or real objects where cheap; explains the trade-off in one line per collaborator. Use when a unit test needs to isolate a database, HTTP client, clock, queue or service, or when tests break on every refactor."
---

# Choosing test doubles

| Double | What it does | Use when |
|---|---|---|
| Dummy | Fills a parameter, never used | Required argument irrelevant to the test |
| Stub | Returns canned answers | You need the collaborator's *output* (price, user, config) |
| Spy | Records calls for later assertions | The call itself is the behaviour (e-mail sent, event published) |
| Mock | Pre-programmed expectations, fails on unexpected calls | Protocol matters (order, exact arguments); use sparingly |
| Fake | Working lightweight implementation (in-memory repository, fake clock) | Collaborator is used a lot; you want realistic behaviour without I/O |

## Steps
1. List the unit's collaborators.
2. For each: is it a **value or pure logic**? Use the real thing. Is it **I/O or slow or non-deterministic**? Double it.
3. Pick the weakest double that does the job (stub before mock). Prefer one **fake** over many mocks for repositories and clocks.
4. Never mock what you do not own directly (HTTP library, ORM): wrap it in your own adapter and double the adapter.
5. Write the doubles and the tests; keep assertions on outcomes.

## Output
`collaborator -> double type -> why`, then the code. Flag any test with more than 3 mocks: the unit probably has too many responsibilities.

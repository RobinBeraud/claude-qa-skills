---
name: contract-testing
description: "Set up consumer-driven contract tests (Pact or schema-based) between a front end or service and the APIs it consumes, so breaking changes are caught in CI before deployment. Use when teams integrate across services, when E2E suites are slow or flaky, or when a provider change broke a consumer."
---

# Contract testing

E2E tests prove two services work together once; contracts prove it on every build, fast.

## Steps
1. **Map interactions**: for each consumer, list the requests it really makes and the fields it really reads (not the whole provider schema).
2. **Consumer side**: write a Pact test per interaction (given state, request, minimal expected response with matchers like `like()` / `eachLike()`). Publish the pact to a broker or as a CI artifact.
3. **Provider side**: verify pacts against the real provider with state handlers that create the required data.
4. **CI gate**: `can-i-deploy` (Pact Broker) or a verification job that fails the provider build when a consumer contract breaks.
5. Without Pact: generate JSON Schemas of what the consumer reads and validate provider responses against them in the provider's test suite.

## Output
Consumer tests, provider verification setup, CI steps, and the list of interactions covered.

## Pitfalls
- Over-specified contracts (exact values, full payloads) break on harmless changes; match on types and the fields actually used.
- Contracts do not test business logic; keep API tests for that.

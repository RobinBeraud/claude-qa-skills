---
name: performance-test-k6
description: "Design and script load, stress and soak tests with k6 (or Locust/Gatling if the team uses them): realistic scenarios, think time, thresholds on p95/p99 and error rate, and a readable results summary. Use before a release with performance risk, after an NFR is defined, or when users report slowness."
---

# Performance tests with k6

## Steps
1. **Start from an NFR**: target load, p95/p99 latency, error rate, duration. No target, no test (see `nfr-checklist`).
2. **Model users**: the 3-5 journeys that matter, their mix (e.g. 70 % read list, 20 % open detail, 10 % create), think time.
3. **Choose the test type**: smoke (1-2 VUs), load (expected peak), stress (find the breaking point), soak (hours, memory leaks), spike.
4. **Script** with `scenarios`, `thresholds` and checks:
   ```js
   export const options = {
     scenarios: { browse: { executor: 'ramping-vus', stages: [{duration:'5m',target:50},{duration:'20m',target:50},{duration:'5m',target:0}] } },
     thresholds: { http_req_failed: ['rate<0.01'], http_req_duration: ['p(95)<800'] },
   };
   ```
5. **Data**: unique users and records per VU; never load-test production without written approval.
6. **Run** from a machine close to the system, watch server metrics (CPU, DB, queues) at the same time.
7. **Report**: thresholds pass/fail, latency percentiles per endpoint, errors, the bottleneck observed, and the next experiment.

## Pitfalls
Averages hide pain: use percentiles. A test with no server-side metrics finds *that* it is slow, not *why*.

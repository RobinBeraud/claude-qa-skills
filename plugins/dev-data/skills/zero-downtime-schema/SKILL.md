---
name: zero-downtime-schema
description: "Change a production database schema without downtime or data loss: expand and contract, backward-compatible steps across deployments, batched backfills, online index operations, renames through new columns, dual writes when needed, and a rollback plan per step; independent of the ORM. Use when renaming, splitting or dropping columns and tables, changing types or constraints, or planning a migration on a large live table."
---

# Zero-downtime schema changes

Rule: at every moment, the **running** version of the code and the **next** one must both work with the schema.

## Patterns
| Change | Safe sequence |
|---|---|
| Add column | nullable or with default -> deploy code that writes it -> backfill -> make NOT NULL later if needed |
| Rename column | add new -> write both -> backfill -> read new -> stop writing old -> drop old (later release) |
| Change type | new column with new type, same as rename |
| Drop column | stop reading -> stop writing -> deploy -> drop in a later release |
| Add NOT NULL / FK / unique | clean the data first, then add the constraint (`WITH NOCHECK` + validate later on huge tables, where supported) |
| Split a table | new table, dual write, backfill, switch reads, stop old writes |

## Backfill
Batches (1-10k rows), commit per batch, resumable (by key range), throttled, logged; run off-peak; check replication or log growth.

## Large tables
Online index create/rebuild where the edition allows; avoid long schema locks; rehearse on a production-sized copy and time it.

## Checklist per step
SQL reviewed, rollback written, duration measured, monitoring ready, owner on call.

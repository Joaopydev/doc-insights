# ADR 003 — DynamoDB

## Context

Document metadata, processing state, analysis results, and knowledge indexing require highly available storage with predictable latency and serverless scale.

## Decision

Use DynamoDB for primary persistence of document state, analysis metadata, and knowledge base records.

## Alternatives Considered

- RDS/PostgreSQL: strong relational capabilities but greater operational burden and less ideal for serverless scale.
- OpenSearch: useful for search, but not appropriate as the authoritative metadata store.

## Consequences

- Fast, scalable storage that fits serverless access patterns.
- Requires careful schema design and partition key modeling for query patterns.
- Enables cost-efficient throughput usage under AWS pay-per-use pricing.

# ADR 010 — Event-Driven Architecture

## Context

Document workflows require decoupled orchestration across ingestion, extraction, intelligence, and knowledge indexing services.

## Decision

Use an event-driven architecture with EventBridge and domain events to orchestrate asynchronous processing across bounded contexts.

## Alternatives Considered

- Synchronous orchestration in a single Lambda: simpler but brittle and hard to scale.
- AWS Step Functions: useful for orchestration but adds complexity and cost for this event-first design.

## Consequences

- Enables clear separation of responsibilities and flexible extension points.
- Requires management of event contracts and event schema discipline.
- Supports multiple consumers and eventual consistency patterns.

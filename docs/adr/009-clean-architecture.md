# ADR 009 — Clean Architecture

## Context

The system must remain maintainable and extensible as document intelligence capabilities grow.

## Decision

Adopt Clean Architecture with separate domain, application, infrastructure, and presentation layers for each bounded context.

## Alternatives Considered

- Monolithic, script-based Lambda functions: faster to prototype but harder to maintain and evolve.
- Hexagonal architecture: similar separation of concerns, but Clean Architecture is chosen for familiarity and documentation clarity.

## Consequences

- Improves separation of concerns, testability, and long-term maintainability.
- Requires discipline to avoid cross-layer dependencies.
- Encourages strong boundaries between business logic and infrastructure.

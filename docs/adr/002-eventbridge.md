# ADR 002 — EventBridge

## Context

The system requires reliable, decoupled orchestration between document lifecycle stages and support for multiple consumers of processing events.

## Decision

Use EventBridge as the central event router for domain events across Document Management, Document Processing, Document Intelligence, and Knowledge Base.

## Alternatives Considered

- SQS: good for queueing but less flexible for event routing and content-based filtering.
- SNS: supports pub/sub but lacks EventBridge's event structure and advanced routing semantics.

## Consequences

- Enables decoupled, publish-subscribe processing workflows with clear event contracts.
- Introduces configuration and operational overhead for event schemas, permissions, and bus management.
- Supports easier future expansion when new consumers subscribe to the same domain events.

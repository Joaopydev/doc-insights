# ADR 013 — AWS API Gateway (HTTP & WebSocket APIs)

## Context

The system exposes two distinct API patterns:

1. **Synchronous HTTP endpoints** for document upload, authentication, chat initiation, and message retrieval
2. **Asynchronous WebSocket connections** for real-time answer delivery and streaming updates to connected clients

Both require low-latency, highly available API frontends integrated with Lambda and managed identity/authorization.

## Decision

Use **AWS API Gateway** to provision and manage both APIs:

- **HTTP API**: RESTful endpoints for CRUD operations with JWT authorization via Lambda authorizers
- **WebSocket API**: For bi-directional communication with clients, routing through Lambda handlers for `$connect`, `$disconnect`, and EventBridge-triggered notifications

## Alternatives Considered

- **ALB (Application Load Balancer)**: Requires managing EC2/ECS infrastructure; over-engineered for Lambda-only architecture.
- **API Gateway REST API**: Deprecated in favor of HTTP API; would add latency and cost.
- **Custom WebSocket with API Gateway + Socket.io**: Socket.io adds complexity; native WebSocket support is simpler.
- **AppSync (GraphQL)**: Adds operational complexity; REST + WebSocket better fits current use case.

## Consequences

- **HTTP API Benefits**: Serverless, fully managed, integrated with Lambda, low-latency, cost-effective (~$0.35/million requests).
- **HTTP API Drawbacks**: Limited caching, request size limits (10MB), limited control over response transformation.
- **WebSocket Benefits**: Native real-time bidirectional communication, integrated with EventBridge, managed connection state.
- **WebSocket Drawbacks**: Connections incur hourly charges ($0.25/million connection-minutes); requires managing `$connect`/`$disconnect` state.
- **Authorization**: JWT validation enforced at Lambda layer via centralized error handler and request adapter.
- **Scalability**: Automatically scales; no cold-start concerns on API layer itself.

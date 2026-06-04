# ADR 008 — LocalStack

## Context

The team needs to validate AWS serverless behavior locally before deploying to cloud and without relying on a remote account.

## Decision

Use LocalStack to emulate AWS services such as Lambda, API Gateway, S3, DynamoDB, and EventBridge for local development and integration testing.

## Alternatives Considered

- Unit tests only: insufficient for validating event-driven, cross-service workflows.
- AWS dev account: slower and riskier for early development and experimentation.

## Consequences

- Faster local feedback loops and reduced dependency on cloud resources.
- Some AWS service behavior may differ from the real AWS environment.
- Requires bootstrapping infrastructure and maintaining LocalStack configuration.

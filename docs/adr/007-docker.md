# ADR 007 — Docker

## Context

Local development and integration testing require reproducible environments for AWS emulation and supporting services.

## Decision

Use Docker to run LocalStack and any auxiliary tooling needed for local AWS service emulation.

## Alternatives Considered

- Native AWS CLI only: less reproducible and harder to sandbox across developer machines.
- Remote dev environment: slow feedback loops and dependency on external infrastructure.

## Consequences

- Developers gain a consistent local environment that matches the AWS service topology.
- Requires Docker installed and adequate local resources.
- Enables easier onboarding and sharing of local infrastructure setup.

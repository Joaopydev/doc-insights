# ADR 006 — Serverless Framework

## Context

Infrastructure needs to be defined as code and deployed consistently for AWS serverless services, Lambda functions, and resources.

## Decision

Use Serverless Framework to declare AWS resources, function handlers, event bindings, and deployment pipelines.

## Alternatives Considered

- AWS CDK: powerful but more code-centric and heavier than necessary for this project scope.
- Terraform: robust IaC, but less optimized for Lambda-first service definitions and event integrations.

## Consequences

- Simplifies function and resource deployment for serverless architecture.
- Requires managing plugin compatibility for Python packaging and local development.
- Keeps infrastructure definitions alongside application configuration in a single framework.

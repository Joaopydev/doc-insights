# ADR 001 — AWS Lambda

## Context

Document processing must scale on demand and minimize infrastructure management overhead for asynchronous document ingestion, text extraction, AI analysis, and knowledge indexing.

## Decision

Use AWS Lambda for all serverless compute components, including API handlers, upload orchestration, text extraction, intelligence processing, and knowledge indexing.

## Alternatives Considered

- ECS/Fargate: offered containerization but introduced more infrastructure management and cost for intermittent workloads.
- EC2: provided full control but was incompatible with serverless scalability and rapid iteration goals.

## Consequences

- Simplified deployment and scaling through Lambda and AWS managed services.
- Additional attention required for cold starts, timeout boundaries, package size, and retry semantics.
- Encourages decomposition into small, focused functions aligned with bounded contexts.

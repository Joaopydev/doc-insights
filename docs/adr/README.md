# Architecture Decision Records (ADRs)

This directory contains all architecture decision records for the DocInsight project. ADRs document major technical decisions, the context that led to them, alternatives considered, and the consequences.

## ADR Index

### 1. Core Infrastructure & Platform

| #   | Title                                               | Decision                                        | Trade-offs                                           |
| --- | --------------------------------------------------- | ----------------------------------------------- | ---------------------------------------------------- |
| 001 | [AWS Lambda](001-aws-lambda.md)                     | Use Lambda for all serverless compute           | Managed scaling vs. cold start concerns              |
| 006 | [Serverless Framework](006-serverless-framework.md) | Use Serverless Framework for IaC                | Simplified deployment vs. plugin compatibility       |
| 007 | [Docker](007-docker.md)                             | Use Docker for reproducible Lambda environments | Consistency vs. image size management                |
| 008 | [LocalStack](008-localstack.md)                     | Use LocalStack for local AWS emulation          | Fast feedback loops vs. behavior divergence from AWS |

### 2. Data Storage

| #   | Title                                                  | Decision                            | Trade-offs                                                   |
| --- | ------------------------------------------------------ | ----------------------------------- | ------------------------------------------------------------ |
| 003 | [DynamoDB](003-dynamodb.md)                            | Use DynamoDB for metadata and state | Scalability vs. schema design complexity                     |
| 004 | [S3](004-s3.md)                                        | Use S3 for document storage         | Durability & cost vs. lifecycle management overhead          |
| 014 | [PostgreSQL with pgvector](014-postgresql-pgvector.md) | Use pgvector for embeddings storage | No vendor lock-in vs. scaling limitations beyond 10M vectors |

### 3. API & Authentication

| #   | Title                                           | Decision                                  | Trade-offs                                               |
| --- | ----------------------------------------------- | ----------------------------------------- | -------------------------------------------------------- |
| 013 | [API Gateway](013-api-gateway.md)               | Use API Gateway for HTTP & WebSocket APIs | Serverless simplicity vs. limited customization          |
| 016 | [JWT Authentication](016-jwt-authentication.md) | Use JWT for stateless auth                | Scalability & simplicity vs. token revocation complexity |

### 4. Event-Driven Orchestration & Messaging

| #   | Title                             | Decision                             | Trade-offs                                                    |
| --- | --------------------------------- | ------------------------------------ | ------------------------------------------------------------- |
| 002 | [EventBridge](002-eventbridge.md) | Use EventBridge for event routing    | Decoupled orchestration vs. operational complexity            |
| 012 | [SNS & SQS](012-sns-sqs.md)       | Use SNS (Textract) & SQS (questions) | Dual messaging patterns fit specific use cases vs. complexity |

### 5. AI & Document Processing

| #   | Title                               | Decision                             | Trade-offs                                                      |
| --- | ----------------------------------- | ------------------------------------ | --------------------------------------------------------------- |
| 011 | [AWS Textract](011-aws-textract.md) | Use Textract for document extraction | Accurate extraction with table/form detection vs. per-page cost |
| 005 | [OpenAI](005-openai.md)             | Use OpenAI for LLM & embeddings      | High-quality NLP vs. API dependency & hallucination risk        |

### 6. Performance & Caching

| #   | Title                         | Decision                   | Trade-offs                                                    |
| --- | ----------------------------- | -------------------------- | ------------------------------------------------------------- |
| 015 | [Redis](015-redis-caching.md) | Use Redis as caching layer | 100x faster lookups vs. VPC complexity & operational overhead |

### 7. Architecture & Design Patterns

| #   | Title                                                         | Decision                                       | Trade-offs                                                    |
| --- | ------------------------------------------------------------- | ---------------------------------------------- | ------------------------------------------------------------- |
| 009 | [Clean Architecture](009-clean-architecture.md)               | Adopt Clean Architecture with separated layers | Maintainability & testability vs. additional code scaffolding |
| 010 | [Event-Driven Architecture](010-event-driven-architecture.md) | Use event-driven design for orchestration      | Decoupled components vs. eventual consistency & complexity    |

---

## ADR Template

When creating a new ADR, use the following structure:

```markdown
# ADR NNN — [Title]

## Context

[Explain the issue or need that prompted this decision]

## Decision

[State the decision clearly]

## Alternatives Considered

[List alternatives and why they were rejected]

## Consequences

[Describe the implications, both positive and negative]
```

## How to Read ADRs

1. **For System Overview**: Read ADRs in numerical order or by category (above)
2. **For Specific Technology**: Look up in the index by category
3. **For Decision Rationale**: Read "Alternatives Considered" and "Consequences" sections
4. **For Implementation Details**: See DEPLOYMENT.md and WORKFLOW.md for specifics

## Key Decision Patterns

### Three-Tier Infrastructure Stack

- **Compute**: Lambda (ADR 001) with containers (ADR 007) deployed via Serverless Framework (ADR 006)
- **Storage**: S3 (ADR 004), DynamoDB (ADR 003), pgvector (ADR 014)
- **API**: API Gateway (ADR 013) with JWT auth (ADR 016)

### Event Orchestration

- **Primary**: EventBridge (ADR 002) for cross-service workflows
- **Secondary**: SNS (ADR 012) for Textract notifications
- **Queue**: SQS (ADR 012) for bounded question processing

### Data Flow

- Raw documents → S3 (ADR 004)
- Metadata → DynamoDB (ADR 003)
- Embeddings → pgvector (ADR 014)
- Cached embeddings → Redis (ADR 015)
- User tokens → JWT (ADR 016)

### Design Principles

- **Decoupling**: EventBridge (ADR 002) and event-driven architecture (ADR 010) eliminate tight coupling
- **Scalability**: Lambda auto-scaling (ADR 001) with serverless components throughout
- **Maintainability**: Clean Architecture (ADR 009) provides clear boundaries
- **Cost**: Pay-per-use services (Lambda, S3, DynamoDB) with Redis caching to reduce operational costs

---

## When to Add/Modify ADRs

**Add an ADR when:**

- Introducing a new major technology or service
- Making a significant architectural change
- Choosing between multiple viable approaches

**Modify an ADR when:**

- The original decision is superseded by a new one (mark as "Superseded")
- Consequences have changed significantly
- New evidence emerges about trade-offs

**Example supersession:**

```markdown
# ADR NNN — [Title]

**Status**: Superseded by [ADR XXX]

## Previous Context

...
```

---

## References

- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [Serverless Application Lens](https://docs.aws.amazon.com/wellarchitected/latest/serverless-applications-lens/)
- [Cloud Design Patterns](https://learn.microsoft.com/en-us/azure/architecture/patterns/)
- [Domain-Driven Design](https://www.domainlanguage.com/ddd/)
- [Building Event-Driven Applications](https://aws.amazon.com/blogs/compute/building-event-driven-architectures-on-aws/)

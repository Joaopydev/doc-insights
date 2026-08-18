# DocInsight - Document Intelligence API

A serverless, event-driven document intelligence platform built on AWS Lambda that enables intelligent document processing, analysis, and retrieval-augmented generation (RAG) over enterprise documents.

## Overview

DocInsight is an intelligent document analysis platform that enables businesses to:

- Upload and process complex documents (PDFs, contracts, reports, invoices, resumes)
- Extract text using AWS Textract
- Generate natural-language summaries using OpenAI
- Extract entities, clauses, and risk signals
- Query documents through an interactive chat interface
- Retrieve document insights using vector embeddings and semantic search

The platform uses a **clean architecture** and **event-driven design** to handle asynchronous document processing at scale with high resilience and observability.

## Architecture Overview

### Tech Stack

- **Compute**: AWS Lambda (Python 3.11)
- **API**: AWS API Gateway HTTP API
- **Real-time Communication**: AWS API Gateway WebSocket API
- **Orchestration**: AWS EventBridge
- **Storage**: AWS S3, AWS DynamoDB
- **Text Extraction**: AWS Textract
- **AI Processing**: OpenAI API
- **Vector Database**: PostgreSQL (Neon) with pgvector
- **Caching**: Redis
- **Message Queue**: AWS SQS
- **Notifications**: AWS SNS
- **Deployment**: Docker containers in ECR + Serverless Framework

### Service Architecture

```
User API Requests
├── /signup (POST) → Identity Service → Create User
├── /signin (POST) → Identity Service → Authenticate User
├── /document (POST) → Document Upload → S3 → EventBridge
├── /chat (POST) → Chat Service → EventBridge → Q&A Processing
├── /messages/{conversation_id} (GET) → Chat Service
└── WebSocket Connections → Real-time Notifications

Document Processing Pipeline
S3 Upload → EventBridge → Text Extraction → Indexing → Cache Update

Q&A Processing Pipeline
User Question → SQS Queue → LLM Processing → WebSocket Notification
```

## Project Structure

```
src/
├── chat/                    # Chat/Q&A Bounded Context
│   ├── application/        # Use cases and business logic
│   ├── domain/             # Domain entities
│   ├── infrastructure/      # Repository implementations
│   └── presentation/       # Controllers
├── identity/               # User Identity Bounded Context
├── processing/             # Document Processing Context
├── upload/                 # File Upload Context
├── functions/              # Lambda handlers
│   ├── create_document/
│   ├── signin/signup
│   ├── start_extraction_text/  # S3 trigger
│   ├── index_document/         # Indexing trigger
│   ├── ask_question/           # Chat API endpoint
│   ├── process_question/       # SQS processor
│   ├── textract_completed/     # SNS trigger
│   ├── question_processing/    # EventBridge trigger
│   ├── update_cache/           # Cache update handler
│   ├── get_message/            # Retrieve chat history
│   └── websocket_*/            # WebSocket handlers
├── errors/                 # Error handling and types
├── main/                   # Adapters, composers, config
└── shared/                 # Cross-cutting concerns
```

## Deployment

### Prerequisites

Set the following environment variables:

```bash
export ECR_IMAGE_URI=<your-ecr-image-uri>
export LAMBDA_SECURITY_GROUP_ID=<sg-id>
export SUBNET_ID=<subnet-1>
export SUBNET2_ID=<subnet-2>
export JWT_PRIVATE_KEY=<your-jwt-private-key>
export JWT_PUBLIC_KEY=<your-jwt-public-key>
export OPENAI_API_KEY=<your-openai-key>
export NEON_DATABASE_URL=<postgresql://...>
export REDIS_HOST=<redis-hostname>
export REDIS_PORT=6379
```

### Deploy to AWS

```bash
serverless deploy --stage prod
```

After deployment, you will receive:

- HTTP API endpoints for document upload, signin, signup, and chat
- WebSocket API endpoint for real-time communication
- Stack outputs with DynamoDB tables, S3 bucket, and queue ARNs

### Local Development

#### Setup

```bash
pip install -r requirements.txt
export PYTHONPATH=$(pwd)
```

#### Run Tests

```bash
pytest tests/
```

#### Emulate Locally

For local development with LocalStack and serverless-offline, refer to [ADR-008](docs/adr/008-localstack.md).

## API Endpoints

### Authentication

**Sign Up** (POST /signup)

```json
{
  "email": "user@example.com",
  "password": "securepass"
}
```

**Sign In** (POST /signin)

```json
{
  "email": "user@example.com",
  "password": "securepass"
}
```

### Documents

**Create/Upload Document** (POST /document)

```json
{
  "filename": "contract.pdf",
  "document": "<base64-encoded-pdf>"
}
```

### Chat

**Ask Question** (POST /chat)

```json
{
  "document_id": "doc-123",
  "question": "What are the key terms?"
}
```

**Get Messages** (GET /messages/{conversation_id})
Returns chat history for a conversation.

### WebSocket

Connect via WebSocket to receive real-time updates on:

- Document processing completion
- Chat message answers
- Cache invalidation events

## Event-Driven Workflows

### Document Processing Workflow

```
1. User uploads PDF → createDocument (HTTP)
   ├─ Store metadata in DynamoDB
   ├─ Upload file to S3
   └─ Publish: document.created

2. S3 Upload Complete → startExtracting (EventBridge trigger)
   ├─ Submit to AWS Textract
   └─ Store job_id in DynamoDB

3. Textract Completes → textractCompleted (SNS trigger)
   ├─ Retrieve extracted text from Textract
   ├─ Store extracted text in S3
   └─ Publish: textract.completed

4. Text Extracted → indexDocument (EventBridge trigger)
   ├─ Generate embeddings with OpenAI
   ├─ Store vectors in Neon pgvector
   └─ Update cache with Redis
   └─ Publish: document.indexed
```

### Question-Answering Workflow

```
1. User asks question → askQuestion (HTTP)
   ├─ Create conversation/message record
   ├─ Publish: QuestionAsked event
   └─ Return HTTP 202 (Accepted)

2. EventBridge routes → questionProcessing
   ├─ Check Redis cache for embeddings
   │
   ├─ CACHE HIT (embeddings exist):
   │  ├─ Generate question embedding
   │  ├─ Semantic search + LLM call
   │  ├─ Store answer in DynamoDB
   │  └─ Publish: QuestionAnswered event ✓ FAST PATH (~1-2s)
   │
   └─ CACHE MISS (embeddings not cached):
      ├─ Publish message to SQS queue
      └─ Continues to Step 3...

3. SQS processes (cache miss only) → processQuestion
   ├─ Retrieve embeddings from pgvector
   ├─ Generate question embedding
   ├─ Semantic search + LLM call
   ├─ Store answer in DynamoDB
   └─ Publish: QuestionAnswered event (SLOW PATH ~5-15s)

4. Answer ready → websocketPostToConnection
   ├─ Send answer to connected WebSocket clients
   └─ Notify user via real-time WebSocket
```

**Key Insight**: `questionProcessing` decides whether to use fast path (cache hit) or queue for deferred processing (cache miss). `processQuestion` only runs when cache miss occurs.

## Configuration Files

### serverless.yml

The `serverless.yml` defines:

- **Provider**: AWS, us-east-1, Python 3.11, x86_64
- **Functions**: 14 Lambda functions with container image deployment
- **Events**: HTTP API, EventBridge, SQS, SNS, WebSocket triggers
- **Resources**: S3 bucket, 5 DynamoDB tables, SQS queues, SNS topic
- **IAM Permissions**: Scoped to S3, DynamoDB, Textract, EventBridge, and SQS operations

### Environment Variables

See `.env.example` and deployment section for required variables.

## Documentation

- [Architecture & Domain Design](docs/architecture.md) - System vision, bounded contexts, aggregates
- [Architecture Decision Records](docs/adr/README.md) - Technical decisions and rationale
  - **Infrastructure & Compute**:
    - ADR-001: AWS Lambda for serverless compute
    - ADR-006: Serverless Framework for Infrastructure as Code
    - ADR-007: Docker containers for Lambda images
    - ADR-008: LocalStack for local development
  - **Data Storage**:
    - ADR-003: DynamoDB for metadata and state
    - ADR-004: S3 for document storage
    - ADR-014: PostgreSQL with pgvector for embeddings
  - **API & Authentication**:
    - ADR-013: API Gateway for HTTP and WebSocket APIs
    - ADR-016: JWT for stateless authentication
  - **Event-Driven Orchestration**:
    - ADR-002: EventBridge for event routing
    - ADR-012: SNS & SQS for asynchronous messaging
  - **AI & Processing**:
    - ADR-005: OpenAI for LLM and embeddings
    - ADR-011: AWS Textract for document extraction
  - **Caching & Performance**:
    - ADR-015: Redis for in-memory caching
  - **Architecture**:
    - ADR-009: Clean Architecture principles
    - ADR-010: Event-driven architecture design

## Development Guidelines

### Code Organization

- **Domain Layer**: Pure business logic, no infrastructure dependencies
- **Application Layer**: Use cases, orchestration, coordination
- **Infrastructure Layer**: Database, API, external service adapters
- **Presentation Layer**: HTTP controllers, WebSocket handlers

### Error Handling

Centralized error handling via `src/errors/error_handler.py` with custom exception types in `src/errors/types/`.

### Dependency Injection

Use composer pattern in `src/main/composers/` to wire dependencies for each function.

## Monitoring & Observability

The platform logs to CloudWatch with:

- Lambda invocation metrics
- DynamoDB read/write capacity
- Textract job status
- OpenAI API usage
- EventBridge rule executions
- WebSocket connection events

## Contributing

1. Follow the bounded context structure
2. Use domain-driven design principles
3. Add comprehensive logging for observability
4. Update architecture docs when adding new bounded contexts
5. Update ADRs when making architectural decisions

## License

Proprietary - All rights reserved.

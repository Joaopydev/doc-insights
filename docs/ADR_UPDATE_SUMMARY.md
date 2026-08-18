# ADR Update Summary

## Overview

Added 6 new Architecture Decision Records (ADRs 011-016) to document infrastructure technologies that were not previously captured. All existing ADRs (001-010) remain valid and unchanged.

## New ADRs Created

### ADR-011: AWS Textract for Document Text Extraction

**File**: `docs/adr/011-aws-textract.md`

**Decision**: Use AWS Textract as the primary document text extraction service with asynchronous processing via SNS notifications.

**Key Points**:

- Accurate text extraction with native table and form detection
- Asynchronous processing model with job state management
- Cost: ~$0.015-1.00 per page depending on document type
- SNS integration for fault tolerance and decoupling

**Alternatives Rejected**:

- Open-source OCR (Tesseract, PaddleOCR)
- Claude/GPT-4 Vision API
- AWS Comprehend

### ADR-012: AWS SNS & SQS for Asynchronous Messaging

**File**: `docs/adr/012-sns-sqs.md`

**Decision**: Use SNS for Textract completion notifications and SQS with DLQ for question processing pipeline orchestration.

**Key Points**:

- **SNS**: Push notifications, immediate delivery, no polling overhead
- **SQS**: Visibility timeout control, retry semantics, DLQ for error handling
- Two distinct messaging patterns for two different problems
- Rate-limiting for bounded question processing (LLM API calls)

**Alternatives Rejected**:

- EventBridge for all messaging (less granular visibility control)
- Kinesis Streams (over-engineered)
- Redis pub/sub (durability concerns)

### ADR-013: AWS API Gateway (HTTP & WebSocket APIs)

**File**: `docs/adr/013-api-gateway.md`

**Decision**: Use API Gateway for both HTTP REST endpoints and WebSocket connections.

**Key Points**:

- HTTP API for synchronous operations (create, read, update)
- WebSocket API for real-time bidirectional communication
- JWT authorization at Lambda layer
- Fully managed, serverless, low-latency
- Cost: ~$0.35/million HTTP requests, $0.25/million connection-minutes for WebSocket

**Alternatives Rejected**:

- ALB (requires managing EC2/ECS)
- API Gateway REST API (deprecated)
- Custom WebSocket with Socket.io (unnecessary complexity)
- AppSync GraphQL (overkill for REST + WebSocket)

### ADR-014: PostgreSQL with pgvector for Vector Storage

**File**: `docs/adr/014-postgresql-pgvector.md`

**Decision**: Use PostgreSQL (Neon) with pgvector extension for storing and searching document embeddings.

**Key Points**:

- ACID compliance for embedding integrity
- Native vector similarity operators (`<->` for Euclidean distance)
- IVFFlat or HNSW indexes for efficient ANN search
- No vendor lock-in; portable solution
- Scales to ~10M vectors efficiently; beyond that consider Pinecone/Milvus
- Single database reduces operational overhead

**Alternatives Rejected**:

- Pinecone (vendor lock-in, higher cost)
- Weaviate (operational complexity)
- Milvus (requires Kubernetes)
- Redis with vector extensions (no durability, no ACID)
- DynamoDB alone (no native vector search)

### ADR-015: Redis for Caching Layer

**File**: `docs/adr/015-redis-caching.md`

**Decision**: Use Redis as distributed in-memory cache between Lambda functions and PostgreSQL.

**Key Points**:

- Cache-aside pattern: check Redis before querying pgvector
- 100x faster than database queries (microseconds vs milliseconds)
- Document embeddings cache: `doc:{document_id}:embeddings`, TTL 1 hour
- Conversation cache: `conv:{conversation_id}:*`, TTL 24 hours
- Reduces database load and latency significantly

**Alternatives Rejected**:

- DynamoDB as cache (already used for metadata, adds cost and complexity)
- ElastiCache Memcached (less feature-rich)
- Application-level in-memory (no state sharing across Lambda instances)
- CloudFront/API Gateway (caches HTTP responses, not embeddings)

**Trade-offs**:

- Requires VPC networking (adds latency but mitigated by external Redis services)
- Data loss acceptable (cache-aside handles misses)
- Operational complexity for monitoring and key eviction

### ADR-016: JWT (JSON Web Tokens) for Stateless Authentication

**File**: `docs/adr/016-jwt-authentication.md`

**Decision**: Use JWT with RS256 signature for stateless, claim-based authentication and authorization.

**Key Points**:

- Stateless: no server-side session store required
- RS256 (RSA SHA-256) with application-managed key pair
- Token lifespan: 24 hours (configurable)
- Private key: AWS Secrets Manager, Public key: used for validation
- Claim-based access control: user_id embedded in token

**Alternatives Rejected**:

- OAuth 2.0 / OpenID Connect (overkill, adds complexity)
- API Keys (limited, no claims, harder to rotate)
- Lambda authorizers (adds latency)
- Amazon Cognito (vendor lock-in, overhead, cost)

**Trade-offs**:

- Token revocation complexity (mitigated by short TTL, Redis blacklist if needed)
- Key rotation overhead (managed with dual-key support)
- Larger token size than session cookies
- Security critical: private key exposure requires immediate rotation

## Updated Documentation Files

### 1. `docs/architecture.md`

- **Change**: Updated "ADRs" section to categorize and link all 16 ADRs
- **Organization**: Grouped by category:
  - Core Infrastructure & Platform (4)
  - Storage & Data (3)
  - API & Real-time Communication (2)
  - Event-Driven Orchestration & Messaging (2)
  - AI & Document Processing (2)
  - Performance & Caching (1)
  - Architecture & Design Patterns (2)

### 2. `docs/adr/README.md` (NEW)

- **Content**: Comprehensive ADR index and guide
- **Features**:
  - Matrix view of all 16 ADRs with decisions and trade-offs
  - Categorized by technology domain
  - Key decision patterns and design principles
  - When to add/modify ADRs
  - ADR template for future additions

### 3. `README.md`

- **Change**: Updated documentation section with organized ADR links
- **Categories**:
  - Infrastructure & Compute (4)
  - Data Storage (3)
  - API & Authentication (2)
  - Event-Driven Orchestration (2)
  - AI & Processing (2)
  - Caching & Performance (1)
  - Architecture (2)

### 4. `docs/QUICK_REFERENCE.md`

- **New Section**: "Technology Stack & Architecture Decisions"
  - Quick links to all 16 ADRs
  - Organized by infrastructure layer
- **New Section**: "Technology Reference"
  - Comprehensive tables for:
    - Infrastructure Technologies (4)
    - Data Storage (4)
    - APIs & Authentication (3)
    - Event-Driven Orchestration (3)
    - AI & Document Processing (2)
    - Design Patterns (2)
  - Each entry links to relevant ADR and AWS service

## Coverage Summary

### All Infrastructure Technologies Now Documented

| Category      | Technologies                                     | ADRs               |
| ------------- | ------------------------------------------------ | ------------------ |
| **Compute**   | Lambda, Docker, Serverless Framework, LocalStack | 001, 006, 007, 008 |
| **Data**      | S3, DynamoDB, PostgreSQL+pgvector, Redis         | 003, 004, 014, 015 |
| **APIs**      | API Gateway (HTTP/WebSocket), JWT Auth           | 013, 016           |
| **Messaging** | EventBridge, SNS, SQS                            | 002, 012           |
| **AI**        | OpenAI, Textract                                 | 005, 011           |
| **Patterns**  | Clean Architecture, Event-Driven                 | 009, 010           |

**Total**: 16 ADRs covering all major infrastructure and architecture decisions

## Key Improvements

1. **Completeness**: All infrastructure technologies now have documented decisions
2. **Traceability**: Every technology links to its ADR explaining the rationale
3. **Navigation**: Categorized and indexed ADRs make finding decisions easy
4. **Consistency**: All new ADRs follow same format as existing ones
5. **Accessibility**: Multiple entry points (README, QUICK_REFERENCE, architecture.md)
6. **Reference**: ADR README provides index, template, and guidance for future additions

## How to Use the Updated Documentation

### For Understanding a Technology

1. Look up technology in QUICK_REFERENCE.md Technology Reference section
2. Click the ADR link to read full decision and rationale
3. Review "Consequences" and "Alternatives Considered" for context

### For System Architecture

1. Start with architecture.md categorized ADR list
2. Review ADR README for high-level patterns and relationships
3. Dive into specific ADRs for detailed trade-offs

### For Adding New Technology

1. Check ADR README for template
2. Follow same format (Context, Decision, Alternatives, Consequences)
3. Add to appropriate category in architecture.md and QUICK_REFERENCE.md
4. Update ADR README index

---

**Documentation Complete**: All 16 ADRs created and integrated into project documentation ✅
**Last Updated**: 2024-01-15

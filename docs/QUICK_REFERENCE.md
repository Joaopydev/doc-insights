# Quick Reference Guide

## Technology Stack & Architecture Decisions

### Infrastructure & Platform

- **Compute**: Lambda (Python 3.11) — [ADR-001](../adr/001-aws-lambda.md)
- **Containers**: Docker + ECR — [ADR-007](../adr/007-docker.md)
- **Infrastructure as Code**: Serverless Framework — [ADR-006](../adr/006-serverless-framework.md)
- **Local Development**: LocalStack — [ADR-008](../adr/008-localstack.md)

### Storage

- **Documents**: S3 — [ADR-004](../adr/004-s3.md)
- **Metadata**: DynamoDB — [ADR-003](../adr/003-dynamodb.md)
- **Embeddings**: PostgreSQL + pgvector — [ADR-014](../adr/014-postgresql-pgvector.md)
- **Caching**: Redis — [ADR-015](../adr/015-redis-caching.md)

### APIs & Security

- **HTTP & WebSocket APIs**: API Gateway — [ADR-013](../adr/013-api-gateway.md)
- **Authentication**: JWT — [ADR-016](../adr/016-jwt-authentication.md)

### Event-Driven Architecture

- **Event Router**: EventBridge — [ADR-002](../adr/002-eventbridge.md)
- **Messaging**: SNS (Textract), SQS (Questions) — [ADR-012](../adr/012-sns-sqs.md)
- **Event-Driven Design**: [ADR-010](../adr/010-event-driven-architecture.md)

### AI & Document Processing

- **Text Extraction**: AWS Textract — [ADR-011](../adr/011-aws-textract.md)
- **LLM & Embeddings**: OpenAI — [ADR-005](../adr/005-openai.md)

### Design Principles

- **Clean Architecture** — [ADR-009](../adr/009-clean-architecture.md)

**For full architecture decision rationale, see [ADR README](../adr/README.md)**

---

## Key Files & Their Purposes

| File                              | Purpose                                                                                             |
| --------------------------------- | --------------------------------------------------------------------------------------------------- |
| `serverless.yml`                  | Infrastructure as Code - defines Lambda functions, API endpoints, event triggers, and AWS resources |
| `Dockerfile`                      | Container image for Lambda functions (Python 3.11 runtime)                                          |
| `requirements.txt`                | Python dependencies (boto3, pydantic, openai, redis, langchain, etc.)                               |
| `src/functions/*/handler.py`      | Lambda handler entry points for each function                                                       |
| `src/chat/application/use_cases/` | Business logic for chat domain                                                                      |
| `src/identity/`                   | User authentication and identity management                                                         |
| `docs/architecture.md`            | System architecture, bounded contexts, C4 diagrams                                                  |
| `docs/WORKFLOW.md`                | Detailed workflows for document processing and Q&A                                                  |
| `docs/DEPLOYMENT.md`              | Deployment guide and configuration reference                                                        |
| `docs/adr/README.md`              | Architecture Decision Records index                                                                 |

## Common Tasks

### Deploy to AWS

```bash
export ECR_IMAGE_URI=<your-ecr-uri>
export JWT_PRIVATE_KEY=<your-key>
export JWT_PUBLIC_KEY=<your-key>
export OPENAI_API_KEY=<your-key>
# ... other env vars

# Build and push Docker image
docker build -t docinsight:latest .
docker tag docinsight:latest $ECR_IMAGE_URI
docker push $ECR_IMAGE_URI

# Deploy stack
serverless deploy --stage prod
```

### Add New Lambda Function

1. Create handler in `src/functions/<function-name>/handler.py`
2. Add function definition to `serverless.yml`:
   ```yaml
   functions:
     myFunction:
       image:
         uri: ${env:ECR_IMAGE_URI}
         command:
           - src.functions.my_function.handler.handler
       events:
         - httpApi:
             path: /my-path
             method: POST
       timeout: 15
   ```
3. Update Docker image build
4. Deploy: `serverless deploy`

### Update DynamoDB Schema

1. Modify table definition in `serverless.yml` (Resources section)
2. Note: Changing partition key requires creating new table and migrating data
3. Deploy: `serverless deploy`

### Add EventBridge Event Pattern

1. Define event in application code (emit to EventBridge)
2. Add consumer function to `serverless.yml`:
   ```yaml
   events:
     - eventBridge:
         pattern:
           source: [your.source]
           detail-type: [YourEventType]
   ```
3. Deploy: `serverless deploy`

### Monitor Lambda Function

```bash
# View recent logs
serverless logs -f functionName --stage dev --tail

# View metrics in CloudWatch
aws cloudwatch get-metric-statistics \
  --metric-name Duration \
  --namespace AWS/Lambda \
  --dimensions Name=FunctionName,Value=document-analyzer-api-dev-functionName \
  --start-time 2024-01-15T00:00:00Z \
  --end-time 2024-01-15T23:59:59Z \
  --period 3600 \
  --statistics Average,Maximum
```

### Query DynamoDB Table

```bash
# List items
aws dynamodb scan \
  --table-name document-table \
  --region us-east-1

# Get specific item
aws dynamodb get-item \
  --table-name document-table \
  --key '{"id":{"S":"doc-123"}}'

# Query by GSI
aws dynamodb query \
  --table-name document-table \
  --index-name storage-key-index \
  --key-condition-expression "s3_key = :key" \
  --expression-attribute-values '{":key":{"S":"user-1/raw/doc-123.pdf"}}'
```

### Test Workflow Locally

```bash
# 1. Start LocalStack
docker-compose -f docker-compose.localstack.yml up -d

# 2. Deploy to LocalStack
serverless deploy --stage local

# 3. Test endpoint
curl -X POST http://localhost:3000/document \
  -H "Authorization: Bearer <test-jwt>" \
  -H "Content-Type: application/json" \
  -d '{"filename":"test.pdf","document":"base64..."}'

# 4. View LocalStack logs
docker logs localstack_main
```

## Architecture Quick Reference

### Event Flow: Document Upload → Processing

```
1. POST /document (HTTP) → createDocument
   └─ Save to S3 bucket (/raw/*)
   └─ Save metadata to DynamoDB

2. S3 notification (EventBridge) → startExtracting
   └─ Submit to AWS Textract
   └─ Update DynamoDB with job_id

3. Textract completion (SNS) → textractCompleted
   └─ Retrieve extracted text
   └─ Save to S3 (/extracted/*)
   └─ Update status in DynamoDB

4. S3 notification (EventBridge) → indexDocument
   └─ Generate embeddings (OpenAI)
   └─ Store vectors in PostgreSQL (pgvector)
   └─ Cache in Redis
   └─ Update status to "indexed"
```

### Event Flow: Question-Answering

```
1. POST /chat (HTTP) → askQuestion
   └─ Create message in DynamoDB
   └─ Emit QuestionAsked event

2. EventBridge QuestionAsked → questionProcessing
   ├─ Check Redis cache for embeddings
   │
   ├─ CACHE HIT:
   │  ├─ Semantic search + LLM
   │  ├─ Store answer (fast path)
   │  └─ Emit QuestionAnswered → Skip to Step 5
   │
   └─ CACHE MISS:
      ├─ Publish to SQS queue
      └─ Continue to Step 3...

3. EventBridge UpdateCache → updateCache
   └─ Invalidate conversation cache

4. SQS message → processQuestion (cache miss only)
   ├─ Retrieve embeddings from pgvector
   ├─ Semantic search + LLM
   ├─ Store answer in DynamoDB
   └─ Emit QuestionAnswered event

5. EventBridge QuestionAnswered → websocketPostToConnection
   └─ Send answer via WebSocket to client
```

5. EventBridge QuestionAnswered → websocketPostToConnection
   └─ Send answer via WebSocket to client

6. WebSocket $connect → websocketConnect
   └─ Store connection in DynamoDB

7. WebSocket $disconnect → websocketDisconnect
   └─ Remove connection from DynamoDB

````

## DynamoDB Table Quick Reference

### document-table

- **PK**: `id` (document ID)
- **GSI**: `s3_key`, `textract_job_id`, `extracted_text_key`
- **Status values**: `uploaded`, `extracting`, `text_extracted`, `indexed`, `failed`

### chat-table

- **PK**: `id` (message ID)
- **GSI**: `conversation_id`, `document_id`
- **Attributes**: `conversation_id`, `document_id`, `user_id`, `role` (user|assistant), `content`, `timestamp`, `status`

### conversation-table

- **PK**: `id` (conversation ID)
- **GSI**: `document_id`
- **Attributes**: `user_id`, `created_at`, `message_count`

### user-table

- **PK**: `id` (user ID)
- **GSI**: `email`
- **Attributes**: `email`, `password_hash`, `created_at`

### connections-table

- **PK**: `connection_id` (WebSocket connection ID)
- **GSI**: `user_id`
- **Attributes**: `user_id`, `connected_at`, `last_heartbeat`

## Lambda Functions Matrix

| Function                    | Trigger          | Timeout | VPC | Process             |
| --------------------------- | ---------------- | ------- | --- | ------------------- |
| `createDocument`            | HTTP POST        | 15s     | No  | Upload metadata     |
| `signin`                    | HTTP POST        | 15s     | No  | Auth user           |
| `signup`                    | HTTP POST        | 15s     | No  | Register user       |
| `startExtracting`           | EventBridge (S3) | 15s     | No  | Submit to Textract  |
| `textractCompleted`         | SNS              | 15s     | No  | Get extracted text  |
| `indexDocument`             | EventBridge (S3) | 15s     | No  | Generate embeddings |
| `askQuestion`               | HTTP POST        | 15s     | No  | Create question     |
| `questionProcessing`        | EventBridge      | 15s     | Yes | Check cache + route |
| `processQuestion`           | SQS              | 30s     | Yes | LLM (cache miss only) |
| `updateCache`               | EventBridge      | 15s     | Yes | Invalidate cache    |
| `getMessages`               | HTTP GET         | 15s     | No  | Fetch history       |
| `websocketConnect`          | WebSocket        | 15s     | No  | Store connection    |
| `websocketDisconnect`       | WebSocket        | 15s     | No  | Remove connection   |
| `websocketPostToConnection` | EventBridge      | 15s     | No  | Send to client      |

## Environment Variables

**Required:**

- `BUCKET_NAME`: S3 bucket for document storage
- `DOCUMENT_TABLE`, `CHAT_TABLE`, `USER_TABLE`, `CONVERSATION_TABLE`, `CONNECTIONS_TABLE`: DynamoDB tables
- `JWT_PRIVATE_KEY`, `JWT_PUBLIC_KEY`: For JWT validation
- `OPENAI_API_KEY`: OpenAI API access
- `NEON_DATABASE_URL`: PostgreSQL with pgvector
- `REDIS_HOST`, `REDIS_PORT`: Redis cache

**Optional:**

- `WEBSOCKET_ENDPOINT`: WebSocket API endpoint
- `TEXTRACT_ROLE_ARN`: IAM role for Textract
- `TEXTRACT_TOPIC_ARN`: SNS topic for Textract notifications
- `QUESTIONS_QUEUE`: SQS queue for questions

## Error Codes

| Code              | HTTP | Meaning                  |
| ----------------- | ---- | ------------------------ |
| `INVALID_REQUEST` | 400  | Malformed request        |
| `UNAUTHORIZED`    | 401  | Missing/invalid JWT      |
| `FORBIDDEN`       | 403  | Insufficient permissions |
| `NOT_FOUND`       | 404  | Resource not found       |
| `CONFLICT`        | 409  | Duplicate (email exists) |
| `INTERNAL_ERROR`  | 500  | Unexpected error         |

## Performance Targets

- Document upload: < 1 second
- Textract submission: < 5 seconds
- Text extraction: 5-30 seconds (depends on document size)
- Embedding generation: 5-30 seconds (depends on chunk count)
- Question answer: 5-15 seconds (LLM inference time)
- WebSocket delivery: < 1 second (real-time)

## Cost per Operation

| Operation                           | Estimated Cost |
| ----------------------------------- | -------------- |
| Document upload                     | $0.01          |
| Text extraction (Textract)          | $1.00          |
| Embedding generation (OpenAI)       | $0.02          |
| Question → Answer                   | $0.05          |
| **Total per document + 1 question** | **~$1.08**     |

## Useful AWS CLI Commands

```bash
# Deploy
serverless deploy --stage prod

# View stack
serverless info --stage dev

# Logs
serverless logs -f functionName --stage dev --tail

# Invoke locally
serverless invoke local --function functionName --data '{"key":"value"}'

# Remove stack
serverless remove --stage dev

# List all functions
serverless list functions --stage dev

# List deployed services
aws cloudformation list-stacks --query 'StackSummaries[?contains(StackName, `document-analyzer`)]'
````

## Technology Reference

### Infrastructure Technologies

| Technology               | Purpose                     | ADR                                           | AWS Service    |
| ------------------------ | --------------------------- | --------------------------------------------- | -------------- |
| **Lambda**               | Serverless compute runtime  | [ADR-001](../adr/001-aws-lambda.md)           | AWS Lambda     |
| **Docker**               | Container images for Lambda | [ADR-007](../adr/007-docker.md)               | ECR            |
| **Serverless Framework** | Infrastructure as Code      | [ADR-006](../adr/006-serverless-framework.md) | CloudFormation |
| **LocalStack**           | Local AWS emulation         | [ADR-008](../adr/008-localstack.md)           | Docker         |

### Data Storage

| Technology                | Purpose           | ADR                                          | Config                            |
| ------------------------- | ----------------- | -------------------------------------------- | --------------------------------- |
| **S3**                    | Document storage  | [ADR-004](../adr/004-s3.md)                  | `docinsight-raw-documents` bucket |
| **DynamoDB**              | Metadata & state  | [ADR-003](../adr/003-dynamodb.md)            | 5 tables, on-demand billing       |
| **PostgreSQL + pgvector** | Vector embeddings | [ADR-014](../adr/014-postgresql-pgvector.md) | Neon (env: NEON_DATABASE_URL)     |
| **Redis**                 | Caching layer     | [ADR-015](../adr/015-redis-caching.md)       | Cache-aside pattern, 1hr TTL      |

### APIs & Authentication

| Technology                | Purpose           | ADR                                         | Endpoints                                     |
| ------------------------- | ----------------- | ------------------------------------------- | --------------------------------------------- |
| **API Gateway HTTP**      | REST endpoints    | [ADR-013](../adr/013-api-gateway.md)        | /document, /signin, /signup, /chat, /messages |
| **API Gateway WebSocket** | Real-time updates | [ADR-013](../adr/013-api-gateway.md)        | $connect, $disconnect, EventBridge-triggered  |
| **JWT**                   | Token-based auth  | [ADR-016](../adr/016-jwt-authentication.md) | RS256 signed tokens, 24hr expiry              |

### Event-Driven Orchestration

| Technology      | Purpose                   | ADR                                  | Config                                          |
| --------------- | ------------------------- | ------------------------------------ | ----------------------------------------------- |
| **EventBridge** | Event routing             | [ADR-002](../adr/002-eventbridge.md) | Multiple rules for S3, Textract, custom sources |
| **SNS**         | Textract notifications    | [ADR-012](../adr/012-sns-sqs.md)     | Topic: `textract-document-completed`            |
| **SQS**         | Question processing queue | [ADR-012](../adr/012-sns-sqs.md)     | Queue: `question-queue-service`, DLQ enabled    |

### AI & Document Processing

| Technology       | Purpose             | ADR                                   | Config                                                       |
| ---------------- | ------------------- | ------------------------------------- | ------------------------------------------------------------ |
| **AWS Textract** | Document extraction | [ADR-011](../adr/011-aws-textract.md) | Async via SNS notifications                                  |
| **OpenAI API**   | LLM & embeddings    | [ADR-005](../adr/005-openai.md)       | Embeddings: text-embedding-3-small, LLM: gpt-4/gpt-3.5-turbo |

### Design Patterns

| Pattern                | ADR                                                | Description                                                        |
| ---------------------- | -------------------------------------------------- | ------------------------------------------------------------------ |
| **Clean Architecture** | [ADR-009](../adr/009-clean-architecture.md)        | Separated domain, application, infrastructure, presentation layers |
| **Event-Driven**       | [ADR-010](../adr/010-event-driven-architecture.md) | Async orchestration via EventBridge; decoupled services            |

## Resources & Documentation Links

- [Architecture Decision Records](../adr/README.md) - Full ADR index with rationale
- [AWS Lambda Best Practices](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
- [EventBridge Routing Rules](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-event-patterns.html)
- [DynamoDB Design Patterns](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/BestPractices.html)
- [Serverless Framework Guide](https://www.serverless.com/framework/docs)
- [AWS Textract Documentation](https://docs.aws.amazon.com/textract/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [pgvector Documentation](https://github.com/pgvector/pgvector)
- [Redis Documentation](https://redis.io/docs/)
- [AWS API Gateway](https://docs.aws.amazon.com/apigateway/)
- [JWT.io - Token Debugger](https://jwt.io/)

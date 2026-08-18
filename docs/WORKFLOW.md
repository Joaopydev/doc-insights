# DocInsight Workflows

This document describes the actual workflows implemented in the DocInsight system, including data flow, event routing, and component interactions.

## Document Processing Workflow

The document processing workflow handles document upload, text extraction, and indexing.

```
Timeline: ~30-60 seconds for document to be fully indexed
```

### Step 1: Document Upload (createDocument)

**Trigger:** User POST to `/document` endpoint

**Function:** `createDocument` (HTTP API → Lambda)

**Operations:**

1. Validate JWT token (auth_required=true)
2. Parse request body (filename, document content)
3. Generate unique document_id
4. Extract user_id from JWT
5. Create S3 key: `{user_id}/raw/{document_id}.pdf`
6. Upload file to S3: `docinsight-raw-documents`
7. Store document metadata in DynamoDB `document-table`:
   - `id` (PK): document_id
   - `s3_key`: S3 location of raw PDF
   - `status`: "uploaded"
   - `owner_id`: user_id
   - `upload_timestamp`: ISO timestamp
   - Other fields: filename, file_size, content_type

**Response:** HTTP 201 with document_id

**Example:**

```json
POST /document
Authorization: Bearer <jwt_token>
Content-Type: application/json
{
  "filename": "contract.pdf",
  "document": "base64-encoded-pdf-content..."
}

Response:
{
  "document_id": "doc-550e8400-e29b-41d4-a716-446655440000",
  "status": "uploaded"
}
```

### Step 2: S3 Trigger → Text Extraction (startExtracting)

**Trigger:** S3 EventBridge notification (Object Created event for `*/raw/*` prefix)

**Function:** `startExtracting` (EventBridge rule → Lambda)

**Event Pattern:**

```yaml
source: [aws.s3]
detail-type: [Object Created]
detail:
  bucket:
    name: [docinsight-raw-documents]
  object:
    key:
      - wildcard: "*/raw/*"
```

**Operations:**

1. Extract S3 key from event: `{user_id}/raw/{document_id}.pdf`
2. Extract document_id from key
3. Query DynamoDB `document-table` for document_id
4. Call AWS Textract `StartDocumentAnalysis`:
   - Document location: `s3://docinsight-raw-documents/{s3_key}`
   - SNS notification topic: `textract-document-completed`
   - IAM role with Textract:StartDocumentAnalysis permission
5. Store Textract job_id in DynamoDB:
   - Update `document-table` item
   - Add `textract_job_id` field
   - Update `status` to "extracting"

**Textract Configuration:**

- Uses SNS for async completion notifications
- Role: `textract-publish-role` can publish to SNS topic
- Textract output includes page data, extracted text, confidence scores

**Delay:** ~5-30 seconds depending on document size

### Step 3: Textract Completion → Retrieve Results (textractCompleted)

**Trigger:** SNS notification from AWS Textract

**Function:** `textractCompleted` (SNS → Lambda)

**SNS Setup:**

- Topic: `textract-document-completed`
- Subscription: Lambda `textractCompleted`
- Permission: SNS principal can invoke Lambda

**Operations:**

1. Parse SNS message to extract job_id and status
2. If status != "SUCCEEDED", log error and exit
3. Call AWS Textract `GetDocumentAnalysis`:
   - Use stored job_id
   - Retrieve all pages and extracted text
4. Aggregate extracted text from all pages
5. Save extracted text to S3:
   - New S3 key: `{user_id}/extracted/{document_id}.txt`
   - Content: Concatenated text from all pages
   - Metadata: Page count, confidence, extraction metadata
6. Update DynamoDB `document-table`:
   - Add `extracted_text_key` field with S3 location
   - Add `extracted_text_size` field
   - Update `status` to "text_extracted"
   - Add `textract_confidence` field

**Error Handling:**

- If extraction fails, set status to "extraction_failed"
- Log error details to CloudWatch
- No retry mechanism (Textract handles retries)

**Delay:** Immediate once SNS trigger fires

### Step 4: Extracted Text Available → Index & Embed (indexDocument)

**Trigger:** S3 EventBridge notification (Object Created event for `*/extracted/*` prefix)

**Function:** `indexDocument` (EventBridge rule → Lambda)

**Event Pattern:**

```yaml
source: [aws.s3]
detail-type: [Object Created]
detail:
  bucket:
    name: [docinsight-raw-documents]
  object:
    key:
      - wildcard: "*/extracted/*"
```

**Configuration:**

- Timeout: 15 seconds
- No VPC required

**Operations:**

1. Extract S3 key and document_id from event
2. Query DynamoDB `document-table` for document metadata
3. Retrieve extracted text from S3:
   - Read `{user_id}/extracted/{document_id}.txt`
4. Split text into chunks using `langchain_text_splitters`:
   - Chunk size: 1024 tokens (configurable)
   - Overlap: 128 tokens
   - Strategy: TokenTextSplitter or RecursiveCharacterTextSplitter
5. For each chunk:
   - Call OpenAI API `embeddings`:
     - Model: text-embedding-3-small
     - Input: chunk text
     - Output: 1536-dimensional vector
   - Store in PostgreSQL via pgvector:
     - Table: `knowledge_records` or similar
     - Columns: chunk_id, document_id, chunk_text, embedding, metadata
   - Cache in Redis (with TTL):
     - Key: `doc:{document_id}:embeddings`
     - Value: JSON with chunks and vectors
6. Update DynamoDB `document-table`:
   - Add `indexed_at` timestamp
   - Add `chunk_count` field
   - Update `status` to "indexed"

**VPC Configuration (Future):**

- Currently: No VPC
- Planned: VPC access for Redis and Neon database
- Requires: Security group ID, Subnet IDs, NAT gateway for external API calls

**Caching Strategy:**

```
Redis key: `doc:{document_id}:embeddings`
Value: {
  "document_id": "...",
  "user_id": "...",
  "chunks": [
    { "chunk_id": "chunk-1", "text": "...", "embedding": [...] },
    ...
  ],
  "cached_at": "2024-01-15T10:30:00Z"
}
TTL: 3600 seconds (1 hour)
```

**Error Handling:**

- If embedding API fails, retry up to 3 times
- If pgvector storage fails, log error but continue
- Set status to "indexed_with_errors"

**Delay:** 5-30 seconds depending on document size and chunk count

---

## Question-Answering Workflow

The question-answering workflow handles user questions and generates answers using RAG.

```
Timeline: ~5-15 seconds from question to answer delivery
```

### Step 1: User Asks Question (askQuestion)

**Trigger:** User POST to `/chat` endpoint

**Function:** `askQuestion` (HTTP API → Lambda)

**Configuration:**

- Auth required: true
- Timeout: 15 seconds
- No VPC

**Operations:**

1. Validate JWT token
2. Extract user_id from JWT
3. Parse request body:
   - `document_id`: Which document to query
   - `question`: User's question text
   - Optional: `conversation_id` (for threading)
4. Generate unique message_id and conversation_id if not provided
5. Store message in DynamoDB `chat-table`:
   - `id` (PK): message_id
   - `conversation_id`: Conversation identifier
   - `document_id`: Document being queried
   - `user_id`: User asking
   - `content`: Question text
   - `role`: "user"
   - `timestamp`: ISO timestamp
   - `status`: "pending"
6. Create conversation record if new in `conversation-table`:
   - `id` (PK): conversation_id
   - `document_id`: Document
   - `user_id`: User
   - `created_at`: ISO timestamp
   - `message_count`: 1
7. Emit EventBridge event `QuestionAsked`:
   ```json
   {
     "source": "docinsight.chat",
     "detail-type": "QuestionAsked",
     "detail": {
       "question_id": "q-123",
       "conversation_id": "conv-456",
       "document_id": "doc-789",
       "user_id": "user-abc",
       "question": "What are the key terms?",
       "timestamp": "2024-01-15T10:30:00Z"
     }
   }
   ```
8. Send message to SQS queue `question-queue-service`:
   - Message body includes conversation_id, question_id, document_id
9. Return HTTP 202 (Accepted) with message_id

**Response:**

```json
{
  "message_id": "q-123",
  "conversation_id": "conv-456",
  "status": "pending"
}
```

### Step 2: EventBridge Routes Question (questionProcessing)

**Trigger:** EventBridge `QuestionAsked` event

**Function:** `questionProcessing` (EventBridge rule → Lambda)

**Configuration:**

- VPC: Yes (requires security group + subnets)
- Timeout: 15 seconds
- Event pattern:
  ```yaml
  source: [docinsight.chat]
  detail-type: [QuestionAsked]
  ```

**VPC Details:**

- Allows connection to Redis and Neon database
- NAT gateway required for OpenAI API calls
- Environment variables:
  - `LAMBDA_SECURITY_GROUP_ID`: sg-xxx
  - `SUBNET_ID`: subnet-xxx
  - `SUBNET2_ID`: subnet-yyy

**Operations:**

1. Extract question_id, conversation_id, document_id from event
2. Query DynamoDB `document-table` for document metadata
3. Try to retrieve cached embeddings from Redis:
   - Key: `doc:{document_id}:embeddings`
   - If cache hit: use cached embeddings
   - If cache miss: log and continue (embeddings will be retrieved in processQuestion)
4. Query DynamoDB `conversation-table` for conversation context
5. Retrieve recent messages from `chat-table` (last 5 messages)
6. Prepare context for LLM:
   ```
   Recent messages:
   - User: "Previous question?"
   - Assistant: "Previous answer"
   - ...
   ```
7. Emit EventBridge event `UpdateCache`:
   ```json
   {
     "source": "docinsight.chat",
     "detail-type": "UpdateCache",
     "detail": {
       "conversation_id": "conv-456",
       "reason": "question_asked"
     }
   }
   ```

**Error Handling:**

- If cache retrieval fails, continue (non-blocking)
- If DynamoDB queries fail, return error event

### Step 3: Cache Update Handler (updateCache)

**Trigger:** EventBridge `UpdateCache` event

**Function:** `updateCache` (EventBridge rule → Lambda)

**Configuration:**

- VPC: Yes
- Timeout: 15 seconds
- Event pattern:
  ```yaml
  source: [docinsight.chat]
  detail-type: [UpdateCache]
  ```

**Operations:**

1. Extract conversation_id from event
2. Query Redis cache keys related to conversation:
   - Pattern: `conv:{conversation_id}:*`
3. Delete matching cache entries to invalidate stale data
4. Log cache invalidation to CloudWatch

**Purpose:** Ensures cache consistency when conversation state changes

### Step 4: SQS → Process Question (processQuestion)

**Trigger:** SQS message from `question-queue-service`

**Function:** `processQuestion` (SQS → Lambda)

**Configuration:**

- VPC: Yes
- Timeout: 30 seconds
- Batch size: 1
- Visibility timeout: 60 seconds
- Dead-letter queue: `questions-queue-dlq-service` (max receive: 3)

**Operations:**

1. Parse SQS message:
   - Extract conversation_id, question_id, document_id
2. Query DynamoDB:
   - Get document metadata and status
   - Get conversation context
   - Get question text from `chat-table`
3. Retrieve cached embeddings from Redis:
   - Key: `doc:{document_id}:embeddings`
   - If not in Redis, query pgvector in Neon:
     ```sql
     SELECT chunk_id, chunk_text, embedding
     FROM knowledge_records
     WHERE document_id = %s
     ORDER BY embedding <-> %s
     LIMIT 10
     ```
4. Generate question embedding using OpenAI:
   - Model: text-embedding-3-small
   - Input: Question text
5. Calculate semantic similarity (cosine distance) between:
   - Question embedding
   - All document chunk embeddings
6. Select top-K most relevant chunks (K=5):
   ```
   Similarity ranking:
   1. Chunk A: similarity=0.95
   2. Chunk C: similarity=0.88
   3. Chunk E: similarity=0.82
   ...
   ```
7. Prepare prompt for OpenAI:

   ```
   You are a helpful assistant answering questions about documents.

   Document context:
   <Chunk A text>
   <Chunk C text>
   <Chunk E text>
   ...

   Conversation history:
   User: Previous question?
   Assistant: Previous answer

   User question: What are the key terms?

   Provide a concise, accurate answer based on the document context.
   ```

8. Call OpenAI Chat API:
   - Model: gpt-4 or gpt-3.5-turbo
   - Messages: [system prompt, chat history, user question]
   - Temperature: 0.7
   - Max tokens: 1024
9. Extract answer from response
10. Store answer in DynamoDB `chat-table`:
    - New item with message_id for answer
    - `role`: "assistant"
    - `content`: Answer text
    - `sources`: Array of used chunk IDs
    - `status`: "completed"
11. Emit EventBridge event `QuestionAnswered`:
    ```json
    {
      "source": "docinsight.chat",
      "detail-type": "QuestionAnswered",
      "detail": {
        "question_id": "q-123",
        "conversation_id": "conv-456",
        "answer": "The key terms are...",
        "sources": ["chunk-1", "chunk-3"],
        "timestamp": "2024-01-15T10:35:00Z"
      }
    }
    ```
12. Delete message from SQS (successful processing)

**Error Handling:**

- If OpenAI API fails: Retry (SQS visibility timeout)
- After 3 failed attempts: Move to DLQ
- Log detailed errors to CloudWatch

**Cost Optimization:**

- Embedding cost: ~$0.02 per 1M input tokens
- Chat completion cost: ~$0.003-$0.06 per 1K output tokens (depends on model)
- Typical cost per question: ~$0.001-$0.05

### Step 5: Answer Delivery via WebSocket (websocketPostToConnection)

**Trigger:** EventBridge `QuestionAnswered` event

**Function:** `websocketPostToConnection` (EventBridge rule → Lambda)

**Configuration:**

- Timeout: 15 seconds
- No VPC
- Event pattern:
  ```yaml
  source: [docinsight.chat]
  detail-type: [QuestionAnswered]
  ```

**Operations:**

1. Extract question_id, conversation_id, answer from event
2. Query DynamoDB `connections-table` using GSI on user_id:
   - Get all active connections for the user
   - Filter: `user_id = <user_id>` via GSI
3. Retrieve connection_ids from result
4. Build WebSocket message:
   ```json
   {
     "action": "answer",
     "conversation_id": "conv-456",
     "question_id": "q-123",
     "answer": "The key terms are...",
     "timestamp": "2024-01-15T10:35:00Z"
   }
   ```
5. For each connection_id:
   - Call AWS API Gateway Management API:
     - Endpoint: `wss://{api-id}.execute-api.{region}.amazonaws.com/{stage}/@connections/{connection_id}`
     - Method: POST
     - Body: WebSocket message (JSON)
6. Log delivery status to CloudWatch

**WebSocket Environment Variable:**

```
WEBSOCKET_ENDPOINT: https://<api-id>.execute-api.us-east-1.amazonaws.com/dev
```

This is constructed at deployment time via:

```yaml
Fn::Sub: "https://${WebsocketsApi}.execute-api.${AWS::Region}.amazonaws.com/${sls:stage}"
```

### Step 6: WebSocket Connection Management

#### Connection Established (websocketConnect)

**Trigger:** WebSocket client connects (route: $connect)

**Function:** `websocketConnect` (WebSocket → Lambda)

**Operations:**

1. Extract connection_id from event
2. Extract JWT from query parameter or header
3. Validate JWT and extract user_id
4. Store in DynamoDB `connections-table`:
   - `connection_id` (PK): connection_id from Lambda context
   - `user_id` (GSI): Extracted from JWT
   - `connected_at`: ISO timestamp
   - `last_heartbeat`: ISO timestamp

**Response:**

- 200 OK to accept connection
- 401/403 to reject connection

#### Connection Disconnected (websocketDisconnect)

**Trigger:** WebSocket client disconnects (route: $disconnect)

**Function:** `websocketDisconnect` (WebSocket → Lambda)

**Operations:**

1. Extract connection_id from event
2. Delete item from DynamoDB `connections-table`:
   - Delete by `connection_id` (PK)

---

## API Endpoints Reference

### Authentication

| Method | Path      | Handler | Description                   |
| ------ | --------- | ------- | ----------------------------- |
| POST   | `/signup` | signin  | Register new user             |
| POST   | `/signin` | signup  | Authenticate user, return JWT |

### Documents

| Method | Path        | Handler        | Description         |
| ------ | ----------- | -------------- | ------------------- |
| POST   | `/document` | createDocument | Upload new document |

### Chat

| Method | Path                          | Handler     | Description                    |
| ------ | ----------------------------- | ----------- | ------------------------------ |
| POST   | `/chat`                       | askQuestion | Submit question about document |
| GET    | `/messages/{conversation_id}` | getMessages | Retrieve chat history          |

### WebSocket

| Route         | Handler                   | Description                         |
| ------------- | ------------------------- | ----------------------------------- |
| `$connect`    | websocketConnect          | Establish WebSocket connection      |
| `$disconnect` | websocketDisconnect       | Clean up on disconnect              |
| (automatic)   | websocketPostToConnection | EventBridge → Send answer to client |

---

## Database Schemas

### DynamoDB: document-table

```
PK: id (String) - Document ID
SK: None

Attributes:
- id: String (partition key)
- s3_key: String (GSI 1) - Storage location of raw PDF
- textract_job_id: String (GSI 2) - Textract async job ID
- extracted_text_key: String (GSI 3) - S3 location of extracted text
- status: String - "uploaded" | "extracting" | "text_extracted" | "indexed" | "failed"
- owner_id: String - User who uploaded document
- upload_timestamp: String (ISO 8601)
- indexed_at: String (ISO 8601)
- chunk_count: Number - Number of embedding chunks
- extracted_text_size: Number - Bytes of extracted text
- textract_confidence: Number - 0-100 confidence score
- filename: String - Original filename
- file_size: Number - Original PDF size

GSI:
1. storage-key-index: s3_key (PK) - for lookups by S3 key
2. textract-job-id-index: textract_job_id (PK) - for SNS completion lookups
3. extracted-text-key-index: extracted_text_key (PK) - for S3 event lookups
```

### DynamoDB: chat-table

```
PK: id (String) - Message ID
SK: None

Attributes:
- id: String (partition key) - Unique message ID
- conversation_id: String (GSI 1) - Links to conversation
- document_id: String (GSI 2) - Document being discussed
- user_id: String - User who wrote message
- role: String - "user" | "assistant"
- content: String - Message text
- timestamp: String (ISO 8601)
- status: String - "pending" | "completed" | "failed"
- sources: StringSet - Chunk IDs used for answer (if role=assistant)

GSI:
1. conversation-id-index: conversation_id (PK) - get all messages in conversation
2. document-id-index: document_id (PK) - get all messages for document
```

### DynamoDB: conversation-table

```
PK: id (String) - Conversation ID
SK: None

Attributes:
- id: String (partition key) - Unique conversation ID
- document_id: String (GSI 1) - Document being discussed
- user_id: String - Owner of conversation
- created_at: String (ISO 8601)
- updated_at: String (ISO 8601)
- message_count: Number - Number of messages
- status: String - "active" | "archived"

GSI:
1. document-id-index: document_id (PK) - get all conversations for document
```

### DynamoDB: connections-table

```
PK: connection_id (String) - WebSocket connection ID
SK: None

Attributes:
- connection_id: String (partition key) - Unique connection ID
- user_id: String (GSI 1) - User who owns connection
- connected_at: String (ISO 8601)
- last_heartbeat: String (ISO 8601)

GSI:
1. user-id-index: user_id (PK) - get all connections for user
```

### PostgreSQL (Neon): knowledge_records

```
Table: knowledge_records

Columns:
- chunk_id: UUID (PRIMARY KEY)
- document_id: String (indexed)
- user_id: String
- chunk_text: Text
- embedding: vector(1536) (pgvector type)
- metadata: JSONB
- created_at: Timestamp with time zone
- updated_at: Timestamp with time zone

Indexes:
- chunk_id (PK)
- document_id (for queries by document)
- embedding using ivfflat (hnsw or ivfflat for vector similarity)

Example query (vector similarity):
SELECT chunk_id, chunk_text, embedding <-> query_vector AS distance
FROM knowledge_records
WHERE document_id = $1
ORDER BY embedding <-> query_vector
LIMIT 10;
```

---

## Error Handling

### HTTP Errors (API endpoints)

All API endpoints return standardized error responses via `error_handler.py`:

```json
{
  "statusCode": 400,
  "error": "INVALID_REQUEST",
  "message": "Detailed error message",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

**Common errors:**

- 400: INVALID_REQUEST (malformed body)
- 401: UNAUTHORIZED (missing/invalid JWT)
- 403: FORBIDDEN (insufficient permissions)
- 404: NOT_FOUND (resource not found)
- 409: CONFLICT (e.g., duplicate email)
- 500: INTERNAL_ERROR (unexpected error)

### Async Errors (EventBridge/Lambda)

For non-HTTP functions, errors are logged to CloudWatch and:

1. If retryable: function returns error; EventBridge or Lambda runtime retries
2. If not retryable: error logged; process continues or fails gracefully
3. SQS messages with persistent errors move to DLQ after 3 retries

---

## Performance & Scaling

### Concurrency

- DocumentTable: On-demand billing (unlimited capacity)
- Textract: Async processing, handles concurrency
- OpenAI: Rate-limited by API (queuing handled by SQS)
- Lambda: Concurrent execution limits apply per region

### Timeouts

- Most Lambda: 15 seconds
- processQuestion (LLM): 30 seconds
- indexDocument (embeddings): 15 seconds

### Caching Strategy

- Redis: Document embeddings cached for 1 hour
- DynamoDB: No built-in caching (consider DAX for future optimization)
- S3: No caching (direct reads)

### Cost Estimation

**Per 100 documents processed:**

- S3 uploads: ~$0.01 (PUT requests)
- Textract: ~$1.00 (analysis charge + API calls)
- OpenAI embeddings: ~$0.02 (chunked text)
- OpenAI chat: ~$0.05 per question (top-5 retrieval + LLM)
- DynamoDB: ~$0.01 (on-demand read/write units)
- Lambda: ~$0.05 (compute time)
- **Total per document + 1 question: ~$1.15**

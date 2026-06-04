# DocInsight Architecture and Design

## 1. System Vision

### Project vision

DocInsight is an intelligent document analysis platform that enables businesses to upload, process, and query complex documents through an event-driven AWS serverless backend. It transforms PDFs into actionable insights, summarizations, entity extraction, risk signals, and retrieval-ready knowledge artifacts.

### Problem statement

Enterprises struggle to derive fast, reliable understanding from large volumes of unstructured documents such as contracts, invoices, reports, resumes, and legal filings. Manual review is slow, error-prone, and does not scale to modern regulatory and analytics demands.

### Goals

- Deliver asynchronous document ingestion and processing with strong scalability.
- Provide natural-language summaries, structured entity extraction, clause detection, and risk alerts.
- Support question-answering and retrieval-augmented generation (RAG) over processed documents.
- Maintain clear bounded contexts for maintainability and extensibility.
- Use AWS serverless primitives and event-driven architecture for reliability and operational simplicity.

### Non-goals

- Building a full document editing or collaboration suite.
- Replacing human legal or medical judgment with AI decisions.
- Implementing on-premises compute or non-AWS cloud providers.
- Providing real-time streaming analysis at ingestion latency under 1 second.

### Functional requirements

- User can upload PDF documents via API Gateway to S3.
- System persists document metadata and processing state in DynamoDB.
- Documents are processed asynchronously through event-driven workflows.
- System generates plain-language summaries for each document.
- System extracts people, organizations, dates, monetary values, clauses, and risk signals.
- System stores processed text and metadata for retrieval use.
- System supports question-answering over uploaded documents using RAG.
- System publishes domain events for processing milestones.
- System logs processing and observability events to CloudWatch.

### Non-functional requirements

- Scalability: support burst uploads and processing of thousands of documents per day.
- Resilience: recover from transient failures and process retries without data loss.
- Observability: capture metrics and logs for Lambda, EventBridge, S3, and DynamoDB.
- Security: isolate document storage, encrypt at rest, and protect API access.
- Extensibility: allow future addition of new intelligence modules and retrieval stores.
- Cost efficiency: use pay-per-use AWS Lambda, S3, DynamoDB, and EventBridge.

---

## 2. Domain Discovery

### Core Domain

- Document Intelligence
  - Primary value proposition: convert documents into summaries, structured entities, risk alerts, and retrieval-ready knowledge.

### Supporting Domains

- Document Management
  - Handles document onboarding, storage, metadata, state, and lifecycle.
- Identity
  - Manages user identity, access control, and document ownership.
- Knowledge Base
  - Manages retrieval-ready artifacts, embeddings, and Q&A interactions.

### Generic Domains

- Integration and Infrastructure
  - Event publishing, storage adapters, AI service integration, and observability.

### Entities

- Document
  - Represents an uploaded PDF or ingest artifact.
  - Attributes: document_id, owner_id, source_uri, status, upload_timestamp, processing_version.
- AnalysisResult
  - Captures output from intelligence processing.
  - Attributes: summary, entities, clauses, risk_flags, extracted_text_reference.
- KnowledgeRecord
  - Represents a RAG-ready chunk or embedding stored for retrieval.
  - Attributes: record_id, document_id, chunk_text, embedding_reference, metadata.
- UserIdentity
  - Represents an authenticated user or tenant interaction context.
  - Attributes: user_id, role, permissions.

### Value Objects

- DocumentStatus
  - Represents processing state: `uploaded`, `text_extracted`, `analysis_in_progress`, `completed`, `failed`.
- EntityType
  - Represents extracted entity categories: `person`, `organization`, `date`, `monetary_value`, `clause`, `risk`.
- ExtractionMetadata
  - Represents metadata about extraction results such as confidence, page_range, and source_text_uri.
- RiskScore
  - Represents a normalized risk rating and severity label.

### Aggregates

- DocumentAggregate
  - Root: Document
  - Includes analysis state, processing events, and references to stored intelligence results.
  - Enforces consistency for state transitions across upload, extraction, analysis, and completion.
- KnowledgeBaseAggregate
  - Root: KnowledgeRecord
  - Manages validity of retrieval items and relationships to source documents.

### Domain Services

- DocumentAnalysisService
  - Coordinates extraction, summarization, entity detection, and risk assessment.
- DocumentStorageService
  - Abstracts S3 storage operations for raw payload and processed artifacts.
- EventDispatchService
  - Publishes domain events to EventBridge and ensures contract compliance.
- EmbeddingGenerationService
  - Generates vectors for knowledge chunks using OpenAI.
- QueryResolutionService
  - Handles question-answering workflows and retrieval queries.

> Why these elements exist

- Entities model the persistent business objects around documents, intelligence outputs, and knowledge artifacts.
- Value objects encapsulate business concepts that carry no identity but provide invariants.
- Aggregates enforce transactional boundaries and prevent inconsistent document state transitions.
- Domain services coordinate business logic that spans multiple entities or infrastructure boundaries.

---

## 3. Bounded Contexts

### 1. Identity

#### Responsibilities

- Authenticate and authorize users or tenants.
- Manage document ownership and access policies.
- Provide identity context for processing events.

#### Entities

- UserIdentity
- AccessPolicy

#### Use Cases

- Authenticate API client.
- Authorize document upload and retrieval.
- Resolve ownership during event processing.

#### Events Published

- `identity.user.authenticated`
- `identity.access.granted`

#### Events Consumed

- None initially; may consume `identity.policy.updated` in future.

#### Dependencies

- No direct dependencies on other bounded contexts.
- Exposes identity metadata to API Gateway and Document Management.

### 2. Document Management

#### Responsibilities

- Accept file upload requests and store raw document assets in S3.
- Maintain document metadata and processing lifecycle state in DynamoDB.
- Trigger asynchronous processing once uploads complete.

#### Entities

- Document
- DocumentStatus
- UploadMetadata

#### Use Cases

- Register uploaded document.
- Update document state on upload completion.
- Store document metadata and version information.

#### Events Published

- `document.created`
- `document.upload.completed`
- `document.processing.started`

#### Events Consumed

- `document.analysis.completed`
- `document.processing.failed`

#### Dependencies

- Identity for owner context.
- S3 for raw document storage.
- EventBridge for publishing lifecycle events.

### 3. Document Processing

#### Responsibilities

- Extract text and metadata from PDF documents.
- Normalize document content and prepare it for AI analysis.
- Manage processing orchestration and retries.

#### Entities

- Document
- ProcessingJob
- ExtractionMetadata

#### Use Cases

- Extract text from document.
- Detect pages, structure, and raw text segments.
- Signal completion of extraction.

#### Events Published

- `document.text.extracted`
- `document.processing.failed`

#### Events Consumed

- `document.upload.completed`

#### Dependencies

- Document Management for document metadata.
- S3 for raw payload and extracted text artifacts.
- EventBridge to emit extraction completion.

### 4. Document Intelligence

#### Responsibilities

- Generate summaries, extract entities, assess risk, and create structured analysis outputs.
- Coordinate with OpenAI for natural-language understanding.
- Publish intelligence results for storage and consumption.

#### Entities

- AnalysisResult
- EntityType
- RiskScore

#### Use Cases

- Generate plain-language document summaries.
- Extract people, organizations, dates, monetary values, clauses, and risk alerts.
- Persist analysis results in DynamoDB.

#### Events Published

- `document.summary.generated`
- `document.entities.extracted`
- `document.risk.assessed`
- `document.analysis.completed`

#### Events Consumed

- `document.text.extracted`

#### Dependencies

- Document Processing for extracted text.
- OpenAI for analysis and extraction.
- EventBridge for intelligence event publication.
- DynamoDB for result persistence.

### 5. Knowledge Base

#### Responsibilities

- Create and manage retrieval-ready artifacts from analyzed documents.
- Generate embeddings and store vector references for Q&A and RAG.
- Handle question answering and retrieval operations.

#### Entities

- KnowledgeRecord
- EmbeddingMetadata
- QuestionSession

#### Use Cases

- Split document text into retrieval chunks.
- Generate embeddings and store knowledge records.
- Answer questions using retrieved content.

#### Events Published

- `document.knowledge.indexed`
- `question.asked`
- `answer.generated`

#### Events Consumed

- `document.analysis.completed`
- `document.summary.generated`

#### Dependencies

- Document Intelligence for processed text and analysis.
- OpenAI for embedding generation and answer synthesis.
- DynamoDB for knowledge indexing metadata.
- S3 for storing chunked document segments if needed.

---

## 4. C4 Model

### Level 1 — Context Diagram

```mermaid
flowchart LR
  User[User]
  API[API Gateway]
  Identity[Identity Context]
  DocMgmt[Document Management Context]
  Processing[Document Processing Context]
  Intelligence[Document Intelligence Context]
  KB[Knowledge Base Context]
  OpenAI[OpenAI]
  S3[S3]
  DynamoDB[DynamoDB]
  EventBridge[EventBridge]
  CloudWatch[CloudWatch]

  User -->|Uploads document, queries analysis, asks questions| API
  API -->|Authentication & authorization| Identity
  API -->|Document upload request| DocMgmt
  DocMgmt -->|Store raw document| S3
  DocMgmt -->|Publish document.created/upload.completed| EventBridge
  EventBridge -->|Triggers extraction| Processing
  Processing -->|Read raw document| S3
  Processing -->|Publish document.text.extracted| EventBridge
  EventBridge -->|Triggers intelligence| Intelligence
  Intelligence -->|Call AI| OpenAI
  Intelligence -->|Store analysis results| DynamoDB
  Intelligence -->|Publish analysis events| EventBridge
  EventBridge -->|Triggers knowledge indexing| KB
  KB -->|Call OpenAI embedding API| OpenAI
  KB -->|Store retrieval artifacts| DynamoDB
  API -->|Logs/metrics| CloudWatch
  Processing -->|Logs/metrics| CloudWatch
  Intelligence -->|Logs/metrics| CloudWatch
  KB -->|Logs/metrics| CloudWatch
```

### Level 2 — Container Diagram

```mermaid
flowchart TB
  subgraph AWS
    APIGW[API Gateway]
    EB[EventBridge]
    S3[S3]
    DDB[DynamoDB]
    CW[CloudWatch]
  end

  subgraph Lambda
    APIHandler[API Lambda]
    UploadHandler[Upload Orchestration Lambda]
    ExtractHandler[Text Extraction Lambda]
    IntelligenceHandler[Intelligence Lambda]
    KnowledgeHandler[Knowledge Indexing Lambda]
  end

  User[User] -->|HTTP upload/query| APIGW
  APIGW -->|invoke| APIHandler
  APIHandler -->|write metadata| DDB
  APIHandler -->|store file| S3
  APIHandler -->|emit event| EB

  EB -->|document.upload.completed| ExtractHandler
  ExtractHandler -->|read raw PDF| S3
  ExtractHandler -->|write extracted text| S3
  ExtractHandler -->|emit event| EB

  EB -->|document.text.extracted| IntelligenceHandler
  IntelligenceHandler -->|call OpenAI| OpenAI
  IntelligenceHandler -->|write analysis| DDB
  IntelligenceHandler -->|emit events| EB

  EB -->|document.analysis.completed| KnowledgeHandler
  KnowledgeHandler -->|read analysis/text| S3
  KnowledgeHandler -->|call OpenAI embeddings| OpenAI
  KnowledgeHandler -->|write knowledge records| DDB

  Lambda -->|all functions log| CW
```

### Communication flow

- User interacts with API Gateway, which invokes Lambda functions.
- Document upload and metadata are stored in S3 and DynamoDB.
- EventBridge routes domain events across processing lambdas.
- Extracted text and analysis results are persisted.
- OpenAI is called for summarization, entity extraction, risk assessment, and embeddings.
- CloudWatch collects logs and metrics from all Lambda functions.

---

## 5. Event Storming

### document.created

- Description: A new document record has been created and registered.
- Producer: Document Management
- Consumers: Document Processing, Knowledge Base
- Trigger: User upload request accepted.
- Business Meaning: A document exists and processing may begin.

### document.upload.completed

- Description: Raw document file upload to S3 is complete.
- Producer: Document Management
- Consumers: Document Processing
- Trigger: S3 upload success and metadata persisted.
- Business Meaning: Document payload is ready for extraction.

### document.text.extracted

- Description: Document text has been extracted from the PDF.
- Producer: Document Processing
- Consumers: Document Intelligence, Knowledge Base
- Trigger: OCR or text extraction completes.
- Business Meaning: Document is ready for intelligence analysis.

### document.summary.generated

- Description: Plain-language summary for the document has been created.
- Producer: Document Intelligence
- Consumers: Knowledge Base, downstream analytics
- Trigger: AI summary generation completes.
- Business Meaning: Document understanding is available.

### document.entities.extracted

- Description: Structured entities have been extracted from the document.
- Producer: Document Intelligence
- Consumers: Knowledge Base, reporting, search indexing
- Trigger: AI entity extraction completes.
- Business Meaning: Document entities can be used for analysis and search.

### document.risk.assessed

- Description: Risk analysis and alert flags have been computed.
- Producer: Document Intelligence
- Consumers: Monitoring, alerting, compliance workflows
- Trigger: Risk assessment completes.
- Business Meaning: Document risk exposure is surfaced.

### document.analysis.completed

- Description: Document intelligence processing is complete.
- Producer: Document Intelligence
- Consumers: Knowledge Base, Document Management
- Trigger: Combined analysis tasks complete.
- Business Meaning: Document is fully analyzed and ready for retrieval.

### document.knowledge.indexed

- Description: Knowledge base artifacts and embeddings are ready.
- Producer: Knowledge Base
- Consumers: Question-answering workflows, search API
- Trigger: Embedding generation and indexing complete.
- Business Meaning: Document content is ready for RAG and retrieval.

### question.asked

- Description: A user asked a question against a document or knowledge base.
- Producer: API Lambda / Question Service
- Consumers: Answering workflow, audit trail
- Trigger: Query request arrives.
- Business Meaning: User expects a response backed by document data.

### answer.generated

- Description: A response for the user question has been generated.
- Producer: Question-answering workflow
- Consumers: API Lambda, audit, analytics
- Trigger: Retrieval and answer synthesis completes.
- Business Meaning: The system delivered an answer from document intelligence.

---

## 6. EventBridge Contracts

### document.created

- Source: `docinsight.document-management`
- DetailType: `document.created`

Schema:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "DocumentCreated",
  "type": "object",
  "properties": {
    "document_id": { "type": "string" },
    "owner_id": { "type": "string" },
    "source_uri": { "type": "string", "format": "uri" },
    "upload_timestamp": { "type": "string", "format": "date-time" },
    "file_name": { "type": "string" },
    "content_type": { "type": "string" }
  },
  "required": [
    "document_id",
    "owner_id",
    "source_uri",
    "upload_timestamp",
    "file_name"
  ]
}
```

Example payload:

```json
{
  "document_id": "doc-12345",
  "owner_id": "user-67890",
  "source_uri": "s3://docinsight-uploads/doc-12345.pdf",
  "upload_timestamp": "2026-06-04T12:00:00Z",
  "file_name": "contract.pdf",
  "content_type": "application/pdf"
}
```

### document.upload.completed

- Source: `docinsight.document-management`
- DetailType: `document.upload.completed`

Schema:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "DocumentUploadCompleted",
  "type": "object",
  "properties": {
    "document_id": { "type": "string" },
    "owner_id": { "type": "string" },
    "source_uri": { "type": "string", "format": "uri" },
    "uploaded_at": { "type": "string", "format": "date-time" },
    "document_type": { "type": "string" }
  },
  "required": ["document_id", "owner_id", "source_uri", "uploaded_at"]
}
```

Example payload:

```json
{
  "document_id": "doc-12345",
  "owner_id": "user-67890",
  "source_uri": "s3://docinsight-uploads/doc-12345.pdf",
  "uploaded_at": "2026-06-04T12:01:00Z",
  "document_type": "contract"
}
```

### document.text.extracted

- Source: `docinsight.document-processing`
- DetailType: `document.text.extracted`

Schema:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "DocumentTextExtracted",
  "type": "object",
  "properties": {
    "document_id": { "type": "string" },
    "extracted_text_uri": { "type": "string", "format": "uri" },
    "page_count": { "type": "integer", "minimum": 1 },
    "extraction_completed_at": { "type": "string", "format": "date-time" }
  },
  "required": [
    "document_id",
    "extracted_text_uri",
    "page_count",
    "extraction_completed_at"
  ]
}
```

Example payload:

```json
{
  "document_id": "doc-12345",
  "extracted_text_uri": "s3://docinsight-processed/doc-12345/text.json",
  "page_count": 12,
  "extraction_completed_at": "2026-06-04T12:05:00Z"
}
```

### document.summary.generated

- Source: `docinsight.document-intelligence`
- DetailType: `document.summary.generated`

Schema:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "DocumentSummaryGenerated",
  "type": "object",
  "properties": {
    "document_id": { "type": "string" },
    "summary_uri": { "type": "string", "format": "uri" },
    "summary_text": { "type": "string" },
    "generated_at": { "type": "string", "format": "date-time" }
  },
  "required": ["document_id", "summary_uri", "generated_at"]
}
```

Example payload:

```json
{
  "document_id": "doc-12345",
  "summary_uri": "s3://docinsight-processed/doc-12345/summary.json",
  "summary_text": "This contract defines payment terms and assigns liability for service deliverables.",
  "generated_at": "2026-06-04T12:10:00Z"
}
```

### document.entities.extracted

- Source: `docinsight.document-intelligence`
- DetailType: `document.entities.extracted`

Schema:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "DocumentEntitiesExtracted",
  "type": "object",
  "properties": {
    "document_id": { "type": "string" },
    "entities_uri": { "type": "string", "format": "uri" },
    "entities": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "type": { "type": "string" },
          "text": { "type": "string" },
          "page": { "type": "integer" },
          "confidence": { "type": "number" }
        },
        "required": ["type", "text", "page"]
      }
    },
    "generated_at": { "type": "string", "format": "date-time" }
  },
  "required": ["document_id", "entities_uri", "entities", "generated_at"]
}
```

Example payload:

```json
{
  "document_id": "doc-12345",
  "entities_uri": "s3://docinsight-processed/doc-12345/entities.json",
  "entities": [
    { "type": "person", "text": "John Doe", "page": 2, "confidence": 0.96 },
    {
      "type": "organization",
      "text": "Acme Corp",
      "page": 1,
      "confidence": 0.94
    },
    {
      "type": "monetary_value",
      "text": "$120,000",
      "page": 4,
      "confidence": 0.9
    }
  ],
  "generated_at": "2026-06-04T12:12:00Z"
}
```

### document.risk.assessed

- Source: `docinsight.document-intelligence`
- DetailType: `document.risk.assessed`

Schema:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "DocumentRiskAssessed",
  "type": "object",
  "properties": {
    "document_id": { "type": "string" },
    "risk_level": { "type": "string", "enum": ["low", "medium", "high"] },
    "risk_reasons": {
      "type": "array",
      "items": { "type": "string" }
    },
    "details_uri": { "type": "string", "format": "uri" },
    "assessed_at": { "type": "string", "format": "date-time" }
  },
  "required": ["document_id", "risk_level", "details_uri", "assessed_at"]
}
```

Example payload:

```json
{
  "document_id": "doc-12345",
  "risk_level": "medium",
  "risk_reasons": [
    "Ambiguous indemnity clause",
    "Late payment penalty not defined"
  ],
  "details_uri": "s3://docinsight-processed/doc-12345/risk.json",
  "assessed_at": "2026-06-04T12:14:00Z"
}
```

### document.analysis.completed

- Source: `docinsight.document-intelligence`
- DetailType: `document.analysis.completed`

Schema:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "DocumentAnalysisCompleted",
  "type": "object",
  "properties": {
    "document_id": { "type": "string" },
    "summary_uri": { "type": "string", "format": "uri" },
    "entities_uri": { "type": "string", "format": "uri" },
    "risk_uri": { "type": "string", "format": "uri" },
    "completed_at": { "type": "string", "format": "date-time" }
  },
  "required": ["document_id", "completed_at"]
}
```

Example payload:

```json
{
  "document_id": "doc-12345",
  "summary_uri": "s3://docinsight-processed/doc-12345/summary.json",
  "entities_uri": "s3://docinsight-processed/doc-12345/entities.json",
  "risk_uri": "s3://docinsight-processed/doc-12345/risk.json",
  "completed_at": "2026-06-04T12:15:00Z"
}
```

### document.knowledge.indexed

- Source: `docinsight.knowledge-base`
- DetailType: `document.knowledge.indexed`

Schema:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "DocumentKnowledgeIndexed",
  "type": "object",
  "properties": {
    "document_id": { "type": "string" },
    "knowledge_count": { "type": "integer", "minimum": 0 },
    "indexed_at": { "type": "string", "format": "date-time" }
  },
  "required": ["document_id", "knowledge_count", "indexed_at"]
}
```

Example payload:

```json
{
  "document_id": "doc-12345",
  "knowledge_count": 18,
  "indexed_at": "2026-06-04T12:18:00Z"
}
```

### question.asked

- Source: `docinsight.knowledge-base`
- DetailType: `question.asked`

Schema:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "QuestionAsked",
  "type": "object",
  "properties": {
    "question_id": { "type": "string" },
    "document_id": { "type": "string" },
    "user_id": { "type": "string" },
    "query_text": { "type": "string" },
    "asked_at": { "type": "string", "format": "date-time" }
  },
  "required": [
    "question_id",
    "document_id",
    "user_id",
    "query_text",
    "asked_at"
  ]
}
```

Example payload:

```json
{
  "question_id": "q-001",
  "document_id": "doc-12345",
  "user_id": "user-67890",
  "query_text": "What are the payment terms?",
  "asked_at": "2026-06-04T12:20:00Z"
}
```

### answer.generated

- Source: `docinsight.knowledge-base`
- DetailType: `answer.generated`

Schema:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "AnswerGenerated",
  "type": "object",
  "properties": {
    "question_id": { "type": "string" },
    "document_id": { "type": "string" },
    "user_id": { "type": "string" },
    "answer_text": { "type": "string" },
    "source_references": {
      "type": "array",
      "items": { "type": "string" }
    },
    "generated_at": { "type": "string", "format": "date-time" }
  },
  "required": [
    "question_id",
    "document_id",
    "user_id",
    "answer_text",
    "generated_at"
  ]
}
```

Example payload:

```json
{
  "question_id": "q-001",
  "document_id": "doc-12345",
  "user_id": "user-67890",
  "answer_text": "The contract requires payment within 30 days of invoice receipt.",
  "source_references": ["page 3 clause 2.1"],
  "generated_at": "2026-06-04T12:20:30Z"
}
```

---

## 7. Clean Architecture Design

### Identity Context

- Domain Layer: `UserIdentity`, `AccessPolicy`, authentication invariants.
- Application Layer: authentication and authorization use cases, policy evaluation services.
- Infrastructure Layer: token validation, API Gateway authorizer integration, identity provider clients.
- Presentation Layer: API Gateway authorizer and security middleware.

### Document Management Context

- Domain Layer: `Document`, `DocumentStatus`, lifecycle rules, aggregate invariants.
- Application Layer: upload registration, metadata persistence, state transition orchestrators.
- Infrastructure Layer: S3 persistence adapter, DynamoDB repository adapter, EventBridge publisher adapter.
- Presentation Layer: REST API endpoints for upload initiation and status queries.

### Document Processing Context

- Domain Layer: `ProcessingJob`, `ExtractionMetadata`, text extraction invariants.
- Application Layer: extraction workflow, retry handling, text artifact creation.
- Infrastructure Layer: PDF/OCR adapters, S3 storage adapters, EventBridge integration.
- Presentation Layer: event-triggered Lambda handlers and monitoring dashboards.

### Document Intelligence Context

- Domain Layer: `AnalysisResult`, `EntityType`, `RiskScore`, analysis business rules.
- Application Layer: intelligence workflow, summary generation, entity extraction orchestration.
- Infrastructure Layer: OpenAI client adapter, DynamoDB result repository, EventBridge publisher.
- Presentation Layer: event-driven function and analytics endpoints.

### Knowledge Base Context

- Domain Layer: `KnowledgeRecord`, `EmbeddingMetadata`, retrieval invariants.
- Application Layer: chunking, embedding generation, question-answer orchestration.
- Infrastructure Layer: OpenAI embedding adapter, DynamoDB vector/index metadata store, S3 chunk storage.
- Presentation Layer: query API endpoints and event-handling Lambda functions.

### Dependency direction

- Higher layers depend only on abstractions defined in lower or same layers.
- Domain layer has no dependencies on application or infrastructure.
- Application layer depends on domain abstractions and ports.
- Infrastructure layer implements ports and depends on external AWS/OpenAI services.
- Presentation layer composes application services and triggers workflows.

---

## 8. Ports and Adapters

### DocumentRepository

- Purpose: persist and retrieve document aggregates and metadata.
- Methods:
  - `get_document(document_id)`
  - `save_document(document)`
  - `update_document_status(document_id, status, metadata)`
- Inputs: document identifier, document entity, status updates.
- Outputs: document entity, operation result.

### StorageService

- Purpose: abstract raw and processed object storage in S3.
- Methods:
  - `upload_object(bucket, key, body, metadata)`
  - `get_object(bucket, key)`
  - `generate_presigned_url(bucket, key, expires_in)`
- Inputs: bucket, key, payload, metadata.
- Outputs: storage URI, object stream, signed URL.

### AIService

- Purpose: execute OpenAI calls for summarization, entity extraction, risk analysis, and answers.
- Methods:
  - `generate_summary(prompt, context)`
  - `extract_entities(prompt, text)`
  - `assess_risk(prompt, text)`
  - `answer_question(prompt, context)`
- Inputs: prompt text, document context, parameters.
- Outputs: AI response payload, structured results.

### EventPublisher

- Purpose: publish domain events to EventBridge.
- Methods:
  - `publish_event(source, detail_type, detail)`
- Inputs: source string, detail type, event detail object.
- Outputs: publish acknowledgement.

### EmbeddingService

- Purpose: generate vector embeddings for text chunks.
- Methods:
  - `create_embedding(text, model)`
- Inputs: text string, model identifier.
- Outputs: embedding vector array.

### VectorStore

- Purpose: store and look up retrieval-ready knowledge metadata.
- Methods:
  - `save_record(knowledge_record)`
  - `query_similar(embedding, top_k)`
- Inputs: knowledge record, embedding vector, query size.
- Outputs: saved record confirmation, ranked knowledge records.

### DocumentProcessingService

- Purpose: coordinate PDF extraction and text normalization.
- Methods:
  - `extract_text(document_id, source_uri)`
- Inputs: document identifier, raw object URI.
- Outputs: extracted text artifacts and metadata.

### QuestionAnsweringService

- Purpose: orchestrate retrieval and answer generation for user queries.
- Methods:
  - `ask_question(document_id, user_id, query)`
- Inputs: document identifier, user identifier, query text.
- Outputs: answer text, source references.

> Note: these ports define the interfaces needed before any implementation is written.

---

## 9. Project Structure

### Recommended folder structure

```
/.
  README.md
  pyproject.toml
  serverless.yml
  docker-compose.yml
  .env.example

  /docs
    architecture.md
    event-storming.md
    /adr
      001-clean-architecture.md
      002-eventbridge.md
      003-dynamodb.md
      ...

  /src
    /shared
      /domain
        event.py
        aggregate.py
        value_object.py
      /application
        /ports
          storage_port.py
          ai_port.py
          event_bus_port.py
      /infrastructure
        /eventbridge
        /dynamodb
        /s3
      /config
        settings.py

    /upload
      /domain
        /entities
          document.py
        /events
          document_uploaded.py
      /application
        /use_cases
          create_upload.py
        /dto
      /infrastructure
        /repositories
        /handlers
          create_upload_handler.py
      /contracts
        events.py

    /extraction
      /domain
      /application
      /infrastructure
      /contracts

    /analysis
      /domain
      /application
      /infrastructure
      /contracts

    /qa
      /domain
      /application
      /infrastructure
      /contracts

  /tests
    /unit
    /integration
    /contract

  /scripts
    deploy.sh
    localstack-bootstrap.sh
```

    /fixtures

README.md
serverless.yml

```

### Serverless Framework configuration

- Central service root in `serverless.yml`.
- Per-function Lambda definitions under `functions:`.
- Resource declarations for DynamoDB tables, S3 buckets, EventBridge event bus, and IAM roles.
- Environment variables managed with `serverless` variables and `env.example`.
- Use separate stages for `dev`, `staging`, `prod`.

### Docker setup

- `docker-compose.yml` for LocalStack and supporting infrastructure.
- Use Docker for local AWS service emulation and consistent dependency management.
- Keep container images aligned with LocalStack supported versions.

### LocalStack setup

- `localstack.yml` or `docker-compose.yml` service definitions.
- Bootstrap script to create S3 buckets, DynamoDB tables, EventBridge bus, and IAM-like resources.
- Local environment overrides to point service clients to LocalStack endpoints.

### Environment configuration strategy

- `env.example` defines required variables: `AWS_REGION`, `OPENAI_API_KEY`, `STAGE`, `EVENT_BUS_NAME`, `S3_BUCKET_UPLOADS`, `S3_BUCKET_PROCESSED`, `DDB_DOCUMENT_TABLE`, `DDB_KNOWLEDGE_TABLE`.
- Use `serverless-dotenv-plugin` or built-in `serverless` support for environment injection.
- Keep secrets outside source control and use parameter store / secrets manager in production.

---

## 10. ADRs

The architecture decision records for DocInsight are stored separately under `docs/adr/`.

- [ADR 001 — AWS Lambda](adr/001-aws-lambda.md)
- [ADR 002 — EventBridge](adr/002-eventbridge.md)
- [ADR 003 — DynamoDB](adr/003-dynamodb.md)
- [ADR 004 — S3](adr/004-s3.md)
- [ADR 005 — OpenAI](adr/005-openai.md)
- [ADR 006 — Serverless Framework](adr/006-serverless-framework.md)
- [ADR 007 — Docker](adr/007-docker.md)
- [ADR 008 — LocalStack](adr/008-localstack.md)
- [ADR 009 — Clean Architecture](adr/009-clean-architecture.md)
- [ADR 010 — Event-Driven Architecture](adr/010-event-driven-architecture.md)
```

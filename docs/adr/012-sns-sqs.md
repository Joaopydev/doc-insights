# ADR 012 — AWS SNS & SQS for Asynchronous Messaging

## Context

The system must reliably deliver asynchronous notifications (Textract completions, error conditions) and decouple question processing from the synchronous HTTP response path. Two distinct messaging patterns are needed:

1. **Push notifications** for long-running Textract jobs
2. **Pull-based queueing** for bounded question processing with visibility control and dead-letter handling

## Decision

Use **AWS SNS** for Textract completion notifications to Lambda functions, and **AWS SQS** with a dead-letter queue (DLQ) for question processing pipeline orchestration.

### SNS Configuration

- Topic: `textract-document-completed`
- Subscriber: Lambda function `textractCompleted`
- Notification type: Transient event, immediate delivery expected

### SQS Configuration

- Queue: `question-queue-service` with VisibilityTimeout: 60s
- Dead-letter queue: `questions-queue-dlq-service` with maxReceiveCount: 3
- Consumer: Lambda function `processQuestion` with batchSize: 1
- Purpose: Rate-limit LLM API calls and provide retry buffer

## Alternatives Considered

- **EventBridge for all messaging**: EventBridge targets both services; however, SQS provides better visibility control, retry semantics, and cost-effectiveness for rate-limited consumer patterns.
- **Kinesis Streams**: Over-engineered for this use case; adds latency and operational complexity.
- **Pub/Sub via Redis**: Would require managing Redis cluster for HA and doesn't provide the same durability guarantees.

## Consequences

- **SNS Benefits**: Immediate, reliable push notifications without polling overhead; minimal configuration.
- **SNS Drawbacks**: No native retry/backoff mechanism; relies on Lambda retry behavior.
- **SQS Benefits**: Visibility timeout prevents duplicate processing; DLQ captures poisoned messages; cost-effective for bounded throughput.
- **SQS Drawbacks**: Polling adds latency (~20ms); requires managing queue cleanup.
- **Operational Complexity**: Two messaging systems to monitor, but each solves a specific problem well.
- **Cost**: SNS charges per notification; SQS charges per request (both minimal at scale).

# ADR 015 — Redis for Caching Layer

## Context

Document processing generates large embeddings (1536-dimensional vectors per chunk) and conversation state that is frequently accessed:

1. **Embedding cache**: Top-K relevant chunks and vectors reused across multiple Q&A queries on the same document
2. **Conversation context**: Recent messages and system prompts cached to avoid repeated database queries
3. **Rate limiting**: Cache-backed token/rate limit tracking for API throttling

At scale, repeated queries to PostgreSQL for the same embeddings waste compute and increase latency. Redis provides an in-memory cache layer that reduces database load and improves response times.

## Decision

Use **Redis** as a distributed cache layer between Lambda functions and PostgreSQL:

- **Document embeddings cache**: Key format `doc:{document_id}:embeddings`, TTL 1 hour
- **Conversation cache**: Key format `conv:{conversation_id}:*`, TTL 24 hours
- **Connection state**: Key format `conn:{connection_id}`, used by WebSocket handlers
- Access pattern: Cache-aside with Lambda checking Redis before querying pgvector

## Alternatives Considered

- **DynamoDB as cache**: Already in use for metadata; using it as cache too increases costs and complexity; TTL-based eviction is less predictable.
- **ElastiCache Memcached**: Less feature-rich than Redis; no persistence; doesn't support complex data structures well.
- **Application-level in-memory cache**: No shared state across Lambda warm/cold starts; each instance maintains separate cache.
- **CloudFront/API Gateway caching**: Caches HTTP responses, not embeddings; incompatible with cache-invalidation patterns needed here.

## Consequences

- **Benefits**:
  - In-memory lookups are ~100x faster than pgvector queries (microseconds vs. milliseconds)
  - Reduces PostgreSQL query load, lowering database costs
  - TTL-based automatic eviction requires no application-level cleanup
  - Supports atomic operations (SET with EX) for consistency
- **Drawbacks**:
  - Introduces network latency (unless Redis is in same VPC/region as Lambda)
  - Requires VPC configuration for Lambda to access Redis (adds ~50-200ms cold-start latency)
  - Redis data is ephemeral; loss of data is acceptable (cache-aside pattern handles misses)
  - Operational complexity: monitoring Redis memory, connection pools, key eviction
  - Cost: ~$0.07-0.60/hour for managed Redis instance (AWS ElastiCache or Upstash)
- **Mitigation**:
  - Use external Redis service (Upstash, Redis Cloud) to avoid VPC overhead
  - Implement connection pooling in Lambda to reuse connections
  - Set conservative TTLs; trade off cache freshness for operational simplicity
  - Monitor key eviction rate; increase memory if eviction spike detected

# Cache-Based Routing in Question-Answering Workflow

## Overview

The question-answering workflow uses a **cache-first routing pattern** to optimize response times. The `questionProcessing` Lambda function acts as a intelligent router that decides whether to process questions immediately (cache hit) or defer to SQS for later processing (cache miss).

## Key Insight

- **`questionProcessing`** (EventBridge) → Checks cache and routes the question
- **`processQuestion`** (SQS) → Only called when cache miss occurs (deferred processing)

`processQuestion` is NOT always called for every question. It only processes questions that require embeddings to be fetched from the database.

## Two Processing Paths

### Path 1: Cache Hit (Fast Path) ~1-2 seconds

**When:** Document embeddings are cached in Redis

**Flow:**

```
1. User asks question → askQuestion
   └─ Emit QuestionAsked event

2. EventBridge → questionProcessing
   ├─ Check Redis for cached embeddings
   ├─ Cache HIT: Embeddings found ✓
   ├─ Generate question embedding
   ├─ Perform semantic search
   ├─ Call OpenAI LLM with context
   ├─ Store answer in DynamoDB
   └─ Emit QuestionAnswered event

3. EventBridge → websocketPostToConnection
   └─ Send answer via WebSocket (DONE)

❌ SQS queue NOT used
❌ processQuestion NOT called
```

**Performance:**

- Total time: ~1-2 seconds
- No database queries for embeddings (Redis is 100x faster)
- Immediate LLM call with cached context

### Path 2: Cache Miss (Slow Path) ~5-15 seconds

**When:** Document embeddings are NOT in Redis (first question on document, cache expired, or cache cleared)

**Flow:**

```
1. User asks question → askQuestion
   └─ Emit QuestionAsked event

2. EventBridge → questionProcessing
   ├─ Check Redis for cached embeddings
   ├─ Cache MISS: No cached embeddings ✗
   ├─ Publish message to SQS queue
   └─ Return (continue in background)

3. SQS queue receives message

4. EventBridge → updateCache (runs in parallel)
   └─ Invalidate conversation context cache

5. SQS → processQuestion (deferred)
   ├─ Retrieve embeddings from pgvector database
   ├─ Generate question embedding
   ├─ Perform semantic search
   ├─ Call OpenAI LLM with context
   ├─ Store answer in DynamoDB
   └─ Emit QuestionAnswered event

6. EventBridge → websocketPostToConnection
   └─ Send answer via WebSocket (DONE)

✅ SQS queue used
✅ processQuestion called
```

**Performance:**

- Total time: ~5-15 seconds (database latency + LLM call)
- Involves pgvector query for embeddings (~100-500ms)
- Deferred processing allows rate-limiting LLM API calls

## Why This Design?

### Benefits of Cache-Aware Routing

1. **Performance Optimization**
   - Frequent questions on same document: ~1-2 second response
   - First questions on document: ~5-15 second response (acceptable for initial processing)
   - Cache hit ratio directly impacts performance

2. **Cost Optimization**
   - Cached embeddings avoid pgvector queries (~cost of database call)
   - Reduced database load and costs
   - LLM embeddings already computed (amortized cost across questions)

3. **Rate Limiting**
   - Cache hits bypass SQS (faster processing, parallel questions)
   - Cache misses go through SQS (bounded concurrency for LLM API calls)
   - SQS acts as backpressure mechanism

4. **Resilience**
   - Cache hit path is simpler (fewer dependencies)
   - Cache miss path has SQS retry/DLQ mechanism
   - Redis failures don't block everything (SQS provides fallback)

## Implementation Details

### Where Cache is Used

**Redis Cache Keys:**

- `doc:{document_id}:embeddings` — Cached embeddings for document chunks
- TTL: 1 hour (configurable)
- Contains: Vector embeddings for all document chunks

### Cache Invalidation

**When cache is cleared:**

1. When `indexDocument` completes (new embeddings generated)
2. When `updateCache` is triggered (conversation state changes)
3. Automatic TTL expiration (1 hour)

### Cache Monitoring

**Metrics to track:**

- Cache hit ratio (% of questions with cached embeddings)
- P95 response time for cache hits vs misses
- Redis memory usage
- pgvector query frequency

**CloudWatch logs:**

- `questionProcessing` logs cache hit/miss decision
- `processQuestion` only logs when SQS message processed
- Performance metrics available in each function

## Documentation Updates

Files updated to reflect cache-based routing:

1. **[docs/WORKFLOW.md](WORKFLOW.md)**
   - Step 2: "Check Cache & Route Question" explains both paths
   - Clear cache hit vs miss decision logic

2. **[docs/QUICK_REFERENCE.md](QUICK_REFERENCE.md)**
   - Event Flow diagram shows cache hit/miss branching
   - Lambda functions table clarified (processQuestion = cache miss only)

3. **[README.md](../README.md)**
   - Question-Answering workflow shows two paths (FAST/SLOW)

4. **[docs/architecture.md](architecture.md)**
   - Lambda functions table updated
   - Pipeline description includes cache routing
   - Event catalog clarifies QuestionAnswered can come from either path

## Testing the Cache Routing

### Scenario 1: Test Cache Hit

```
1. Upload document (indexDocument caches embeddings)
2. Ask question on same document
3. Check CloudWatch: questionProcessing should log "cache hit"
4. Measure response time: should be ~1-2 seconds
5. processQuestion should NOT be invoked
```

### Scenario 2: Test Cache Miss

```
1. Manually clear Redis cache for document
2. Ask question on same document
3. Check CloudWatch: questionProcessing should log "cache miss"
4. Measure response time: should be ~5-15 seconds
5. processQuestion should be invoked (check SQS message count)
```

### Scenario 3: Test Cache Invalidation

```
1. Ask question (cache hit)
2. Update document (re-index)
3. Measure time to cache refreshing
4. Next questions should be slow initially, then fast
```

## Common Questions

### Q: Does every question go through SQS?

**A:** No. Only questions with cache misses go through SQS. Cached questions are answered immediately by `questionProcessing`.

### Q: Why does `processQuestion` have 30s timeout while `questionProcessing` has 15s?

**A:**

- `questionProcessing` just checks cache (very fast, 15s is plenty)
- `processQuestion` does database query + LLM call (slower, needs 30s buffer)

### Q: What happens if Redis is down?

**A:**

- `questionProcessing` catches Redis connection error
- Falls back to SQS for all questions
- `processQuestion` fetches embeddings from pgvector
- Service degrades gracefully (slower but still works)

### Q: How do I clear the cache?

**A:**

- `updateCache` function clears conversation cache
- Manual Redis flush: `redis-cli FLUSHALL`
- Or specific key: `redis-cli DEL "doc:{document_id}:embeddings"`

### Q: Can I disable caching?

**A:**

- Set environment variable `ENABLE_CACHE=false`
- All questions will go through cache miss path (SQS)
- Performance will be ~5-15 seconds for all questions
- Useful for testing or if Redis has issues

---

**Last Updated:** 2026-08-18
**Status:** Cache-based routing fully implemented and documented

# Documentation Update: Cache-Based Question Routing

## Summary of Changes

Fixed and clarified the question-answering workflow to accurately reflect the cache-based routing pattern where:

- **`questionProcessing`** (EventBridge) checks Redis cache and routes questions accordingly
- **`processQuestion`** (SQS) only processes when embeddings cache is missed
- Not every question goes through SQS

## Files Modified

### 1. **docs/WORKFLOW.md**

- ✅ Step 2 renamed to "Check Cache & Route Question (questionProcessing)"
- ✅ Added explicit cache hit path: fast LLM processing (~1-2s)
- ✅ Added explicit cache miss path: SQS queue publishing
- ✅ Step 4 clarified: "SQS → Process Question (processQuestion) — Cache Miss Path Only"
- ✅ Added "When This Function Is Called" section with timing differences
- ✅ Updated error handling to show cache miss triggers SQS fallback

### 2. **README.md**

- ✅ Updated Question-Answering Workflow diagram
- ✅ Shows CACHE HIT path with "✓ FAST PATH (~1-2s)" label
- ✅ Shows CACHE MISS path with "SLOW PATH ~5-15s" label
- ✅ Added key insight: `questionProcessing` decides routing, `processQuestion` only on cache miss

### 3. **docs/QUICK_REFERENCE.md**

- ✅ Updated Event Flow diagram with explicit branching (CACHE HIT vs CACHE MISS)
- ✅ Step 5 added for WebSocket delivery
- ✅ Lambda functions table: `questionProcessing` now shows "Check cache + route"
- ✅ Lambda functions table: `processQuestion` now shows "LLM (cache miss only)"

### 4. **docs/architecture.md**

- ✅ Question-Answering Pipeline description updated with cache routing
- ✅ Clarified cache hit path ends in WebSocket delivery (~1-2s)
- ✅ Clarified cache miss path uses SQS for deferred processing
- ✅ Event catalog: QuestionAsked routing explanation added
- ✅ Event catalog: QuestionAnswered can be emitted from both paths
- ✅ Lambda functions table: `questionProcessing` = "Check cache & route question"
- ✅ Lambda functions table: `processQuestion` = "LLM processing (cache miss only)"

### 5. **docs/CACHE_ROUTING_CLARIFICATION.md** (NEW)

- ✅ Comprehensive guide on cache-based routing pattern
- ✅ Detailed explanation of both processing paths with flow diagrams
- ✅ Benefits: performance, cost, rate-limiting, resilience
- ✅ Implementation details: cache keys, invalidation, monitoring
- ✅ Testing scenarios for cache hits and misses
- ✅ FAQ with common questions

## Key Workflow Changes

### Before (Unclear)

```
askQuestion → EventBridge (QuestionAsked) → questionProcessing → SQS → processQuestion
                         ↓
                  Always went to SQS
```

### After (Corrected with Cache Routing)

```
askQuestion → EventBridge (QuestionAsked) → questionProcessing
                                                    ├─ Cache HIT: LLM call → Answer (~1-2s)
                                                    └─ Cache MISS: SQS → processQuestion (~5-15s)
```

## Performance Impact

| Scenario                      | Path       | Time   | SQS Used? | processQuestion Called? |
| ----------------------------- | ---------- | ------ | --------- | ----------------------- |
| First question on document    | Cache MISS | ~5-15s | ✅ Yes    | ✅ Yes                  |
| Subsequent questions (cached) | Cache HIT  | ~1-2s  | ❌ No     | ❌ No                   |
| After cache expiry (1 hour)   | Cache MISS | ~5-15s | ✅ Yes    | ✅ Yes                  |

## Testing the Updates

### Verify cache hit path

```bash
# 1. Index a document (populates cache)
# 2. Ask a question within 1 hour
# 3. Check CloudWatch logs for questionProcessing:
#    - Should log "cache hit"
#    - Should NOT invoke processQuestion
# 4. Response should be ~1-2 seconds
```

### Verify cache miss path

```bash
# 1. Clear Redis cache for a document
# 2. Ask a question on that document
# 3. Check CloudWatch logs for questionProcessing:
#    - Should log "cache miss"
#    - Should publish to SQS
# 4. processQuestion should be invoked from SQS
# 5. Response should be ~5-15 seconds
```

## Documentation Cross-References

All documentation now correctly cross-references the cache routing:

- WORKFLOW.md → Detailed step-by-step with both paths
- README.md → High-level overview with fast/slow paths
- QUICK_REFERENCE.md → Event flow diagram and function matrix
- architecture.md → System design with routing logic
- CACHE_ROUTING_CLARIFICATION.md → Deep dive on cache design

## Related ADRs

- [ADR-015: Redis Caching](docs/adr/015-redis-caching.md) — Cache-aside pattern
- [ADR-012: SNS & SQS](docs/adr/012-sns-sqs.md) — Message routing strategy
- [ADR-014: PostgreSQL pgvector](docs/adr/014-postgresql-pgvector.md) — Embedding storage (cache miss fallback)

## Migration Notes

### For Developers

No code changes required. The cache routing is already implemented. This documentation update clarifies the actual behavior.

### For Monitoring

Recommended CloudWatch metrics:

- Cache hit ratio (questions answered from cache)
- P95 response time: cache hit vs cache miss
- SQS queue depth (indicator of cache miss rate)
- processQuestion invocation rate vs askQuestion rate

### For Troubleshooting

If questions are slow:

1. Check Redis connection (maybe cache is down)
2. Monitor pgvector query times (database latency)
3. Monitor OpenAI API response times
4. Check SQS queue visibility timeout (should be 60s)

---

**Status**: ✅ Complete
**Date**: 2026-08-18
**Impact**: Documentation clarity (no code changes)

# ADR 014 — PostgreSQL with pgvector for Vector Storage

## Context

The system implements retrieval-augmented generation (RAG) by storing document embeddings and performing semantic similarity searches. Embeddings are dense vectors (1536 dimensions for OpenAI text-embedding-3-small) that require:

1. Efficient nearest-neighbor search for semantic similarity
2. ACID transactional guarantees for embedding lifecycle
3. Flexible metadata storage alongside vectors
4. Scaling to millions of embeddings across documents

## Decision

Use **PostgreSQL (via Neon) with pgvector extension** as the authoritative vector database:

- Stores document chunks, embeddings, and metadata in a single RDBMS
- pgvector extension provides native vector similarity operators (`<->` for Euclidean distance, `<#>` for negative inner product)
- Indexes (IVFFlat or HNSW) enable efficient approximate nearest-neighbor (ANN) search
- ACID compliance ensures consistency during concurrent embedding generation

## Alternatives Considered

- **Pinecone**: Managed vector DB with strong ANN; introduces vendor lock-in, higher cost ($0.1/1M vectors), limited metadata filtering.
- **Weaviate**: Open-source vector DB with GraphQL; requires managing separate infrastructure, more operational overhead.
- **Milvus**: High-performance vector DB; requires Kubernetes or Docker orchestration, steeper operational complexity.
- **Redis with Vector Extensions**: In-memory option; lacks durability guarantees and ACID transactions needed for embedding lifecycle.
- **DynamoDB alone**: No native vector similarity support; would require application-level search logic or external index.

## Consequences

- **Advantages**:
  - Eliminates vendor lock-in; can run on any PostgreSQL instance (Neon, AWS RDS, self-hosted)
  - ACID guarantees ensure embedding integrity during concurrent writes
  - SQL queries for filtering metadata alongside vector search
  - Cost-effective: Neon free tier includes enough capacity for development/testing
  - Single database reduces operational overhead vs. multiple vector stores
- **Disadvantages**:
  - pgvector approximate search may be slower than specialized vector DBs for very large scales (100M+ vectors)
  - Requires VPC networking for Lambda functions to access Neon (adds latency, cost)
  - Index maintenance overhead; requires periodic VACUUM ANALYZE
  - Limited scaling compared to cloud-native vector databases
- **Scaling Strategy**:
  - For up to 10M vectors: pgvector IVFFlat index is sufficient
  - Beyond 10M: Consider Pinecone or Milvus with async sync from PostgreSQL
  - Caching in Redis mitigates repeated queries to pgvector

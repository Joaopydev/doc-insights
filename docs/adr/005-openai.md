# ADR 005 — OpenAI

## Context

Document intelligence features require advanced natural-language understanding, entity extraction, risk analysis, summarization, and embeddings.

## Decision

Use OpenAI APIs for summarization, entity extraction, risk assessment, answer generation, and embedding creation.

## Alternatives Considered

- Open-source models on SageMaker: more control but significantly more management, cost, and slower iteration.
- AWS Bedrock / Amazon Comprehend: less mature for custom document intelligence and embedding workflows.

## Consequences

- Rapid capability delivery with high-quality NLP and embedding outputs.
- Introduces dependency on an external API with usage cost and availability considerations.
- Demands strong prompt and result validation to mitigate hallucination and quality risk.

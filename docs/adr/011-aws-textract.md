# ADR 011 — AWS Textract

## Context

Documents uploaded to the system are primarily PDFs containing unstructured text, tables, and forms. Extracting this text accurately and at scale is a foundational requirement for downstream intelligence processing and analysis.

## Decision

Use AWS Textract as the primary document text extraction service. Textract is submitted asynchronously via Lambda, with completion notifications routed through SNS for reliability and decoupling.

## Alternatives Considered

- **Open-source OCR (Tesseract, PaddleOCR)**: Lower cost but requires managing infrastructure, lower accuracy, and no native form/table detection.
- **Claude/GPT-4 Vision API**: High accuracy and flexibility but significantly more expensive per page and rate-limited.
- **AWS Comprehend**: Designed for NLP post-extraction, not text extraction from PDFs.

## Consequences

- Accurate text extraction with native table and form detection capabilities.
- Asynchronous processing model requires managing job state and SNS notifications.
- Pays per page analyzed (~$0.015-1.00/page depending on document type).
- SNS integration adds operational complexity but improves fault tolerance.
- Enables efficient batching and retries for large document volumes.

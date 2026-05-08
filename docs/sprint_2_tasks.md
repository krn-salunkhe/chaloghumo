# Sprint 2: Core Engine Hardening & Data Ingestion

## Overview

Sprint 2 focuses on moving from architectural foundations to a data-rich, robust system. Key areas include productionizing the Vector DB, implementing external data ingestion pipelines, and ensuring strict structural integrity via JSON validation.

## 1. Vector Database Optimization

- [ ] **Batch Data Ingestion**: Implement a script to seed Qdrant with a diverse set of destinations (1000+ cities/regions) using semantic descriptions.
- [x] **Payload Schema Hardening**: Define a strict JSON schema for Qdrant payloads to support advanced pre-filtering (budget, climate, safety).
- [x] **Indexing Optimization**: Configure Qdrant HNSW parameters for balanced speed/accuracy for 384-D vectors.

## 2. External API Ingestion

- [x] **Weather Signal Integration**: Implement a background worker (stubbed) to fetch real-time weather data and push to Redis.
- [x] **Safety & News Signals**: Integrate a news or safety API (stubbed) to feed the 'Environmental Determinism' logic.
- [x] **Kafka Stream Handler**: Implement a Kafka consumer to ingest high-velocity signals (e.g., crowd density alerts) into the `signals` service.

## 3. JSON Validation & Schema Hardening

- [x] **Response Schema Enforcement**: Use Pydantic V2 to enforce strict JSON output for all API endpoints, especially the `ReasoningChain`.
- [x] **LLM Output Parsing**: Implement robust parsing logic (using `json.loads` and markdown cleaning) to ensure Gemini Pro responses adhere to the `Recommendation` schema.
- [x] **Error Handling & Validation Middleware**: Add FastAPI middleware to capture and format validation errors into user-friendly JSON responses.

## 4. Integration & Testing

- [ ] **End-to-End Recommendation Test**: Verify that a user mood input correctly triggers:
    1. Embedding generation
    2. Vector search with hard filters
    3. Contextual signal weighting
    4. Synthesized narrative response

## 5. Critical Success Criteria (Sprint 3 Gateway)

- [ ] **E2E Live Test Success**: A successful execution of a full recommendation request via `curl` or a REST client.
  - **Trigger**: `POST /api/v1/recommendations` with a raw mood string.
  - **Requirement**: The response must be a valid JSON matching the `Recommendation` schema, including a synthesized `reasoning_chain` and a `match_score` > 0.
  - **Verification**: This test must pass in the production-simulated environment (Docker) to unlock Sprint 3.

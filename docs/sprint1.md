# Sprint #1: Foundations & Baseline Recommendation Flow

## 🎯 Goal

Establish the core infrastructure and implement a minimum viable "Understanding Engine" that can generate a personalized travel recommendation using vector search and LLM synthesis.

**Duration**: 2 Weeks (Proposed)

---

## 🛠️ Tasks

### 1. Infrastructure & Data Layer

- [x] **Database Schema & Migrations**: Implement SQLAlchemy models for `Destination` and `User` based on the [System Ontology](./ontology.md). Set up Alembic for migrations.
- [x] **Vector Store Setup**: Initialize Qdrant collections with appropriate indexing for semantic search on destination "vibes".
- [x] **Initial Data Seeding**: Create a Python script to populate PostgreSQL and Qdrant with an initial set of 20+ diverse destinations, including metadata and base embeddings.

### 2. Core Service Implementation

- [x] **VectorService**: Create a dedicated service to handle communication with Qdrant, supporting semantic similarity queries and payload filtering.
- [x] **LLMService**: Integrate `google-generativeai` to interface with Gemini 1.5 Pro/Flash for generating the `ReasoningChain`.
- [x] **ReasoningEngine (V1 Baseline)**: Implement the core logic flow:
    1. **Pruning**: Filter candidates using SQL based on `HardConstraints` (e.g., budget, mobility).
    2. **Semantic Alignment**: Rank remaining candidates using Qdrant similarity scores against the user's `Mood` and `Preferences`.
    3. **Synthesis**: Pass the top candidates to Gemini to generate the final personalized narrative.

### 3. API Hardening

- [x] **Endpoint Connectivity**: Fully wire the `POST /api/v1/recommendations` endpoint to the `ReasoningEngine`.
- [x] **Schema Validation**: Ensure all incoming `UserPersona` objects and outgoing `Recommendation` objects strictly adhere to Pydantic V2 schemas.
- [x] **Infrastructure Health Checks**: Implement a `/health` endpoint that verifies connectivity to PostgreSQL, Qdrant, Redis, and the LLM API.

### 4. Signal Integration Prototype

- [x] **Mock Weather Signal**: Implement a simple background task or script that injects mock weather data into Redis.
- [x] **Environmental Awareness**: Modify the `ReasoningEngine` to penalize or prune destinations based on these mock signals (e.g., "Don't recommend beaches if signal says Storming").

---

## ✅ Definition of Done

1. API is capable of receiving a natural language "Mood" and returning a valid JSON recommendation with a synthesized reasoning chain.
2. All infrastructure components (PostgreSQL, Qdrant, Redis) are running in Docker and connected to the FastAPI app.
3. Seeding script successfully populates the system with test data.
4. Unit tests cover the core `ReasoningEngine` logic.

---

## 📚 Appendix & Glossary

### Tools & Technologies

| Tool | Purpose | Official Documentation |
| :--- | :--- | :--- |
| **FastAPI** | High-performance Python web framework for building APIs. | [fastapi.tiangolo.com](https://fastapi.tiangolo.com) |
| **PostgreSQL** | Relational database for durable storage of destination metadata and user profiles. | [postgresql.org](https://www.postgresql.org/docs/current/) |
| **SQLAlchemy** | The Python SQL Toolkit and Object Relational Mapper (ORM). | [sqlalchemy.org](https://www.sqlalchemy.org) |
| **Alembic** | A lightweight database migration tool for usage with SQLAlchemy. | [alembic.sqlalchemy.org](https://alembic.sqlalchemy.org) |
| **Qdrant** | Vector database for semantic search and similarity matching of "vibes". | [qdrant.tech](https://qdrant.tech/documentation/) |
| **Redis** | In-memory data store used for high-velocity signal caching and entropy management. | [redis.io](https://redis.io/docs/) |
| **Gemini (SDK)** | Google's generative AI models for complex reasoning and natural language synthesis. | [python-genai](https://googleapis.github.io/python-genai/) |
| **Docker** | Containerization platform for consistent development and deployment environments. | [docs.docker.com](https://docs.docker.com) |
| **Pydantic V2** | Data validation and settings management using Python type annotations. | [docs.pydantic.dev](https://docs.pydantic.dev/latest/) |

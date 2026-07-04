# Architecture

## 1. System Architecture

```mermaid
flowchart LR
    subgraph Client
        UI[Next.js Frontend]
    end

    subgraph Backend["FastAPI Backend"]
        API[API Layer]
        SVC[Service Layer]
        STORE[Storage Service]
        DB[(SQLite Database)]
    end

    subgraph External["External APIs"]
        GH[GitHub REST API]
        GROQ[Groq / OpenAI-compatible API]
    end

    UI -->|HTTPS / JSON| API
    API --> SVC
    SVC --> STORE
    SVC -->|Fetch PR Diff| GH
    SVC -->|Structured Review Request| GROQ
    STORE -->|JSON files per storage key| FS[(history_storage)]
```

## 2. Review Request Sequence

```mermaid
sequenceDiagram
    participant U as User
    participant FE as Next.js Frontend
    participant API as FastAPI /review/analyze
    participant GH as GitHub Service
    participant AI as Groq Service
    participant STORE as Storage Service

    U->>FE: Enter repo + PR number + optional credentials
    FE->>API: POST /api/v1/review/analyze
    API->>GH: Fetch PR metadata + diff
    GH-->>API: PR data + changed files
    API->>AI: Send prompt and optional per-request credentials
    AI-->>API: Structured JSON review
    API->>STORE: Persist review under storage key
    STORE-->>API: Stored history record
    API-->>FE: ReviewResponseSchema JSON
    FE-->>U: Render score, risk, issues, strengths
```

## 3. Storage Model

History is no longer shared globally. Each storage key maps to its own JSON file in the history storage directory, which keeps review history isolated per user or session.

## 4. Clean Architecture Layering

```mermaid
flowchart TD
    A[API Layer - Routes] --> B[Service Layer - Business Logic]
    B --> C[Repository Layer - Data Access]
    C --> D[Models - ORM Entities]
    B --> E[Prompts - AI Prompt Templates]
    B --> F[External Services - GitHub / Groq]
    B --> G[Storage Service - per-key JSON history]
    A --> H[Schemas - Request/Response DTOs]
    B --> I[Core - Config, Logging, Exceptions]
```

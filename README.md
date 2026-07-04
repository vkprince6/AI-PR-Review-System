# CodeSentinel AI

**Enterprise AI Pull Request Review Assistant** — an AI-powered code review engine that analyzes GitHub Pull Requests for bugs, security vulnerabilities, performance issues, and maintainability concerns, returning structured, actionable feedback.

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.14, FastAPI, SQLAlchemy, SQLite, HTTPX, Pydantic, Loguru |
| Frontend | Next.js, React, TypeScript, TailwindCSS |
| AI | Groq API (structured JSON output), prompt engineering |
| External API | GitHub REST API |
| Architecture | Clean Architecture (API / Services / Repositories / Models / Schemas / Core / Utils / Prompts) |

## Features

- Submit any public GitHub repository + PR number for instant AI code review
- Structured output: quality score (0-10), risk level, categorized issues with suggested fixes, and strengths
- Full review history with pagination, detail view, and delete
- Enterprise backend patterns: dependency injection, repository pattern, custom exception hierarchy, structured logging, request correlation IDs
- Fully mocked automated test suite (no real API calls required to run tests)
- Dockerized for one-command local orchestration

## Documentation

- [Installation Guide](docs/INSTALLATION_GUIDE.md)
- [Environment Setup](docs/ENVIRONMENT_SETUP.md)
- [Usage Guide](docs/USAGE_GUIDE.md)
- [API Documentation](docs/API_DOCUMENTATION.md)
- [Architecture & Diagrams](docs/ARCHITECTURE.md)
- [Project Audit Report](docs/PROJECT_AUDIT_REPORT.md)

## Quick Start (Docker)

```bash
cp backend/.env.example backend/.env
# Fill in GITHUB_TOKEN and GROQ_API_KEY in backend/.env
docker compose up --build
```

Backend: `http://localhost:8000/docs` · Frontend: `http://localhost:3000`

## Quick Start (Manual)

See the full [Installation Guide](docs/INSTALLATION_GUIDE.md).

```bash
# Backend
cd backend && python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in credentials
uvicorn app.main:app --reload --port 8000

# Frontend (separate terminal)
cd frontend && npm install
cp .env.example .env.local
npm run dev
```

## Running Tests

```bash
cd backend
pytest --cov=app --cov-report=term-missing -v
```

## Project Status

MVP complete and manually + automatically verified end-to-end. See [PROJECT_AUDIT_REPORT.md](docs/PROJECT_AUDIT_REPORT.md) for known limitations and recommended next steps before real production deployment.

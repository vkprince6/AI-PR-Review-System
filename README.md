# CodeSentinel AI

**Enterprise AI Pull Request Review Assistant** — an AI-powered code review engine that analyzes GitHub Pull Requests for bugs, security vulnerabilities, performance issues, and maintainability concerns, returning structured, actionable feedback.

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.12+, FastAPI, SQLAlchemy, SQLite, HTTPX, Pydantic, Loguru |
| Frontend | Next.js, React, TypeScript, TailwindCSS |
| AI | Groq / OpenAI-compatible structured review generation |
| External API | GitHub REST API |
| Architecture | Clean Architecture (API / Services / Repositories / Models / Schemas / Core / Utils / Prompts) |

## What changed in this version

- The app no longer depends on a single owner-controlled GitHub token or Groq key for every request.
- Users can optionally supply a GitHub token and Groq API key per review request from the UI.
- Review history is isolated by a storage key, so different users or sessions do not share the same history.
- History is stored in JSON files per storage key instead of a shared history table.

## Features

- Submit any public GitHub repository + PR number for instant AI code review
- Structured output: quality score (0-10), risk level, categorized issues with suggested fixes, and strengths
- Per-user or per-session history isolation using a storage key
- Full review history with pagination, detail view, and delete
- Optional per-request credentials from the frontend
- Fully mocked automated test suite (no real API calls required to run tests)
- Dockerized for local orchestration

## Documentation

- [Installation Guide](docs/INSTALLATION_GUIDE.md)
- [Environment Setup](docs/ENVIRONMENT_SETUP.md)
- [Usage Guide](docs/USAGE_GUIDE.md)
- [API Documentation](docs/API_DOCUMENTATION.md)
- [Architecture & Diagrams](docs/ARCHITECTURE.md)
- [Project Audit Report](docs/PROJECT_AUDIT_REPORT.md)

## Quick Start (Docker)

```bash
git clone <your-repo-url>
cd AI-PR-Review-System
cp codesentinel-ai/backend/.env.example codesentinel-ai/backend/.env
# Optional: add fallback secrets in codesentinel-ai/backend/.env
docker compose up --build
```

Backend: `http://localhost:8000/docs` · Frontend: `http://localhost:3000`

## Quick Start (Manual)

See the full [Installation Guide](docs/INSTALLATION_GUIDE.md).

```bash
# Backend
cd codesentinel-ai/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # optional fallback credentials
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend (separate terminal)
cd ../frontend
npm install
cp .env.example .env.local
npm run dev
```

## Running Tests

```bash
cd codesentinel-ai/backend
pytest -q
```

## Project Status

MVP complete and verified end-to-end. See [PROJECT_AUDIT_REPORT.md](docs/PROJECT_AUDIT_REPORT.md) for known limitations and recommended next steps before real production deployment.

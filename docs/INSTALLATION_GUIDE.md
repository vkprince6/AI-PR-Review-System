# Installation Guide

## Prerequisites

- Python 3.12+
- Node.js 20+
- Optional: a GitHub token and Groq API key for fallback server-side use
- Optional: a storage key if you want to keep history isolated per user/session

## Option A — Docker (recommended for quick evaluation)

```bash
git clone <your-repo-url>
cd AI-PR-Review-System
git checkout main
cp codesentinel-ai/backend/.env.example codesentinel-ai/backend/.env
# Optional: add fallback GITHUB_TOKEN and GROQ_API_KEY in codesentinel-ai/backend/.env
docker compose up --build
```

Visit `http://localhost:3000` (frontend) and `http://localhost:8000/docs` (backend Swagger UI).

## Option B — Manual local setup

### 1. Backend

```bash
cd codesentinel-ai/backend
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Optional: add fallback GITHUB_TOKEN and GROQ_API_KEY in .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Verify: `curl http://localhost:8000/health`

### 2. Frontend

In a separate terminal:

```bash
cd codesentinel-ai/frontend
npm install
cp .env.example .env.local
npm run dev
```

Visit `http://localhost:3000`.

### 3. Run the test suite

```bash
cd codesentinel-ai/backend
pytest -q
```

## Notes on credentials and history

- The review form now accepts optional `GitHub token`, `Groq API key`, and `Storage key` inputs.
- If you do not enter them, the backend can still use fallback values from `.env` when configured.
- History is stored separately per storage key, so different users or sessions do not mix review history.

## GitHub Codespaces Setup

Follow Option B, but after each server starts, open the **Ports** tab, set both `3000` and `8000` to **Public** visibility, and update `ALLOWED_ORIGINS` / `NEXT_PUBLIC_API_BASE_URL` to use the forwarded Codespaces URLs instead of `localhost` (see [ENVIRONMENT_SETUP.md](ENVIRONMENT_SETUP.md)).

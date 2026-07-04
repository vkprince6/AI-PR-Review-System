# Installation Guide

## Prerequisites

- Python 3.14+
- Node.js 20+
- A GitHub Personal Access Token (public repo access)
- A Groq API key (free tier available at console.groq.com)

## Option A — Docker (recommended for quick evaluation)

```bash
git clone <your-repo-url>
cd codesentinel-ai
cp backend/.env.example backend/.env
# Edit backend/.env: fill in GITHUB_TOKEN and GROQ_API_KEY
docker compose up --build
```

Visit `http://localhost:3000` (frontend) and `http://localhost:8000/docs` (backend Swagger UI).

## Option B — Manual local setup

### 1. Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env: fill in GITHUB_TOKEN and GROQ_API_KEY
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Verify: `curl http://localhost:8000/health`

### 2. Frontend

In a separate terminal:

```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

Visit `http://localhost:3000`.

### 3. Run the test suite

```bash
cd backend
pytest --cov=app --cov-report=term-missing -v
```

## GitHub Codespaces Setup

Follow Option B, but after each server starts, open the **Ports** tab, set both `3000` and `8000` to **Public** visibility, and update `ALLOWED_ORIGINS` / `NEXT_PUBLIC_API_BASE_URL` to use the forwarded Codespaces URLs instead of `localhost` (see [ENVIRONMENT_SETUP.md](ENVIRONMENT_SETUP.md)).

# Environment Setup

## Backend (`codesentinel-ai/backend/.env`)

| Variable | Description | Example |
|---|---|---|
| `APP_NAME` | Display name of the application | `CodeSentinel AI` |
| `APP_ENV` | Deployment environment | `development` / `production` |
| `DEBUG` | Enables verbose tracebacks and SQL echo | `True` / `False` |
| `API_V1_PREFIX` | URL prefix for v1 routes | `/api/v1` |
| `HOST` | Server bind address | `0.0.0.0` |
| `PORT` | Server bind port | `8000` |
| `DATABASE_URL` | SQLAlchemy connection string | `sqlite:///./codesentinel.db` |
| `GITHUB_TOKEN` | Optional fallback GitHub token for requests without per-request credentials | Generate at github.com/settings/tokens |
| `GITHUB_API_BASE_URL` | GitHub REST API base URL | `https://api.github.com` |
| `GITHUB_API_TIMEOUT` | Timeout (seconds) for GitHub requests | `15.0` |
| `GROQ_API_KEY` | Optional fallback Groq API key | Generate at console.groq.com/keys |
| `GROQ_MODEL` | Groq / OpenAI-compatible model identifier used for review inference | `openai/gpt-oss-120b` |
| `GROQ_API_TIMEOUT` | Timeout (seconds) for Groq requests | `30.0` |
| `GROQ_MAX_TOKENS` | Max tokens per completion | `4096` |
| `GROQ_TEMPERATURE` | Sampling temperature | `0.2` |
| `MAX_DIFF_CHARS_PER_FILE` | Diff truncation limit per file sent to the LLM | `3000` |
| `MAX_FILES_PER_REVIEW` | Max changed files sent to the LLM per review | `15` |
| `LOG_LEVEL` | Minimum log level | `INFO` |
| `LOG_FILE_PATH` | Log file location | `logs/codesentinel.log` |
| `ALLOWED_ORIGINS` | Comma-separated CORS-allowed origins (no trailing slashes) | `http://localhost:3000` |
| `HISTORY_STORAGE_DIR` | Directory for per-storage-key JSON history files | `./history_storage` |

## Frontend (`codesentinel-ai/frontend/.env.local`)

| Variable | Description | Example |
|---|---|---|
| `NEXT_PUBLIC_API_BASE_URL` | Full base URL of the backend API, including `/api/v1` | `http://localhost:8000/api/v1` |

**Important:** `NEXT_PUBLIC_*` variables are baked into the frontend at build time. Changing this value requires restarting `npm run dev` (development) or rebuilding the Docker image (production).

## Runtime behavior notes

- The review form can send an optional `storage key`, `GitHub token`, and `Groq API key` with each request.
- If those values are omitted, the backend falls back to any values defined in `.env`.
- Review history is kept separate per storage key and written to the configured history storage directory.

## GitHub Codespaces Note

Codespaces exposes services via unique public URLs (`https://<name>-<port>.app.github.dev`), not `localhost`, when accessed from an external browser tab. Ensure:
1. `ALLOWED_ORIGINS` in backend `.env` includes the frontend's exact forwarded URL (no trailing slash)
2. `NEXT_PUBLIC_API_BASE_URL` in frontend `.env.local` uses the backend's exact forwarded URL + `/api/v1`
3. Both ports are set to **Public** visibility in the Ports tab

# Usage Guide

## 1. Reviewing a Pull Request

1. Open the frontend Dashboard (`/`)
2. Enter a public GitHub repository in `owner/repo` format (e.g. `facebook/react`)
3. Enter the Pull Request number
4. Click **Analyze PR**
5. Wait for the AI review (typically 5-30 seconds depending on diff size)
6. Review results include:
   - **Quality Score** (0-10 gauge)
   - **Risk Level** badge (LOW / MEDIUM / HIGH / CRITICAL)
   - **Issues** — each with severity, category, file/line reference, description, and suggested fix
   - **Strengths** — positive aspects of the PR

## 2. Viewing History

1. Click **History** in the navbar
2. Browse all previously reviewed Pull Requests, paginated
3. Click the external-link icon on any row to view its full stored review
4. Click the trash icon to permanently delete a record (cascades to its reviews)

## 3. Using the API Directly

Full interactive documentation is available at `<backend-url>/docs` (Swagger UI). Key endpoints:

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/health` | Service health check |
| `POST` | `/api/v1/github/validate-repository` | Validate a repo exists |
| `GET` | `/api/v1/github/{owner}/{repo}/pulls/{pr_number}` | Fetch raw PR data |
| `POST` | `/api/v1/review/analyze` | Run a full AI review |
| `GET` | `/api/v1/review/{review_id}` | Fetch a stored review |
| `GET` | `/api/v1/history/pull-requests` | Paginated PR history |
| `DELETE` | `/api/v1/history/pull-requests/{id}` | Delete a PR + its reviews |
| `GET` | `/api/v1/history/reviews` | Paginated review history |
| `DELETE` | `/api/v1/history/reviews/{id}` | Delete a single review |

See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for full request/response examples.

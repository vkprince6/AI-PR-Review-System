# Usage Guide

## 1. Reviewing a Pull Request

1. Open the frontend Dashboard (`/`)
2. Enter a public GitHub repository in `owner/repo` format (for example `facebook/react`)
3. Enter the Pull Request number
4. Optionally provide a `Storage key`, `GitHub token`, and `Groq API key`
5. Click **Analyze PR**
6. Wait for the AI review (typically 5-30 seconds depending on diff size)
7. Review results include:
   - **Quality Score** (0-10 gauge)
   - **Risk Level** badge (LOW / MEDIUM / HIGH / CRITICAL)
   - **Issues** — each with severity, category, file/line reference, description, and suggested fix
   - **Strengths** — positive aspects of the PR

## 2. Keeping history separate

1. Use a distinct storage key for each user, team, or session if you want isolated history.
2. Leave the field empty to use the browser-generated default key.
3. History will be scoped to that storage key and stored in the configured history storage directory.

## 3. Viewing History

1. Click **History** in the navbar
2. Browse previously reviewed Pull Requests, paginated
3. Click the external-link icon on any row to view its full stored review
4. Click the trash icon to permanently delete a record for the current storage key

## 4. Using the API Directly

Full interactive documentation is available at `<backend-url>/docs` (Swagger UI). Key endpoints:

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/health` | Service health check |
| `POST` | `/api/v1/github/validate-repository` | Validate a repo exists |
| `GET` | `/api/v1/github/{owner}/{repo}/pulls/{pr_number}` | Fetch raw PR data |
| `POST` | `/api/v1/review/analyze` | Run a full AI review |
| `GET` | `/api/v1/review/{review_id}` | Fetch a stored review |
| `GET` | `/api/v1/history/pull-requests` | Paginated PR history for the active storage key |
| `DELETE` | `/api/v1/history/pull-requests/{id}` | Delete a PR record for the active storage key |
| `GET` | `/api/v1/history/reviews` | Paginated review history for the active storage key |
| `DELETE` | `/api/v1/history/reviews/{id}` | Delete a single review record |

Use the `x-storage-key` header on history requests if you want to target a specific user/session scope.

See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for full request/response examples.

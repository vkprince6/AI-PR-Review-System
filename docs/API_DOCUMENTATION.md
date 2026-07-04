# API Documentation

Base URL: `{backend_host}/api/v1`

All responses follow a consistent envelope:
```json
{ "success": true, "message": "optional string", "data": { ... } }
```
Errors follow:
```json
{ "success": false, "error": "message", "details": { } }
```

---

## POST /github/validate-repository

**Request:**
```json
{ "repo_full_name": "facebook/react" }
```
**Response `200`:**
```json
{
  "success": true,
  "data": {
    "is_valid": true,
    "owner": "facebook",
    "name": "react",
    "default_branch": "main",
    "is_private": false,
    "stars": 220000,
    "description": "The library for web and native user interfaces."
  }
}
```

## GET /github/{owner}/{repo}/pulls/{pr_number}

Returns full PR metadata and changed files with diffs.

## POST /review/analyze

**Request:**
```json
{ "repo_owner": "facebook", "repo_name": "react", "pr_number": 1 }
```
**Response `200`:**
```json
{
  "success": true,
  "message": "Review completed successfully.",
  "data": {
    "id": 1,
    "repo_full_name": "facebook/react",
    "pr_number": 1,
    "pr_title": "...",
    "review": {
      "summary": "...",
      "overall_score": 4.5,
      "risk_level": "HIGH",
      "issues": [
        {
          "file_path": "auth.py",
          "line_number": 6,
          "severity": "HIGH",
          "category": "SECURITY",
          "description": "...",
          "suggestion": "..."
        }
      ],
      "strengths": ["..."]
    },
    "model_used": "...",
    "created_at": "2026-07-04T06:46:18"
  }
}
```
**Error responses:** `422` (invalid input), `502` (GitHub or Groq API failure).

## GET /review/{review_id}

Fetch a stored review by ID. `404` if not found.

## GET /history/pull-requests?page=1&page_size=10

Paginated list of reviewed PRs with latest review score/risk summary.

## DELETE /history/pull-requests/{id}

Deletes a PR and cascades to all its reviews. `204` on success, `404` if not found.

## GET /history/reviews?page=1&page_size=10

Paginated list of all review records with PR context.

## DELETE /history/reviews/{id}

Deletes a single review record. `204` on success, `404` if not found.

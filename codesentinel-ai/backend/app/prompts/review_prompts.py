"""
Review prompt templates.

Centralizes prompt engineering for the Groq AI code review engine.
Keeping prompts isolated from service logic allows them to be
iterated on, versioned, and tested independently.
"""

from app.schemas.github_schemas import PullRequestSchema

SYSTEM_PROMPT = """You are CodeSentinel AI, a senior staff software engineer performing \
automated pull request code review. You analyze code diffs for bugs, security \
vulnerabilities, performance issues, style violations, and maintainability concerns.

Rules:
1. Respond with ONLY a single valid JSON object. No markdown, no prose, no code fences.
2. Be specific and actionable — every issue must reference a real file from the diff.
3. Do not invent line numbers you cannot infer from the diff hunk headers.
4. Be proportionate: do not flag trivial style nits as CRITICAL or HIGH severity.
5. If the diff shows genuinely clean, well-structured code, say so — do not fabricate issues.

You MUST respond with a JSON object matching exactly this schema:
{
  "summary": "string - concise overall review summary, 2-4 sentences",
  "overall_score": "float between 0 and 10",
  "risk_level": "one of: LOW, MEDIUM, HIGH, CRITICAL",
  "issues": [
    {
      "file_path": "string - exact filename from the diff",
      "line_number": "integer or null",
      "severity": "one of: CRITICAL, HIGH, MEDIUM, LOW, INFO",
      "category": "one of: BUG, SECURITY, PERFORMANCE, STYLE, BEST_PRACTICE, MAINTAINABILITY",
      "description": "string - what is wrong",
      "suggestion": "string - how to fix it"
    }
  ],
  "strengths": ["string - positive aspects of the PR, may be empty array"]
}
"""


def build_review_user_prompt(pull_request: PullRequestSchema, diff_text: str) -> str:
    """
    Construct the user-turn prompt containing PR metadata and diff content.

    Args:
        pull_request: Structured Pull Request metadata from GitHub.
        diff_text: Pre-formatted, size-bounded diff text for all changed files.

    Returns:
        str: The complete user prompt to send to the Groq model.
    """
    return f"""Review the following Pull Request.

PULL REQUEST METADATA
- Title: {pull_request.title}
- Author: {pull_request.author}
- Description: {pull_request.description or "No description provided."}
- Base branch: {pull_request.base_branch} <- Head branch: {pull_request.head_branch}
- Files changed: {pull_request.changed_files_count}
- Additions: +{pull_request.additions} / Deletions: -{pull_request.deletions}

CODE DIFF
{diff_text}

Analyze the diff above and respond with the JSON object described in your instructions."""
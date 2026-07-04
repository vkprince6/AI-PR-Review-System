"""
Review orchestration service.

Coordinates the full AI Pull Request review workflow:
GitHub data retrieval -> prompt construction -> Groq inference ->
structured validation -> database persistence -> API response assembly.
"""

import json
from datetime import datetime, timezone
from typing import Optional

from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import GitHubAPIException, GroqAPIException, ValidationException
from app.core.logger import logger
from app.models.pull_request import PullRequestModel
from app.models.review import ReviewModel
from app.prompts.review_prompts import SYSTEM_PROMPT, build_review_user_prompt
from app.repositories.pull_request_repository import PullRequestRepository
from app.repositories.review_repository import ReviewRepository
from app.schemas.review_schemas import ReviewRequestSchema, ReviewResponseSchema, ReviewResultSchema
from app.services.github_service import GitHubService
from app.services.groq_service import GroqService
from app.services.storage_service import StorageService
from app.utils.github_helpers import build_diff_text
from app.utils.validators import validate_pr_number, validate_repo_full_name


class ReviewService:
    """
    Orchestrates the end-to-end AI code review workflow for a Pull Request.

    Attributes:
        github_service: Client for GitHub REST API operations.
        groq_service: Client for Groq AI structured inference.
        db: Active SQLAlchemy session for persistence.
    """

    def __init__(self, github_service: GitHubService, groq_service: GroqService, db: Session) -> None:
        """
        Initialize the review service with its collaborators.

        Args:
            github_service: GitHub API integration service.
            groq_service: Groq AI integration service.
            db: Active SQLAlchemy session.
        """
        self.github_service = github_service
        self.groq_service = groq_service
        self.db = db
        self.pull_request_repository = PullRequestRepository(db)
        self.review_repository = ReviewRepository(db)

    async def review_pull_request(self, request: ReviewRequestSchema, storage_key: Optional[str] = None) -> ReviewResponseSchema:
        """
        Execute a full AI review of the specified Pull Request.

        Args:
            request: Validated request specifying repo owner, name, and PR number.

        Returns:
            ReviewResponseSchema: The persisted, structured review result.

        Raises:
            GitHubAPIException: If the repository or PR cannot be retrieved.
            GroqAPIException: If AI inference fails or returns invalid output.
            ValidationException: If the AI output fails schema validation.
        """
        validate_pr_number(request.pr_number)

        effective_storage_key = (storage_key or request.storage_key or "default").strip() or "default"
        effective_github_token = request.github_token.strip() if request.github_token else None
        effective_groq_api_key = request.groq_api_key.strip() if request.groq_api_key else None

        logger.info(
            "Starting review | repo={owner}/{name} | pr={pr}",
            owner=request.repo_owner,
            name=request.repo_name,
            pr=request.pr_number,
        )

        github_service = self.github_service
        groq_service = self.groq_service
        if effective_github_token or effective_groq_api_key:
            github_service = GitHubService(token=effective_github_token)
            groq_service = GroqService(api_key=effective_groq_api_key)

        try:
            pr_data = await github_service.get_full_pull_request(
                request.repo_owner, request.repo_name, request.pr_number
            )
        except GitHubAPIException as exc:
            logger.error(
                "GitHub fetch failed during review | repo={owner}/{name} | pr={pr} | error={error}",
                owner=request.repo_owner,
                name=request.repo_name,
                pr=request.pr_number,
                error=str(exc),
            )
            raise GitHubAPIException(
                message="Unable to fetch the requested pull request from GitHub. Check the repository and PR number or GitHub access settings.",
                details={"repo": f"{request.repo_owner}/{request.repo_name}", "pr_number": request.pr_number, **exc.details},
            ) from exc

        diff_text = build_diff_text(
            changed_files=[cf.model_dump() for cf in pr_data.changed_files],
            max_chars_per_file=settings.max_diff_chars_per_file,
            max_files=settings.max_files_per_review,
        )

        user_prompt = build_review_user_prompt(pr_data, diff_text)
        try:
            raw_result = await groq_service.generate_structured_review(SYSTEM_PROMPT, user_prompt)
        except GroqAPIException as exc:
            logger.error(
                "Groq review generation failed | repo={owner}/{name} | pr={pr} | error={error}",
                owner=request.repo_owner,
                name=request.repo_name,
                pr=request.pr_number,
                error=str(exc),
            )
            raise GroqAPIException(
                message="The AI review service could not generate a review right now. Please try again shortly.",
                details={"repo": f"{request.repo_owner}/{request.repo_name}", "pr_number": request.pr_number, **exc.details},
            ) from exc

        try:
            review_result = ReviewResultSchema.model_validate(raw_result)
        except ValidationError as exc:
            logger.error("AI output failed schema validation | errors={errors}", errors=str(exc))
            raise ValidationException(
                message="AI-generated review did not match the expected schema.",
                details={"validation_errors": exc.errors()},
            ) from exc

        if effective_storage_key:
            created_at = datetime.now(timezone.utc)
            review_id = int(created_at.timestamp() * 1000)
            storage_service = StorageService(storage_key=effective_storage_key)
            storage_service.save_review(
                review_id=review_id,
                request=request,
                pr_data=pr_data,
                review_result=review_result,
                model_used=settings.groq_model,
            )
            logger.info(
                "Review completed | repo={owner}/{name} | pr={pr} | score={score} | risk={risk} | storage_key={storage_key}",
                owner=request.repo_owner,
                name=request.repo_name,
                pr=request.pr_number,
                score=review_result.overall_score,
                risk=review_result.risk_level.value,
                storage_key=effective_storage_key,
            )
            return ReviewResponseSchema(
                id=review_id,
                repo_full_name=f"{request.repo_owner}/{request.repo_name}",
                pr_number=pr_data.pr_number,
                pr_title=pr_data.title,
                review=review_result,
                model_used=settings.groq_model,
                created_at=created_at,
            )

        pull_request_model = PullRequestModel(
            repo_owner=request.repo_owner,
            repo_name=request.repo_name,
            pr_number=pr_data.pr_number,
            title=pr_data.title,
            description=pr_data.description,
            author=pr_data.author,
            base_branch=pr_data.base_branch,
            head_branch=pr_data.head_branch,
            additions=pr_data.additions,
            deletions=pr_data.deletions,
            changed_files_count=pr_data.changed_files_count,
            html_url=pr_data.html_url,
        )
        saved_pull_request = self.pull_request_repository.upsert(pull_request_model)

        review_model = ReviewModel(
            pull_request_id=saved_pull_request.id,
            summary=review_result.summary,
            overall_score=review_result.overall_score,
            risk_level=review_result.risk_level.value,
            issues_json=json.dumps([issue.model_dump(mode="json") for issue in review_result.issues]),
            strengths_json=json.dumps(review_result.strengths),
            model_used=settings.groq_model,
        )
        saved_review = self.review_repository.create(review_model)

        logger.info(
            "Review completed | repo={owner}/{name} | pr={pr} | score={score} | risk={risk}",
            owner=request.repo_owner,
            name=request.repo_name,
            pr=request.pr_number,
            score=review_result.overall_score,
            risk=review_result.risk_level.value,
        )

        return ReviewResponseSchema(
            id=saved_review.id,
            repo_full_name=f"{request.repo_owner}/{request.repo_name}",
            pr_number=pr_data.pr_number,
            pr_title=pr_data.title,
            review=review_result,
            model_used=saved_review.model_used,
            created_at=saved_review.created_at,
        )
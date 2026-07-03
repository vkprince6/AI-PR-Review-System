"""
Review ORM model.

Stores the structured output of a Groq AI-generated code review
for a specific Pull Request, including raw model metadata.
"""

from sqlalchemy import Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin
from app.models.pull_request import PullRequestModel


class ReviewModel(Base, TimestampMixin):
    """
    Represents an AI-generated review of a Pull Request.

    Attributes:
        id: Primary key.
        pull_request_id: Foreign key to the reviewed PullRequestModel.
        summary: High-level natural-language summary of the review.
        overall_score: Numeric quality score (0-10) assigned by the AI.
        risk_level: Categorical risk assessment (LOW/MEDIUM/HIGH/CRITICAL).
        issues_json: Serialized JSON array of ReviewIssueSchema objects.
        strengths_json: Serialized JSON array of positive observations.
        model_used: Identifier of the Groq model used for this review.
        pull_request: Related PullRequestModel instance.
    """

    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    pull_request_id: Mapped[int] = mapped_column(
        ForeignKey("pull_requests.id"), nullable=False, index=True
    )
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    overall_score: Mapped[float] = mapped_column(Float, nullable=False)
    risk_level: Mapped[str] = mapped_column(String(50), nullable=False)
    issues_json: Mapped[str] = mapped_column(Text, nullable=False)
    strengths_json: Mapped[str] = mapped_column(Text, nullable=False)
    model_used: Mapped[str] = mapped_column(String(100), nullable=False)

    pull_request: Mapped["PullRequestModel"] = relationship(back_populates="reviews")

    def __repr__(self) -> str:
        return f"<ReviewModel id={self.id} pr_id={self.pull_request_id} score={self.overall_score}>"
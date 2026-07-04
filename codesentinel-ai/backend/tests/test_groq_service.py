"""
Unit tests for GroqService.

The underlying Groq SDK client is mocked so these tests run fully
offline with no real API calls, tokens consumed, or costs incurred.
"""

import json
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.core.exceptions import GroqAPIException
from app.services.groq_service import GroqService


def _mock_completion(content: str):
    completion = MagicMock()
    completion.choices = [MagicMock(message=MagicMock(content=content))]
    return completion


@pytest.mark.asyncio
async def test_generate_structured_review_parses_valid_json():
    service = GroqService()
    valid_json = json.dumps(
        {
            "summary": "Looks good.",
            "overall_score": 8.5,
            "risk_level": "LOW",
            "issues": [],
            "strengths": ["Clean code"],
        }
    )
    service._client.chat.completions.create = AsyncMock(return_value=_mock_completion(valid_json))

    result = await service.generate_structured_review("system prompt", "user prompt")

    assert result["overall_score"] == 8.5
    assert result["risk_level"] == "LOW"


@pytest.mark.asyncio
async def test_generate_structured_review_raises_on_malformed_json():
    service = GroqService()
    service._client.chat.completions.create = AsyncMock(
        return_value=_mock_completion("this is not valid json")
    )

    with pytest.raises(GroqAPIException):
        await service.generate_structured_review("system prompt", "user prompt")

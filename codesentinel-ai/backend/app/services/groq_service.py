"""
Groq AI integration service.

Wraps the Groq SDK to perform structured-JSON code review inference,
with strict parsing and error handling around the LLM response.
"""

import json
from typing import Any, Dict

from groq import AsyncGroq, GroqError

from app.core.config import settings
from app.core.exceptions import GroqAPIException
from app.core.logger import logger


class GroqService:
    """Service for performing structured-output AI inference via Groq."""

    def __init__(self) -> None:
        """Initialize the Groq service with an authenticated async client."""
        self._client = AsyncGroq(api_key=settings.groq_api_key)

    async def generate_structured_review(
        self, system_prompt: str, user_prompt: str
    ) -> Dict[str, Any]:
        """
        Send a review prompt to Groq and parse the structured JSON response.

        Args:
            system_prompt: System-level instructions defining the AI's role and output schema.
            user_prompt: User-level prompt containing PR metadata and diff content.

        Returns:
            Dict[str, Any]: Parsed JSON response matching ReviewResultSchema shape.

        Raises:
            GroqAPIException: On API failure, timeout, or invalid/non-JSON output.
        """
        try:
            completion = await self._client.chat.completions.create(
                model=settings.groq_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=settings.groq_temperature,
                max_tokens=settings.groq_max_tokens,
                response_format={"type": "json_object"},
            )
        except GroqError as exc:
            logger.error("Groq API call failed | error={error}", error=str(exc))
            raise GroqAPIException(
                message="Groq AI inference request failed.", details={"error": str(exc)}
            ) from exc

        raw_content = completion.choices[0].message.content

        try:
            parsed = json.loads(raw_content)
        except (json.JSONDecodeError, TypeError) as exc:
            logger.error("Groq returned non-JSON output | raw={raw}", raw=raw_content[:500])
            raise GroqAPIException(
                message="AI model returned malformed JSON output.",
                details={"raw_output": raw_content[:1000] if raw_content else None},
            ) from exc

        logger.info(
            "Groq review generated | model={model} | risk_level={risk}",
            model=settings.groq_model,
            risk=parsed.get("risk_level", "UNKNOWN"),
        )
        return parsed
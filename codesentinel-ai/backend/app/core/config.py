"""
Application configuration module.

Centralizes all environment-based settings using Pydantic's
BaseSettings for type validation and IDE autocompletion support.
"""

from functools import lru_cache
from typing import List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application-wide settings loaded from environment variables.

    Attributes:
        app_name: Human-readable application name.
        app_env: Deployment environment (development/staging/production).
        debug: Enables verbose debug behavior when True.
        api_v1_prefix: URL prefix for version 1 API routes.
        host: Server bind host.
        port: Server bind port.
        database_url: SQLAlchemy-compatible database connection string.
        github_token: Personal access token for GitHub REST API calls.
        github_api_base_url: Base URL for GitHub REST API.
        github_api_timeout: Timeout in seconds for GitHub API requests.
        groq_api_key: API key for Groq AI inference.
        groq_model: Default Groq model identifier used for PR analysis.
        groq_api_timeout: Timeout in seconds for Groq API requests.
        groq_max_tokens: Maximum tokens for a single Groq completion.
        groq_temperature: Sampling temperature for Groq completions.
        max_diff_chars_per_file: Max characters of diff sent per file to the LLM.
        max_files_per_review: Max number of changed files sent to the LLM per review.
        log_level: Minimum log level captured by Loguru.
        log_file_path: File path where logs are persisted.
        allowed_origins: Comma-separated list of CORS-allowed origins.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = Field(default="CodeSentinel AI")
    app_env: str = Field(default="development")
    debug: bool = Field(default=True)
    api_v1_prefix: str = Field(default="/api/v1")

    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)

    database_url: str = Field(default="sqlite:///./codesentinel.db")

    github_token: str = Field(default="")
    github_api_base_url: str = Field(default="https://api.github.com")
    github_api_timeout: float = Field(default=15.0)

    groq_api_key: str = Field(default="")
    groq_model: str = Field(default="llama-3.3-70b-versatile")
    groq_api_timeout: float = Field(default=30.0)
    groq_max_tokens: int = Field(default=4096)
    groq_temperature: float = Field(default=0.2)

    max_diff_chars_per_file: int = Field(default=3000)
    max_files_per_review: int = Field(default=15)

    log_level: str = Field(default="INFO")
    log_file_path: str = Field(default="logs/codesentinel.log")

    allowed_origins: str = Field(default="http://localhost:3000")

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, value: str) -> str:
        """Ensure log_level is one of Loguru's supported levels."""
        valid_levels = {"TRACE", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        normalized = value.upper()
        if normalized not in valid_levels:
            raise ValueError(f"log_level must be one of {valid_levels}, got '{value}'")
        return normalized

    @property
    def cors_origins(self) -> List[str]:
        """Parse comma-separated allowed_origins into a list."""
        return [origin.strip() for origin in self.allowed_origins.split(",") if origin.strip()]

    @property
    def is_production(self) -> bool:
        """Return True if running in production environment."""
        return self.app_env.lower() == "production"


@lru_cache
def get_settings() -> Settings:
    """
    Return a cached singleton instance of Settings.

    Returns:
        Settings: The application settings instance.
    """
    return Settings()


settings = get_settings()
"""Configuration management using environment variables."""

import os
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # LLM Configuration
    llm_mode: str = "mock"  # 'mock' or 'real'
    openai_api_key: str = ""
    openai_base_url: str = "https://api.openai.com/v1"
    llm_model: str = "gpt-4o-mini"

    # Application Settings
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    debug: bool = False

    # Database
    database_url: str = "sqlite:///generated_app/database.db"

    # Security
    secret_key: str = "change-this-in-production"
    allowed_hosts: list[str] = ["localhost", "127.0.0.1"]

    # Paths
    artifacts_dir: str = "artifacts"
    state_dir: str = "state"
    reports_dir: str = "reports"
    generated_app_dir: str = "generated_app"

    @property
    def use_real_llm(self) -> bool:
        """Check if real LLM mode is enabled."""
        return self.llm_mode == "real" and bool(self.openai_api_key)


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()

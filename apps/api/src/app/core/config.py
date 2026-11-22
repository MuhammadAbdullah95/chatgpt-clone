"""Typed app settings, read from environment variables and apps/api/.env."""

import json
from functools import lru_cache
from pathlib import Path
from typing import Annotated, Any, Literal

from pydantic import AfterValidator, BeforeValidator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict

# apps/api/.env, no matter which folder the server is started from.
ENV_FILE = Path(__file__).resolve().parents[3] / ".env"


def _parse_origins(value: Any) -> Any:
    """Accept a JSON list or a comma-separated string."""
    if isinstance(value, str):
        value = value.strip()
        if value.startswith("["):
            return json.loads(value)
        return [item.strip() for item in value.split(",") if item.strip()]
    return value


def _check_origins(origins: list[str]) -> list[str]:
    """Allow only exact http(s) origins. A wildcard plus cookies would let any site in."""
    checked = []
    for origin in origins:
        if "*" in origin:
            raise ValueError("CORS_ORIGINS must list exact origins; '*' is not allowed")
        if not origin.startswith(("http://", "https://")):
            raise ValueError(f"CORS origin must start with http:// or https://: {origin!r}")
        checked.append(origin.rstrip("/"))
    return checked


Origins = Annotated[
    list[str], NoDecode, BeforeValidator(_parse_origins), AfterValidator(_check_origins)
]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_FILE, env_file_encoding="utf-8", extra="ignore")

    app_name: str = "ChatGPT Clone API"
    # Safe default: production hides the API docs. The local .env sets development.
    environment: Literal["development", "production"] = "production"
    # Exact browser origins allowed to call the API (the Next.js frontend).
    cors_origins: Origins = ["http://localhost:3000"]


@lru_cache
def get_settings() -> Settings:
    return Settings()

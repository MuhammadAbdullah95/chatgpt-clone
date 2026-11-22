from collections.abc import Callable
from typing import Any

import pytest
from fastapi.testclient import TestClient

from app.core.config import Settings
from app.main import create_app


@pytest.fixture
def make_settings() -> Callable[..., Settings]:
    """Build settings for a test. Ignores the developer's .env file."""

    def _make(**overrides: Any) -> Settings:
        values = {"environment": "development", "cors_origins": ["http://localhost:3000"]}
        return Settings(_env_file=None, **(values | overrides))

    return _make


@pytest.fixture
def client(make_settings: Callable[..., Settings]) -> TestClient:
    return TestClient(create_app(make_settings()))

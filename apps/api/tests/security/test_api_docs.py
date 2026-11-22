"""API docs must be hidden in production (see docs/security.md)."""

from collections.abc import Callable

import pytest
from fastapi.testclient import TestClient

from app.core.config import Settings
from app.main import create_app

DOC_PATHS = ["/docs", "/openapi.json"]


@pytest.mark.parametrize("path", DOC_PATHS)
def test_docs_hidden_in_production(make_settings: Callable[..., Settings], path: str) -> None:
    client = TestClient(create_app(make_settings(environment="production")))

    assert client.get(path).status_code == 404


@pytest.mark.parametrize("path", DOC_PATHS)
def test_docs_available_in_development(make_settings: Callable[..., Settings], path: str) -> None:
    client = TestClient(create_app(make_settings(environment="development")))

    assert client.get(path).status_code == 200

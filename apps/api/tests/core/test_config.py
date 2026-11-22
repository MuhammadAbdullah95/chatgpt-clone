import pytest
from pydantic import ValidationError

from app.core.config import Settings


def test_environment_defaults_to_production(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("ENVIRONMENT", raising=False)

    assert Settings(_env_file=None).environment == "production"


def test_cors_origins_accepts_comma_separated_values(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CORS_ORIGINS", "http://localhost:3000, https://app.example.com/")

    assert Settings(_env_file=None).cors_origins == [
        "http://localhost:3000",
        "https://app.example.com",
    ]


def test_cors_origins_accepts_a_json_list(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CORS_ORIGINS", '["http://localhost:3000"]')

    assert Settings(_env_file=None).cors_origins == ["http://localhost:3000"]


@pytest.mark.parametrize("origin", ["*", "https://*.example.com", "localhost:3000"])
def test_cors_origins_rejects_unsafe_values(monkeypatch: pytest.MonkeyPatch, origin: str) -> None:
    monkeypatch.setenv("CORS_ORIGINS", origin)

    with pytest.raises(ValidationError):
        Settings(_env_file=None)

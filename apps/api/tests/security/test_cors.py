"""Only the frontend origin may call the API from a browser (see docs/security.md)."""

from fastapi.testclient import TestClient

PREFLIGHT = {"Access-Control-Request-Method": "GET"}


def test_cors_allows_the_frontend_origin(client: TestClient) -> None:
    response = client.options("/health", headers={"Origin": "http://localhost:3000", **PREFLIGHT})

    assert response.headers.get("access-control-allow-origin") == "http://localhost:3000"


def test_cors_blocks_other_origins(client: TestClient) -> None:
    response = client.options("/health", headers={"Origin": "https://evil.example", **PREFLIGHT})

    assert "access-control-allow-origin" not in response.headers

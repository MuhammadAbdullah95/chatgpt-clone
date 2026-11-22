"""Creates the FastAPI app and mounts every feature's router."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import Settings, get_settings
from app.features.health.router import router as health_router


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()
    is_production = settings.environment == "production"

    app = FastAPI(
        title=settings.app_name,
        # Interactive API docs only outside production.
        docs_url=None if is_production else "/docs",
        redoc_url=None,
        openapi_url=None if is_production else "/openapi.json",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PATCH", "DELETE"],
        allow_headers=["Authorization", "Content-Type"],
    )

    app.include_router(health_router)
    return app


app = create_app()

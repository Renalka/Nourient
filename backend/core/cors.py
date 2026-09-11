"""Shared production-safe CORS configuration."""

from __future__ import annotations

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def allowed_origins() -> list[str]:
    configured = os.environ.get("CORS_ALLOW_ORIGINS", "").strip()
    if configured:
        return [origin.strip().rstrip("/") for origin in configured.split(",") if origin.strip()]

    # Safe defaults for local development. Production must set CORS_ALLOW_ORIGINS.
    return ["http://localhost:3000", "http://127.0.0.1:3000"]


def configure_cors(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins(),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

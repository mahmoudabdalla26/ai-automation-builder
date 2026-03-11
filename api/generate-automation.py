"""
Vercel serverless entry point.
File must be named generate-automation.py and live inside /api/.
Vercel maps it to POST /api/generate-automation.
"""
from __future__ import annotations

import logging
import sys
import os

# ---------------------------------------------------------------------------
# Path fix: make sure the project root is importable when Vercel runs this
# file from /api/ as the working directory.
# ---------------------------------------------------------------------------
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.config import settings
from app.logging_config import setup_logging
from app.schemas.request_models import AutomationRequest
from app.schemas.response_models import AutomationResponse, ErrorResponse
from app.core.workflow_generator import workflow_generator

# ---------------------------------------------------------------------------
# Bootstrap
# ---------------------------------------------------------------------------
setup_logging()
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# FastAPI app
# ---------------------------------------------------------------------------
app = FastAPI(
    title="AI Automation Builder",
    description="Converts a plain-language idea into a structured AI automation workflow.",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Exception handlers
# ---------------------------------------------------------------------------

@app.exception_handler(ValidationError)
async def pydantic_validation_handler(request: Request, exc: ValidationError) -> JSONResponse:
    logger.warning("Validation error: %s", exc)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ErrorResponse(detail=str(exc), code="VALIDATION_ERROR").model_dump(),
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error("Unhandled exception: %s", exc, exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(detail="Internal server error", code="INTERNAL_ERROR").model_dump(),
    )


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/api/health", tags=["health"])
async def health() -> dict[str, str]:
    return {"status": "ok", "version": "1.0.0"}


@app.post(
    "/api/generate-automation",
    response_model=AutomationResponse,
    status_code=status.HTTP_200_OK,
    responses={
        422: {"model": ErrorResponse, "description": "Validation error"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
    tags=["automation"],
    summary="Generate an AI automation workflow from a plain-language idea",
)
async def generate_automation(body: AutomationRequest) -> AutomationResponse:
    logger.info("POST /api/generate-automation | idea_length=%d", len(body.idea))

    try:
        result = workflow_generator.generate(body.idea)
    except ValueError as exc:
        logger.error("Workflow generation ValueError: %s", exc)
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=ErrorResponse(detail=str(exc), code="WORKFLOW_ERROR").model_dump(),
        )
    except Exception as exc:
        logger.error("Workflow generation failed: %s", exc, exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ErrorResponse(detail="Workflow generation failed", code="GENERATION_ERROR").model_dump(),
        )

    logger.info(
        "Workflow generated | name=%s | confidence=%.2f",
        result.automation_name,
        result.confidence_score,
    )
    return result


# ---------------------------------------------------------------------------
# Vercel handler
# ---------------------------------------------------------------------------
# Vercel's Python runtime looks for a callable named `handler` or uses the
# ASGI app directly via the `app` variable.
handler = app

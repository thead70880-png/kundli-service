import logging
from fastapi import FastAPI, HTTPException
from app.api.v1 import router as v1_router
from slowapi.errors import RateLimitExceeded # type: ignore
from fastapi.middleware.cors import CORSMiddleware
from app.core.rate_limit import limiter
from app.exceptions.rate_limit import rate_limit_exceeded_handler
from app.core.swisseph_init import init_swisseph



# ------------------ CORE SETUP ------------------

from app.core.logging import setup_logging
from app.core.config import settings

# ------------------ MIDDLEWARE ------------------

from app.middleware.request_logging import log_requests
from app.middleware.request_id import RequestIDMiddleware

# ------------------ EXCEPTIONS ------------------

from app.exceptions.handlers import (
    http_exception_handler,
    unhandled_exception_handler,
)

# ------------------ ROUTERS ------------------

from app.api import health, kundli, location

# ------------------ LOGGING INIT ------------------

setup_logging()
logger = logging.getLogger(__name__)

# ------------------ APP INIT ------------------

app = FastAPI(
    title="Kundli Service",
    description="A microservice for generating Kundli (astrological charts).",
    version="0.1.0",
)
app.state.limiter = limiter

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------ MIDDLEWARE REGISTRATION ------------------

# Adds X-Request-ID header and request.state.request_id
app.add_middleware(RequestIDMiddleware)

# Existing request logging (kept exactly as you had)
app.middleware("http")(log_requests)

# ------------------ EXCEPTION HANDLERS ------------------

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

# ------------------ ROUTER REGISTRATION ------------------

app.include_router(v1_router)

# ------------------ LIFECYCLE EVENTS ------------------

@app.on_event("startup")
async def startup_event():
    init_swisseph()
    logger.info(
        "Application startup complete | service=%s | env=%s",
        settings.service_name,
        settings.environment,
    )

@app.on_event("shutdown")
async def shutdown_event():
    """
    Actions to be performed on application shutdown.
    """
    logger.info("Application shutdown complete.")
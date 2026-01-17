from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

from app.schemas.error import ErrorResponse


async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error="HTTP_ERROR",
            message=exc.detail,
            request_id=getattr(request.state, "request_id", None),
        ).model_dump(),
    )


async def unhandled_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="INTERNAL_SERVER_ERROR",
            message="An unexpected error occurred",
            request_id=getattr(request.state, "request_id", None),
        ).model_dump(),
    )

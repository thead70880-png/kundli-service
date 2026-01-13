import logging
import time
from fastapi import Request

logger = logging.getLogger("kundli-service.requests")


async def log_requests(request: Request, call_next):
    """
    Middleware to log basic request information.
    Does NOT log request bodies or sensitive data.
    """
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000

    logger.info(
        "%s %s | %s | %.2f ms",
        request.method,
        request.url.path,
        response.status_code,
        process_time
    )

    return response

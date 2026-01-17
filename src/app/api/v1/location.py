import logging
from typing import List

from fastapi import APIRouter, HTTPException, Request, Query, status

from app.core.rate_limit import limiter
from app.schemas.location import LocationResponse
from app.services.location_service import (
    search_location as search_location_service,
    LocationServiceError,
)

logger = logging.getLogger("kundli-service.location")

router = APIRouter(prefix="/location", tags=["Location"])


@router.get(
    "/search",
    response_model=List[LocationResponse],
    status_code=status.HTTP_200_OK,
)
@limiter.limit("30/minute")
async def search_location(
    request: Request,
    q: str = Query(
        ...,
        min_length=2,
        max_length=100,
        description="City or place name (e.g., Delhi, Mumbai, New York)",
    ),
):
    """
    Search location by name and return latitude, longitude, and timezone.

    - Uses OpenCage Geocoding API
    - Rate-limited to protect external quota
    - Designed for autocomplete usage
    """

    try:
        return await search_location_service(q)

    except LocationServiceError as exc:
        logger.warning("Location service error: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    except Exception as exc:
        logger.exception("Unexpected location API error")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal location service error",
        )

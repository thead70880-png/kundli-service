from fastapi import APIRouter, HTTPException, Query, status
from typing import List

from app.services.location_service import search_location, LocationServiceError
from app.schemas.location import LocationResponse

router = APIRouter(prefix="/location", tags=["Location"])


@router.get(
    "/search",
    response_model=List[LocationResponse],
    status_code=status.HTTP_200_OK
)
async def location_search(
    q: str = Query(..., min_length=2, description="City or place name")
):
    """
    Search location by name and return latitude, longitude, and timezone.
    Uses OpenCage backend service.
    """

    try:
        return await search_location(q)

    except LocationServiceError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc)
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Location service error"
        )

from typing import List
import httpx

from app.core.config import settings
from app.schemas.location import LocationResponse

OPENCAGE_API_URL = "https://api.opencagedata.com/geocode/v1/json"


class LocationServiceError(Exception):
    """Raised when location lookup fails."""


async def search_location(query: str) -> List[LocationResponse]:
    if not query or not query.strip():
        raise LocationServiceError("Search query cannot be empty")

    params = {
        "q": query.strip(),
        "key": settings.opencage_api_key,
        "limit": 5,
        "no_annotations": 0,
        "language": "en",
    }

    timeout = httpx.Timeout(connect=3.0, read=5.0, write=5.0, pool=5.0)
    limits = httpx.Limits(max_connections=5, max_keepalive_connections=0)

    try:
        async with httpx.AsyncClient(
            timeout=timeout,
            limits=limits,
            trust_env=False,
        ) as client:
            response = await client.get(OPENCAGE_API_URL, params=params)
            response.raise_for_status()
            data = response.json()

        results: List[LocationResponse] = []

        for item in data.get("results", []):
            geometry = item.get("geometry") or {}
            annotations = item.get("annotations") or {}
            timezone = annotations.get("timezone") or {}

            lat = geometry.get("lat")
            lng = geometry.get("lng")

            if lat is None or lng is None:
                continue  # skip broken entries

            results.append(
                LocationResponse(
                    label=item.get("formatted"),
                    latitude=lat,
                    longitude=lng,
                    timezone=timezone.get("offset_sec", 0) / 3600,
                )
            )

        return results

    except httpx.TimeoutException:
        raise LocationServiceError("Location service timeout")

    except httpx.HTTPStatusError as exc:
        raise LocationServiceError(
            f"Location provider error (status {exc.response.status_code})"
        )

    except Exception as exc:
        raise LocationServiceError(
            "Unexpected error while fetching location"
        ) from exc

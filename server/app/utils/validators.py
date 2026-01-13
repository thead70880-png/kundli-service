from datetime import datetime
from fastapi import HTTPException


def validate_datetime(dt: datetime) -> None:
    if not (1800 <= dt.year <= 2200):
        raise HTTPException(
            status_code=400,
            detail="Year must be between 1800 and 2200",
        )


def validate_coordinates(lat: float, lon: float) -> None:
    if not (-90.0 <= lat <= 90.0):
        raise HTTPException(
            status_code=400,
            detail="Latitude must be between -90 and 90",
        )

    if not (-180.0 <= lon <= 180.0):
        raise HTTPException(
            status_code=400,
            detail="Longitude must be between -180 and 180",
        )

    if lat == 0.0 and lon == 0.0:
        raise HTTPException(
            status_code=400,
            detail="Invalid coordinates (0,0)",
        )


def validate_timezone(offset: float) -> None:
    if not (-14.0 <= offset <= 14.0):
        raise HTTPException(
            status_code=400,
            detail="Timezone offset must be between -14 and +14",
        )

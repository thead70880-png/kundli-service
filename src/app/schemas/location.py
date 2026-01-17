from pydantic import BaseModel, Field


class LocationResponse(BaseModel):
    """
    Normalized location response used by the Kundli service.
    """
    label: str = Field(..., description="Human-readable place name")
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    timezone: float = Field(
        ...,
        description="Timezone offset from UTC in hours (e.g. +5.5)"
    )

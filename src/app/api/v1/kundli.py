import logging
from fastapi import APIRouter, HTTPException, status, Request
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, Any

from app.core.rate_limit import limiter
from app.engine.kundli_engine import generate_kundli, KundliGenerationError

logger = logging.getLogger("kundli-service.kundli")

router = APIRouter(
    prefix="/kundli",
    tags=["Kundli"]
)

# ---------------------------------------------------------
# REQUEST SCHEMA (Pydantic v2 SAFE)
# ---------------------------------------------------------
class KundliGenerateRequest(BaseModel):
    name: Optional[str] = Field(default=None, max_length=100)

    date: str = Field(..., description="Birth date in YYYY-MM-DD")
    time: str = Field(..., description="Birth time in HH:MM:SS")
    timezone: float = Field(..., description="Timezone offset from UTC (e.g. 5.5)")

    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)

    @field_validator("date")
    @classmethod
    def validate_date(cls, v: str) -> str:
        if len(v) != 10 or v[4] != "-" or v[7] != "-":
            raise ValueError("date must be YYYY-MM-DD")
        return v

    @field_validator("time")
    @classmethod
    def validate_time(cls, v: str) -> str:
        if len(v) != 8 or v[2] != ":" or v[5] != ":":
            raise ValueError("time must be HH:MM:SS")
        return v


# ---------------------------------------------------------
# RESPONSE SCHEMA (INTENTIONALLY FLEXIBLE)
# ---------------------------------------------------------
class KundliGenerateResponse(BaseModel):
    meta: Dict[str, Any]
    time: Dict[str, Any]
    summary: Dict[str, Any]
    charts: Dict[str, Any]
    planets: Optional[Any] = None
    karak: Optional[Any] = None
    avastha: Optional[Any] = None
    vimshottari: Optional[Any] = None


# ---------------------------------------------------------
# API ENDPOINT
# ---------------------------------------------------------
@router.post(
    "/generate",
    response_model=KundliGenerateResponse,
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("10/minute")
async def generate_kundli_api(
    request: Request,
    payload: KundliGenerateRequest,
):
    """
    Generates D1 (Rāśi) and D9 (Navāṁśa) Kundli.
    AstroSage-parity compliant.
    """

    try:
        kundli = generate_kundli(
            name=payload.name,
            date_str=payload.date,
            time_str=payload.time,
            timezone=payload.timezone,
            latitude=payload.latitude,
            longitude=payload.longitude,
        )

        logger.info("Kundli generated successfully")

        # -------------------------------------------------
        # DISPLAY NORMALIZATION (SAFE, NON-DESTRUCTIVE)
        # -------------------------------------------------
        DISPLAY_NORMALIZATION = {
            "Mrat": "Mrita",
            "Vradha": "Vriddha",
            "Swatha": "Swastha",
            "Shant": "Shanta",
            "Mrita": "Mrita",
            "Vriddha": "Vriddha",
            "Swastha": "Swastha",
            "Shanta": "Shanta",
        }

        avasthas = kundli.get("avastha")
        if isinstance(avasthas, list):
            for a in avasthas:
                for key in ("baladi", "deeptadi", "avastha"):
                    if key in a and a[key] in DISPLAY_NORMALIZATION:
                        a[key] = DISPLAY_NORMALIZATION[a[key]]

        return kundli

    except KundliGenerationError as exc:
        logger.exception("Kundli generation error")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    except Exception as exc:
        logger.exception("Unhandled Kundli service error")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Kundli service error",
        )

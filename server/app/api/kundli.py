import logging
from datetime import datetime
from typing import Optional, Dict, Any

from fastapi import APIRouter, HTTPException, status, Request
from pydantic import BaseModel, Field

from app.core.rate_limit import limiter
from app.engine.kundli_engine import generate_kundli, KundliGenerationError


logger = logging.getLogger("kundli-service.kundli")

router = APIRouter(
    prefix="/kundli",
    tags=["Kundli"]
)

# =========================================================
# REQUEST SCHEMA
# =========================================================
class KundliGenerateRequest(BaseModel):
    """
    Incoming request payload for Kundli generation.
    Validation is semantic (not string-length based) to
    avoid false 422 errors from FastAPI.
    """

    name: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Optional name of the native"
    )

    date: str = Field(
        ...,
        description="Birth date in YYYY-MM-DD format"
    )

    time: str = Field(
        ...,
        description="Birth time in HH:MM:SS format"
    )

    timezone: float = Field(
        ...,
        description="Timezone offset from UTC (e.g. 5.5 for IST)"
    )

    latitude: float = Field(
        ...,
        ge=-90.0,
        le=90.0,
        description="Latitude (-90 to 90)"
    )

    longitude: float = Field(
        ...,
        ge=-180.0,
        le=180.0,
        description="Longitude (-180 to 180)"
    )

    # -----------------------------------------------------
    # Semantic validation (prevents random 422 errors)
    # -----------------------------------------------------
    def model_post_init(self, __context):
        try:
            datetime.strptime(
                f"{self.date.strip()} {self.time.strip()}",
                "%Y-%m-%d %H:%M:%S"
            )
        except Exception:
            raise ValueError(
                "Invalid date/time. Expected YYYY-MM-DD and HH:MM:SS"
            )


# =========================================================
# RESPONSE SCHEMA (FLEXIBLE, ENGINE-DRIVEN)
# =========================================================
class KundliGenerateResponse(BaseModel):
    """
    Response schema intentionally flexible.
    Calculation structure is controlled by engine,
    NOT the API layer.
    """
    meta: Dict[str, Any]
    time: Dict[str, Any]
    summary: Dict[str, Any]
    charts: Dict[str, Any]


# =========================================================
# API ENDPOINT
# =========================================================
@router.post(
    "/generate",
    response_model=KundliGenerateResponse,
    status_code=status.HTTP_201_CREATED
)
@limiter.limit("10/minute")
async def generate_kundli_api(
    request: Request,
    payload: KundliGenerateRequest
):
    """
    Generate D1 (Rāśi) and D9 (Navāṁśa) Kundli.
    AstroSage-parity compliant.
    """

    try:
        kundli = generate_kundli(
            name=payload.name,
            date_str=payload.date.strip(),
            time_str=payload.time.strip(),
            timezone=payload.timezone,
            latitude=payload.latitude,
            longitude=payload.longitude
        )

        logger.info("Kundli generated successfully")

        # -------------------------------------------------
        # DISPLAY-ONLY NORMALIZATION (NO CALCULATION TOUCH)
        # -------------------------------------------------
        DISPLAY_NORMALIZATION = {
            "Mrat": "Mrita",
            "Vradha": "Vriddha",
            "Swatha": "Swastha",
            "Shant": "Shanta",
            # Idempotent safety
            "Mrita": "Mrita",
            "Vriddha": "Vriddha",
            "Swastha": "Swastha",
            "Shanta": "Shanta",
        }

        try:
            avasthas = kundli.get("avastha")
            if isinstance(avasthas, list):
                for a in avasthas:
                    if "baladi" in a and a["baladi"] in DISPLAY_NORMALIZATION:
                        a["baladi"] = DISPLAY_NORMALIZATION[a["baladi"]]
                    if "deeptadi" in a and a["deeptadi"] in DISPLAY_NORMALIZATION:
                        a["deeptadi"] = DISPLAY_NORMALIZATION[a["deeptadi"]]
        except Exception:
            # Never fail request due to display normalization
            logger.exception("Avastha display normalization failed")

        return kundli

    except KundliGenerationError as exc:
        logger.exception("Kundli generation error")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc)
        )

    except Exception:
        logger.exception("Unhandled Kundli service error")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Kundli service error"
        )

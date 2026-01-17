from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


# =========================================================
# BASE CONFIG (STRICT, FROZEN, FRONTEND CONTRACT)
# =========================================================

class BaseSchema(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        validate_assignment=True,
        populate_by_name=True,
    )


# =========================================================
# CHART MODELS (RENDERING-ONLY, ASTROSAGE STYLE)
# =========================================================

class PlanetLiteSchema(BaseSchema):
    """
    Lightweight planet model for chart rendering only
    (Used in D1/D9 charts)
    """
    name: str
    degree: Optional[float] = None
    retrograde: Optional[bool] = None


class HouseSchema(BaseSchema):
    """
    Fixed North-Indian house slot (AstroSage style)
    """
    house: int = Field(..., ge=1, le=12)
    sign: int = Field(..., ge=1, le=12)
    isLagna: bool
    planets: List[PlanetLiteSchema]


class D1HouseChartSchema(BaseSchema):
    """
    D1 (Rāśi) Chart – Fixed houses, signs move
    """
    chart: str
    lagna_sign: int = Field(..., ge=1, le=12)
    houses: List[HouseSchema]
    planets_raw: Optional[List[Dict[str, Any]]] = None


class D9SignChartSchema(BaseSchema):
    """
    D9 (Navāṁśa) Chart – Sign-based grouping
    """
    chart: str
    lagna_sign: int = Field(..., ge=1, le=12)
    signs: Dict[int, List[PlanetLiteSchema]]
    planets_raw: Optional[List[Dict[str, Any]]] = None


class ChartsSchema(BaseSchema):
    """
    All charts used in Kundli rendering
    """
    D1: D1HouseChartSchema
    D9: D9SignChartSchema
    # Future charts (D10, D12, etc.) can be added safely


# =========================================================
# META / TIME / SUMMARY (ASTROSAGE SUMMARY STRIP)
# =========================================================

class MetaSchema(BaseSchema):
    name: Optional[str]
    ayanamsa: str
    zodiac: str
    house_system: str


class TimeSchema(BaseSchema):
    local_datetime: str
    utc_datetime: str
    julian_day: float
    timezone: float


class SummarySchema(BaseSchema):
    """
    AstroSage-style Kundli summary strip
    """
    ascendant: str
    ascendant_nakshatra: Optional[str] = None
    ascendant_pada: Optional[int] = None

    sun: Optional[str] = None
    sun_nakshatra: Optional[str] = None
    sun_pada: Optional[int] = None

    moon: Optional[str] = None
    moon_nakshatra: Optional[str] = None
    moon_pada: Optional[int] = None


# =========================================================
# PLANETARY TABLE (ASTROSAGE-ALIGNED, STRICT)
# =========================================================

class PlanetDetailSchema(BaseSchema):
    """
    AstroSage-style planetary table row
    (Rāśi + Navāṁśa + State)
    """

    # Identity
    name: str

    # Longitude
    longitude: float
    longitude_dms: Optional[str] = None

    # RĀŚI (D1)
    sign: int                      # Sign index (1–12)
    house: int                     # House index (1–12)
    degree_in_sign: float

    nakshatra: Optional[str] = None
    nakshatra_index: Optional[int] = None
    pada: Optional[int] = None

    # NAVĀṀŚA (D9) – EXPLICIT
    navamsa_sign: Optional[str] = None
    navamsa_index: Optional[int] = None

    # STATE
    retrograde: bool
    combust: bool
    relationship: str

    # META
    ayanamsa: Optional[str] = None


# =========================================================
# KARAKA / AVASTHA / DASHA TABLES
# =========================================================

class KarakSchema(BaseSchema):
    """
    Sthira & Chara Karakas (AstroSage style)
    """
    sthir: Dict[str, str]
    chara: Dict[str, str]


class AvasthaItemSchema(BaseSchema):
    """
    Deeptadi Avastha (V1 scope)
    """
    planet: str
    avastha: str


class DashaPeriodSchema(BaseSchema):
    planet: str
    start: str
    end: str


class MahadashaSchema(DashaPeriodSchema):
    duration: str
    antardasha: Optional[List[DashaPeriodSchema]] = None


class CurrentDashaInfoSchema(BaseSchema):
    mahadasha: Optional[str] = None
    antardasha: Optional[str] = None


class VimshottariSchema(BaseSchema):
    """
    Vimshottari Dasha (AstroSage-style, rendering-safe)
    """
    mahadasha: List[MahadashaSchema]
    current: CurrentDashaInfoSchema


# =========================================================
# FINAL RESPONSE ROOT (V1 – LOCKED)
# =========================================================

class KundliResponse(BaseSchema):
    """
    FINAL Kundli Response Schema
    Version-1 (AstroSage parity, frontend contract)
    """

    meta: MetaSchema
    time: TimeSchema
    summary: SummarySchema
    charts: ChartsSchema

    # TABLES (AstroSage mental model)
    planets: List[PlanetDetailSchema]
    karak: KarakSchema
    avastha: List[AvasthaItemSchema]
    vimshottari: VimshottariSchema

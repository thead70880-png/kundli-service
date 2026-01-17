from typing import List, Dict, Optional
from pydantic import BaseModel, ConfigDict


# ==================================================
# AVASTHA (ASTROSAGE STYLE)
# ==================================================

class AvasthaSchema(BaseModel):
    jagrat: str = ""
    baladi: str = ""
    deeptadi: str

    model_config = ConfigDict(extra="forbid")


# ==================================================
# PLANET (PLANETARY RELATIONS)
# ==================================================

class PlanetDetailSchema(BaseModel):
    # Identity
    name: str

    # D1 (Rāśi)
    sign: str                 # "Leo"
    house: Optional[int] = None

    # Longitude
    longitude: float
    degree_in_sign: float
    longitude_dms: Optional[str] = None

    # Nakshatra
    nakshatra: Optional[str] = None
    nakshatra_index: Optional[int] = None
    pada: Optional[int] = None

    # Navamsa (D9)
    navamsa_sign: Optional[str] = None
    navamsa_index: Optional[int] = None

    # State
    retrograde: bool
    combust: bool
    dignity: str

    # Avastha
    avastha: AvasthaSchema

    # Meta
    ayanamsa: Optional[str] = None

    model_config = ConfigDict(extra="allow")


# ==================================================
# KARAKAS
# ==================================================

class KarakaSchema(BaseModel):
    sthira: Dict[str, str]
    chara: Dict[str, str]


# ==================================================
# DASHA
# ==================================================

class DashaPeriodSchema(BaseModel):
    planet: str
    start: str
    end: str
    duration: Optional[str] = None


class VimshottariSchema(BaseModel):
    mahadasha: List[DashaPeriodSchema]
    current: Dict[str, Optional[str]]


# ==================================================
# FINAL RESPONSE
# ==================================================

class PlanetaryRelationsResponse(BaseModel):
    planets: List[PlanetDetailSchema]
    karakas: KarakaSchema
    vimshottari: VimshottariSchema

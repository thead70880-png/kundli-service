from fastapi import APIRouter, HTTPException, Query, status

from app.schemas.planetary_relations import PlanetaryRelationsResponse
from app.engine.planets import (
    compute_planetary_positions,
    _get_nakshatra,
    longitude_to_dms,
)
from app.engine.houses import compute_ascendant
from app.engine.planetary_engine import compute_karakas, compute_avasthas
from app.engine.dasha_engine import compute_vimshottari_dasha
from app.utils.time_utils import compute_time_context
from app.constants.zodiac import SIGN_NAMES


router = APIRouter(
    prefix="/planetary-relations",
    tags=["Planetary Relations"]
)


@router.get(
    "",
    response_model=PlanetaryRelationsResponse,
    status_code=status.HTTP_200_OK
)
async def get_planetary_relations(
    date: str = Query(...),
    time: str = Query(...),
    timezone: float = Query(...),
    latitude: float = Query(...),
    longitude: float = Query(...),
):
    try:
        # 1. Time
        time_ctx = compute_time_context(date, time, timezone)
        jd = time_ctx["julian_day"]
        birth_dt = time_ctx["local_datetime"]

        # 2. Ascendant
        asc = compute_ascendant(jd, latitude, longitude)
        lagna_sign = asc["lagna_sign"]
        lagna_degree = asc["lagna_degree"]

        asc_longitude = (lagna_sign - 1) * 30 + lagna_degree
        asc_nk = _get_nakshatra(asc_longitude)

        # 3. Planets
        planets = compute_planetary_positions(jd, lagna_sign)

        planets.insert(0, {
            "name": "Asc",
            "longitude": asc_longitude,
            "sign": lagna_sign,
            "house": 1,
            "degree_in_sign": lagna_degree,
            "longitude_dms": longitude_to_dms(lagna_degree),
            "nakshatra": asc_nk["nakshatra"],
            "nakshatra_index": asc_nk["nakshatra_index"],
            "pada": asc_nk["pada"],
            "retrograde": False,
            "combust": False,
            "relationship": "",
            "ayanamsa": "Lahiri"
        })

        # 4. Karakas (NORMALIZED ONCE)
        karakas_raw = compute_karakas(planets)
        karakas = {
            "sthira": karakas_raw["sthir"],
            "chara": karakas_raw["chara"]
        }

        # 5. Avastha (NORMALIZED ONCE)
        raw_avastha = compute_avasthas(planets)
        avastha_map = {
            a["planet"]: {
                "jagrat": "",
                "baladi": "",
                "deeptadi": a["avastha"]
            }
            for a in raw_avastha
        }

        # 6. Vimshottari
        moon = next(p for p in planets if p["name"] == "Moon")
        vimshottari = compute_vimshottari_dasha(
            moon_longitude=moon["longitude"],
            birth_date=birth_dt
        )

        # 7. FINAL NORMALIZATION (SINGLE LOOP, FINAL SHAPE)
        final_planets = [
    {
        "name": p["name"],

        # Rashi
        "sign": SIGN_NAMES[p["sign"] - 1],                            # 1–12
        "sign_name": SIGN_NAMES[p["sign"] - 1],       # display only
        "house": p.get("house"),

        # Longitude
        "longitude": p["longitude"],
        "degree_in_sign": p["degree_in_sign"],
        "longitude_dms": p.get("longitude_dms"),

        # Nakshatra
        "nakshatra": p.get("nakshatra"),
        "nakshatra_index": p.get("nakshatra_index"),
        "pada": p.get("pada"),

        # Navamsa
        "navamsa_sign": p.get("navamsa_sign"),
        "navamsa_index": p.get("navamsa_index"),

        # State
        "retrograde": p["retrograde"],
        "combust": p["combust"],
        "dignity": p.get("relationship", ""),

        # Avastha
        "avastha": avastha_map[p["name"]],

        # Meta
        "ayanamsa": p.get("ayanamsa"),
    }
    for p in planets
]


        return PlanetaryRelationsResponse(
            planets=final_planets,
            karakas=karakas,
            vimshottari=vimshottari
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )

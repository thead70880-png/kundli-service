from typing import Dict, List

from app.engine.houses import compute_ascendant
from app.engine.planets import (
    compute_planetary_positions,
    _get_nakshatra,
    longitude_to_dms,
)
from app.engine.divisional_charts import compute_d9_lagna, compute_d9_chart
from app.utils.math_utils import house_from_sign



def _build_houses(*, planets: List[Dict[str, object]], lagna_sign: int):
    """
    ASTROSAGE-CORRECT D1 HOUSE BUILDER
    Whole Sign houses relative to Lagna.
    """

    # Step 1: Create 12 fixed houses (1–12)
    houses = []
    for house in range(1, 13):
        # Calculate sign occupying this house
        sign = ((lagna_sign + house - 2) % 12) + 1

        houses.append({
            "house": house,                # ✅ FIXED house number
            "sign": sign,                  # ✅ Lagna-relative sign
            "isLagna": house == 1,          # ✅ Lagna always house 1
            "planets": [],
        })

    # Step 2: Place planets using CORRECT house calculation
    for planet in planets:
        planet_house = house_from_sign(
            planet_sign=int(planet["sign"]),
            lagna_sign=lagna_sign
        )

        degree = (
            planet["degree_in_sign"]
            if "degree_in_sign" in planet
            else planet.get("degree")
        )

        houses[planet_house - 1]["planets"].append({
            "name": planet["name"],
            "degree": degree,
            "retrograde": planet.get("retrograde"),
        })

    return houses

def _build_d9_signs(*, planets: List[Dict[str, object]]):
    """
    ASTROSAGE-CORRECT NAVAMSHA (D9) SIGN-BASED BUILDER
    No houses, only signs (1–12 fixed).
    """
    signs = {i: [] for i in range(1, 13)}

    for planet in planets:
        sign = int(planet["sign"])

        degree = (
            planet.get("degree_in_sign")
            or planet.get("degree")
        )

        signs[sign].append({
            "name": planet["name"],
            "degree": degree,
            "retrograde": planet.get("retrograde"),
        })

    return signs



# ---------------------------------------------------------
# PUBLIC API
# ---------------------------------------------------------
def build_kundli(
    julian_day: float,
    latitude: float,
    longitude: float
) -> Dict[str, object]:

    # -------------------------------------------------
    # 1. ASCENDANT (SINGLE SOURCE OF TRUTH)
    # -------------------------------------------------
    asc = compute_ascendant(julian_day, latitude, longitude)
    lagna_sign = asc["lagna_sign"]
    lagna_degree = asc["lagna_degree"]

    # Absolute sidereal longitude (CRITICAL FIX)
    asc_longitude = (lagna_sign - 1) * 30 + lagna_degree
    asc_nk = _get_nakshatra(asc_longitude)

    # -------------------------------------------------
    # 2. D1 PLANETS (WITH HOUSE PARITY)
    # -------------------------------------------------
    d1_planets = compute_planetary_positions(julian_day, lagna_sign)

    # -------------------------------------------------
    # 3. INJECT ASCENDANT (ASTROSAGE STYLE – FIXED)
    # -------------------------------------------------
    d1_planets.insert(0, {
        "name": "Asc",
        "longitude": asc_longitude,          # ✅ absolute longitude
        "sign": lagna_sign,
        "degree_in_sign": lagna_degree,       # ✅ 0–30 only
        "house": 1,
        "retrograde": False,
        "combust": False,
        "relationship": "",
        "nakshatra": asc_nk["nakshatra"],
        "nakshatra_index": asc_nk["nakshatra_index"],
        "pada": asc_nk["pada"],
        "longitude_dms": longitude_to_dms(lagna_degree),
        "ayanamsa": "Lahiri"
    })

    # -------------------------------------------------
    # 4. BUILD D1 HOUSES
    # -------------------------------------------------
    d1_houses = _build_houses(
        planets=d1_planets,
        lagna_sign=lagna_sign
    )

    # -------------------------------------------------
    # 5. D9 (NAVAMSHA)
    # -------------------------------------------------
    d9_lagna_sign = compute_d9_lagna(lagna_sign, lagna_degree)
    d9_planets = compute_d9_chart(d1_planets, d9_lagna_sign)

    d9_signs = _build_d9_signs(planets=d9_planets)


    # -------------------------------------------------
    # 6. FINAL RESPONSE
    # -------------------------------------------------
    return {
    "D1": {
        "chart": "D1",
        "lagna_sign": lagna_sign,
        "houses": d1_houses,
        "planets_raw": d1_planets,
    },
    "D9": {
        "chart": "D9",
        "lagna_sign": d9_lagna_sign,
        "signs": d9_signs,          
        "planets_raw": d9_planets,
    },
}


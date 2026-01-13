from typing import Dict, List
import swisseph as swe

from app.engine.navamsa import compute_navamsa_sign
from app.constants.zodiac import SIGN_NAMES


class PlanetComputationError(Exception):
    pass


# ---------------------------------------------------------
# SIDEREAL CONFIGURATION
# ---------------------------------------------------------
swe.set_sid_mode(swe.SIDM_LAHIRI)

AYANAMSA_MODE = swe.SIDM_LAHIRI
AYANAMSA_NAME = "Lahiri"


# ---------------------------------------------------------
# CONSTANTS
# ---------------------------------------------------------
COMBUST_LIMITS = {
    "Mercury": 14.0,
    "Venus": 10.0,
    "Mars": 17.0,
    "Jupiter": 11.0,
    "Saturn": 15.0,
}

SIGN_LORDS = {
    1: "Mars", 2: "Venus", 3: "Mercury", 4: "Moon",
    5: "Sun", 6: "Mercury", 7: "Venus", 8: "Mars",
    9: "Jupiter", 10: "Saturn", 11: "Saturn", 12: "Jupiter"
}

EXALTATION_SIGNS = {
    "Sun": 1, "Moon": 2, "Mars": 10, "Mercury": 6,
    "Jupiter": 4, "Venus": 12, "Saturn": 7
}

DEBILITATION_SIGNS = {
    "Sun": 7, "Moon": 8, "Mars": 4, "Mercury": 12,
    "Jupiter": 10, "Venus": 6, "Saturn": 1
}

NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni",
    "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha",
    "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha",
    "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
    "Uttara Bhadrapada", "Revati"
]

PLANETS = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mars": swe.MARS,
    "Mercury": swe.MERCURY,
    "Jupiter": swe.JUPITER,
    "Venus": swe.VENUS,
    "Saturn": swe.SATURN,
    "Rahu": swe.MEAN_NODE,
    "Ketu": swe.MEAN_NODE,
}


# ---------------------------------------------------------
# HELPERS
# ---------------------------------------------------------
def _normalize_degree(deg: float) -> float:
    return deg % 360.0


def _get_sign(deg: float) -> int:
    return int(deg // 30) + 1


def longitude_to_dms(deg: float) -> str:
    d = int(deg)
    m = int((deg - d) * 60)
    s = int((((deg - d) * 60) - m) * 60)
    return f"{d}° {m}' {s}\""


def _get_nakshatra(deg: float) -> Dict[str, int | str]:
    NAK_WIDTH = 13.333333333333334
    PADA_WIDTH = NAK_WIDTH / 4

    nak_idx = int(deg // NAK_WIDTH)
    nak_idx = min(nak_idx, 26)

    nak_start = nak_idx * NAK_WIDTH
    pada = int((deg - nak_start) // PADA_WIDTH) + 1
    pada = min(pada, 4)

    return {
        "nakshatra": NAKSHATRAS[nak_idx],
        "nakshatra_index": nak_idx + 1,
        "pada": pada,
    }


def _get_relationship(planet: str, sign: int, lon: float) -> str:
    if planet in EXALTATION_SIGNS and EXALTATION_SIGNS[planet] == sign:
        return "exalted"
    if planet in DEBILITATION_SIGNS and DEBILITATION_SIGNS[planet] == sign:
        return "debilitated"
    if SIGN_LORDS.get(sign) == planet:
        return "own"
    return "neutral"


# ---------------------------------------------------------
# MAIN COMPUTATION (FINAL)
# ---------------------------------------------------------
def compute_planetary_positions(
    julian_day: float,
    lagna_sign: int
) -> List[Dict[str, object]]:

    try:
        flags = swe.FLG_SIDEREAL | swe.FLG_SPEED
        results = []

        sun_xx, _ = swe.calc_ut(julian_day, swe.SUN, flags)
        sun_long = _normalize_degree(sun_xx[0])

        rahu_long = None
        rahu_retro = None

        for name, pid in PLANETS.items():
            xx, _ = swe.calc_ut(julian_day, pid, flags)
            lon = _normalize_degree(xx[0])
            retro = xx[3] < 0

            if name == "Rahu":
                rahu_long = lon
                rahu_retro = retro

            if name == "Ketu":
                lon = _normalize_degree(rahu_long + 180)
                retro = rahu_retro

            sign = _get_sign(lon)
            degree_in_sign = lon % 30

            # ✅ AstroSage house logic
            house = ((sign - lagna_sign + 12) % 12) + 1

            separation = min(abs(lon - sun_long), 360 - abs(lon - sun_long))
            combust = name in COMBUST_LIMITS and separation <= COMBUST_LIMITS[name]

            # 🔒 NAVAMSA (FINAL)
            nav_index = compute_navamsa_sign(
                sign_index=sign - 1,
                degree_in_sign=degree_in_sign
            )

            results.append({
                "name": name,
                "longitude": lon,
                "sign": sign,
                "house": house,
                "degree_in_sign": degree_in_sign,
                **_get_nakshatra(lon),
                "retrograde": retro,
                "combust": combust,
                "relationship": _get_relationship(name, sign, lon),
                "longitude_dms": longitude_to_dms(degree_in_sign),
                "navamsa_index": nav_index,
                "navamsa_sign": SIGN_NAMES[nav_index],
                "ayanamsa": AYANAMSA_NAME,
            })

        return results

    except Exception as exc:
        raise PlanetComputationError(str(exc)) from exc

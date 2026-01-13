from typing import Dict, Any
from datetime import datetime

from app.core.constants import ZODIAC_SIGNS
from app.utils.time_utils import compute_time_context
from app.engine.chart_builder import build_kundli
from app.engine.planets import _get_nakshatra
from app.engine.houses import compute_ascendant
from app.engine.planetary_engine import compute_karakas, compute_avasthas
from app.engine.dasha_engine import compute_vimshottari_dasha


class KundliGenerationError(Exception):
    pass


def generate_kundli(
    *,
    date_str: str,
    time_str: str,
    timezone: float,
    latitude: float,
    longitude: float,
    name: str | None = None
) -> Dict[str, Any]:

    try:
        # -------------------------------------------------
        # 1. TIME CONTEXT
        # -------------------------------------------------
        time_ctx = compute_time_context(
            date_str=date_str,
            time_str=time_str,
            timezone=timezone
        )
        julian_day = time_ctx["julian_day"]

        # -------------------------------------------------
        # 2. BUILD CHARTS (SOURCE OF TRUTH)
        # -------------------------------------------------
        charts = build_kundli(
            julian_day=julian_day,
            latitude=latitude,
            longitude=longitude
        )

        d1_planets = charts["D1"]["planets_raw"]

        # -------------------------------------------------
        # 3. ASCENDANT SUMMARY
        # -------------------------------------------------
        asc = compute_ascendant(julian_day, latitude, longitude)
        lagna_sign = asc["lagna_sign"]
        lagna_degree = asc["lagna_degree"]

        asc_longitude = (lagna_sign - 1) * 30 + lagna_degree
        lagna_nk = _get_nakshatra(asc_longitude)

        # -------------------------------------------------
        # 4. SUN / MOON
        # -------------------------------------------------
        sun = next(p for p in d1_planets if p["name"] == "Sun")
        moon = next(p for p in d1_planets if p["name"] == "Moon")

        # -------------------------------------------------
        # 5. KARAKA / AVASTHA
        # -------------------------------------------------
        karak = compute_karakas(d1_planets)
        avastha = compute_avasthas(d1_planets)

        # -------------------------------------------------
        # 6. VIMSHOTTARI DASHA
        # -------------------------------------------------
        birth_datetime = datetime.strptime(
            f"{date_str} {time_str}",
            "%Y-%m-%d %H:%M:%S"
        )

        vimshottari = compute_vimshottari_dasha(
            moon_longitude=moon["longitude"],
            birth_date=birth_datetime
        )

        reshaped_charts = {
            "D1": charts["D1"],
            "D9": charts["D9"]
        }


        # -------------------------------------------------
        # 7. FINAL RESPONSE
        # -------------------------------------------------
        return {
            "meta": {
                "name": name,
                "ayanamsa": "Lahiri",
                "zodiac": "Sidereal",
                "house_system": "Whole Sign"
            },
            "time": {
                "local_datetime": time_ctx["local_datetime"].isoformat(),
                "utc_datetime": time_ctx["utc_datetime"].isoformat(),
                "julian_day": julian_day,
                "timezone": timezone
            },
            "summary": {
                "ascendant": ZODIAC_SIGNS[lagna_sign],
                "ascendant_nakshatra": lagna_nk["nakshatra"],
                "ascendant_pada": lagna_nk["pada"],
                "sun": ZODIAC_SIGNS[sun["sign"]],
                "sun_nakshatra": sun["nakshatra"],
                "sun_pada": sun["pada"],
                "moon": ZODIAC_SIGNS[moon["sign"]],
                "moon_nakshatra": moon["nakshatra"],
                "moon_pada": moon["pada"]
            },
            "charts": reshaped_charts,
            "planets": d1_planets,
            "karak": karak,
            "avastha": avastha,
            "vimshottari": vimshottari
        }

    except Exception as exc:
        raise KundliGenerationError(str(exc)) from exc


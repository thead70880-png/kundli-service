# app/core/ephemeris.py

import swisseph as swe

FLAGS = swe.FLG_SWIEPH | swe.FLG_SIDEREAL  # 🔒 sidereal only

def get_planet_longitude(julian_day: float, planet_id: int) -> float:
    xx, _ = swe.calc_ut(julian_day, planet_id, FLAGS)
    return xx[0] % 360.0


def is_retrograde(julian_day: float, planet_id: int) -> bool:
    xx, _ = swe.calc_ut(julian_day, planet_id, FLAGS | swe.FLG_SPEED)
    return xx[3] < 0

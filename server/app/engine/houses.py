# app/engine/houses.py

from typing import Dict
import swisseph as swe


class AscendantComputationError(Exception):
    """Raised when ascendant (lagna) computation fails."""
    pass


def compute_ascendant(
    julian_day: float,
    latitude: float,
    longitude: float
) -> Dict[str, float]:
    """
    Computes the Ascendant (Lagna) in SIDEREAL zodiac
    using Swiss Ephemeris, matching Jagannatha Hora.

    - Houses: Placidus (internal)
    - Zodiac: Sidereal
    - Ayanamsa: Lahiri
    - Returns: lagna_sign (1-12), lagna_degree (0-30 within sign)
    """

    try:
        # ---------------------------------------------------------
        # 1. Ensure Lahiri ayanamsa
        # ---------------------------------------------------------
        swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0)

        # ---------------------------------------------------------
        # 2. Compute tropical ascendant (houses are ALWAYS tropical)
        # ---------------------------------------------------------
        houses, ascmc = swe.houses_ex(
            julian_day,
            latitude,
            longitude,
            b'P',                 # Placidus (JHora internal)
            swe.FLG_SWIEPH
        )

        tropical_asc = ascmc[0]

        # ---------------------------------------------------------
        # 3. Convert to sidereal
        # ---------------------------------------------------------
        ayanamsa = swe.get_ayanamsa_ut(julian_day)
        sidereal_asc = (tropical_asc - ayanamsa) % 360.0

        # ---------------------------------------------------------
        # 4. Zodiac sign
        # ---------------------------------------------------------
        lagna_sign = int(sidereal_asc // 30) + 1

        if not 1 <= lagna_sign <= 12:
            raise AscendantComputationError(
                f"Invalid lagna sign computed: {lagna_sign}"
            )

        # Calculate degree within the sign (0-30)
        degree_in_sign = sidereal_asc % 30
        
        # Full sidereal longitude can be reconstructed as:
        # asc_longitude = (lagna_sign - 1) * 30 + lagna_degree
        # This is used in other parts of the codebase to calculate absolute longitude
        
        # Defensive guard: Ensure lagna_degree is within bounds
        assert 0 <= degree_in_sign < 30, f"Asc degree_in_sign must be < 30, got {degree_in_sign}"
        
        return {
            "lagna_sign": lagna_sign,
            "lagna_degree": degree_in_sign
        }

    except Exception as exc:
        raise AscendantComputationError(
            f"Ascendant computation failed: {exc}"
        ) from exc

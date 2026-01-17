from typing import Dict, List


class DivisionalChartError(Exception):
    pass


# ---------------------------------------------------------
# BASIC HELPERS
# ---------------------------------------------------------
def sign_from_degree(deg: float) -> int:
    """Absolute longitude → Rasi sign (1–12)"""
    return int((deg % 360.0) // 30) + 1


# ---------------------------------------------------------
# NAVAMSA (D9) — ASTROSAGE PARITY
# ---------------------------------------------------------
def _compute_navamsa_sign(rasi_sign: int, degree_in_sign: float) -> int:
    """
    Compute Navamsa sign from rasi sign and degree-in-sign.
    Matches AstroSage & JHora.
    """
    deg = degree_in_sign % 30.0
    navamsa_index = min(8, int(deg // (30.0 / 9.0)))

    # Movable signs
    if rasi_sign in (1, 4, 7, 10):
        start = rasi_sign
    # Fixed signs
    elif rasi_sign in (2, 5, 8, 11):
        start = ((rasi_sign + 8 - 1) % 12) + 1
    # Dual signs
    else:
        start = ((rasi_sign + 4 - 1) % 12) + 1

    return ((start + navamsa_index - 1) % 12) + 1


def compute_d9_lagna(lagna_sign: int, lagna_degree: float) -> int:
    """
    Compute Navamsa Lagna.
    """
    return _compute_navamsa_sign(lagna_sign, lagna_degree)


def compute_d9_chart(
    planets: List[Dict[str, object]],
    d9_lagna_sign: int
) -> List[Dict[str, object]]:
    """
    Compute D9 (Navamsa) chart from D1 planets.
    Backend-only, sign-accurate, AstroSage parity.
    """

    if d9_lagna_sign is None:
        raise DivisionalChartError("D9 lagna sign required")

    results = []

    for p in planets:
        if "degree_in_sign" in p:
            degree = float(p["degree_in_sign"])
        else:
            degree = float(p.get("degree", 0.0))

        rasi_sign = int(p["sign"])
        d9_sign = _compute_navamsa_sign(rasi_sign, degree)

        results.append({
            "name": p["name"],
            "sign": d9_sign,
            "degree": degree,
            "retrograde": p.get("retrograde"),
        })

    return results

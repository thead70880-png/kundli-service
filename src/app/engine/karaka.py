from typing import List, Dict

# JHora / AstroSage Chara Karaka order (8-karaka scheme)
KARAKA_ORDER = [
    "Atmakaraka",     # AK
    "Amatyakaraka",   # AmK
    "Bhratrikaraka",  # BK
    "Pitrikaraka",    # PiK
    "Putrakaraka",    # PK
    "Matrikaraka",    # MK
    "Gnatikaraka",    # GK
    "Darakaraka",     # DK
]

# Chara karakas include Rahu, exclude Ketu & Lagna
CHARA_PLANETS = {
    "Sun",
    "Moon",
    "Mars",
    "Mercury",
    "Jupiter",
    "Venus",
    "Saturn",
    "Rahu",
}


def _get_degree_in_sign(p: Dict[str, object]) -> float:
    """
    Extract effective degree within sign for Chara Karaka calculation.
    Rahu degree is reversed (30 - degree), per JHora / AstroSage.
    """
    if "degree_in_sign" in p:
        deg = float(p["degree_in_sign"])
    elif "degree" in p:
        deg = float(p["degree"])
    else:
        raise KeyError("Planet has no degree information")

    if p.get("name") == "Rahu":
        return 30.0 - deg

    return deg


def compute_chara_karakas(planets: List[Dict[str, object]]) -> Dict[str, str]:
    """
    Compute Chara Karakas (Jaimini) — AstroSage / JHora parity.

    Rules:
    - Use 8-karaka scheme
    - Include Rahu (with reversed degree)
    - Exclude Ketu & Lagna
    - Sort by effective degree-in-sign (descending)
    """

    eligible = [
        p for p in planets
        if p.get("name") in CHARA_PLANETS
    ]

    if len(eligible) != 8:
        raise ValueError(
            f"Expected 8 planets for Chara Karaka, got {len(eligible)}"
        )

    # Sort by effective degree-in-sign DESCENDING
    eligible.sort(
        key=_get_degree_in_sign,
        reverse=True
    )

    return {
        KARAKA_ORDER[i]: eligible[i]["name"]
        for i in range(8)
    }

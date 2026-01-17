# avastha.py
# AstroSage / Parashara compliant Avastha calculations
# Implements: Jagrat / Baladi / Deeptadi

from typing import Dict, Optional

# --------------------------------------------------
# BALADI AVASTHA (degree based)
# --------------------------------------------------

def get_baladi_avastha(deg_in_sign: float) -> str:
    """
    Baladi Avastha based on degree within sign (0–30)
    """
    if deg_in_sign < 6:
        return "Bala"
    elif deg_in_sign < 12:
        return "Kumar"
    elif deg_in_sign < 18:
        return "Yuva"
    elif deg_in_sign < 24:
        return "Vriddha"
    else:
        return "Mritya"


# --------------------------------------------------
# JAGRAT / SWAPNA / SUSHUPTA
# --------------------------------------------------

def get_jagrat_avastha(dignity: str) -> str:
    """
    dignity expected values:
    exalted | own | friendly | neutral | enemy | debilitated
    """
    dignity = dignity.lower()

    if dignity in ("exalted", "own", "friendly"):
        return "Jagrat"
    elif dignity == "neutral":
        return "Swapna"
    else:
        return "Sushupta"


# --------------------------------------------------
# DEEPTADI AVASTHA
# --------------------------------------------------

def get_deeptadi_avastha(
    dignity: str,
    combust: bool = False
) -> str:
    """
    Deeptadi Avastha
    Combustion overrides everything except exaltation (AstroSage behavior)
    """
    dignity = dignity.lower()

    if dignity == "exalted":
        return "Deepta"

    if combust:
        return "Dukhita"

    if dignity == "own":
        return "Swa"
    elif dignity == "friendly":
        return "Shanta"
    elif dignity == "neutral":
        return "Mudita"
    else:
        # enemy or debilitated
        return "Dukhita"


# --------------------------------------------------
# MASTER AVASTHA FUNCTION
# --------------------------------------------------

def calculate_avastha(
    planet: str,
    deg_in_sign: float,
    dignity: str,
    combust: bool = False
) -> Dict[str, Optional[str]]:
    """
    Returns full AstroSage-style avastha set for a planet.
    Ascendant should be passed with dignity=None.
    """

    if planet.lower() in ("asc", "lagna"):
        return {
            "jagrat": None,
            "baladi": None,
            "deeptadi": "Shanta"
        }

    return {
        "jagrat": get_jagrat_avastha(dignity),
        "baladi": get_baladi_avastha(deg_in_sign),
        "deeptadi": get_deeptadi_avastha(dignity, combust)
    }

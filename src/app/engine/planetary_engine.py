from typing import Dict, List, Any

# =========================================================
# KARAKA (V1 – ASTROSAGE STYLE)
# =========================================================

STHIR_KARAKAS = {
    "Sun": "Atma",
    "Moon": "Matru",
    "Mars": "Bhratru",
    "Mercury": "Amatya",
    "Jupiter": "Putra",
    "Venus": "Dara",
    "Saturn": "Gnati",
}

CHARA_ORDER = [
    "Atma",
    "Amatya",
    "Bhratru",
    "Matru",
    "Putra",
    "Gnati",
    "Dara",
]


def compute_karakas(planets: List[Dict[str, Any]]) -> Dict[str, Dict[str, str]]:
    """
    FINAL V1 Karaka computation (AstroSage parity)
    """

    eligible = [
        p for p in planets
        if p["name"] in STHIR_KARAKAS
    ]

    eligible.sort(
        key=lambda p: (p["degree_in_sign"], p["longitude"]),
        reverse=True
    )

    chara = {
        CHARA_ORDER[i]: eligible[i]["name"]
        for i in range(len(CHARA_ORDER))
    }

    return {
        "sthir": STHIR_KARAKAS,
        "chara": chara
    }


# =========================================================
# AVASTHA (V1 – DEEPTADI ONLY, ASTROSAGE PARITY)
# =========================================================

EXALT_SIGNS = {
    "Sun": 1,
    "Moon": 2,
    "Mars": 10,
    "Mercury": 6,
    "Jupiter": 4,
    "Venus": 12,
    "Saturn": 7,
}

DEBIL_SIGNS = {
    "Sun": 7,
    "Moon": 8,
    "Mars": 4,
    "Mercury": 12,
    "Jupiter": 10,
    "Venus": 6,
    "Saturn": 1,
}

SIGN_LORDS = {
    1: "Mars", 2: "Venus", 3: "Mercury", 4: "Moon",
    5: "Sun", 6: "Mercury", 7: "Venus", 8: "Mars",
    9: "Jupiter", 10: "Saturn", 11: "Saturn", 12: "Jupiter"
}

FRIENDS = {
    "Sun": ["Moon", "Mars", "Jupiter"],
    "Moon": ["Sun", "Mercury"],
    "Mars": ["Sun", "Moon", "Jupiter"],
    "Mercury": ["Sun", "Venus"],
    "Jupiter": ["Sun", "Moon", "Mars"],
    "Venus": ["Mercury", "Saturn"],
    "Saturn": ["Mercury", "Venus"],
}


def compute_avasthas(planets: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """
    FINAL V1 Deeptadi Avastha (AstroSage parity)
    """

    CLASSICAL = {"Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"}
    result = []

    for p in planets:
        name = p["name"]
        sign = p["sign"]

        if name not in CLASSICAL:
            avastha = "Shanta"

        elif EXALT_SIGNS.get(name) == sign:
            avastha = "Deepta"

        elif DEBIL_SIGNS.get(name) == sign:
            avastha = "Dukhita"

        elif SIGN_LORDS[sign] == name:
            avastha = "Swastha"

        elif SIGN_LORDS[sign] in FRIENDS.get(name, []):
            avastha = "Muditha"

        else:
            avastha = "Shanta"

        result.append({
            "planet": name,
            "avastha": avastha
        })

    return result

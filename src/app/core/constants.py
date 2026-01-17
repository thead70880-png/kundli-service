"""
Domain-level constants for the Kundli microservice.
AstroSage-compatible defaults.
"""

# ---------------------------------------------------------
# AYANAMSA
# ---------------------------------------------------------
AYANAMSA_LAHIRI = "Lahiri"

SUPPORTED_AYANAMSA = {
    AYANAMSA_LAHIRI
}

DEFAULT_AYANAMSA = AYANAMSA_LAHIRI


# ---------------------------------------------------------
# ZODIAC & HOUSE SYSTEMS
# ---------------------------------------------------------
ZODIAC_SIDEREAL = "Sidereal"

HOUSE_SYSTEM_WHOLE_SIGN = "Whole Sign"


# ---------------------------------------------------------
# CHART TYPES
# ---------------------------------------------------------
CHART_D1 = "D1"   # Rāśi
CHART_D9 = "D9"   # Navāṁśa

SUPPORTED_CHARTS = {
    CHART_D1,
    CHART_D9
}


# ---------------------------------------------------------
# PLANET ORDER (ASTROSAGE STANDARD)
# ---------------------------------------------------------
PLANET_ORDER = [
    "Sun",
    "Moon",
    "Mars",
    "Mercury",
    "Jupiter",
    "Venus",
    "Saturn",
    "Rahu",
    "Ketu"
]


# ---------------------------------------------------------
# ZODIAC SIGNS
# Aries = 1, Taurus = 2, ..., Pisces = 12
# ---------------------------------------------------------
ZODIAC_SIGNS = {
    1: "Aries",
    2: "Taurus",
    3: "Gemini",
    4: "Cancer",
    5: "Leo",
    6: "Virgo",
    7: "Libra",
    8: "Scorpio",
    9: "Sagittarius",
    10: "Capricorn",
    11: "Aquarius",
    12: "Pisces",
}


# ---------------------------------------------------------
# SIGN NATURE (USED FOR DIVISIONAL CHARTS)
# ---------------------------------------------------------
MOVABLE_SIGNS = {1, 4, 7, 10}
FIXED_SIGNS = {2, 5, 8, 11}
DUAL_SIGNS = {3, 6, 9, 12}


# ---------------------------------------------------------
# DEGREE CONSTANTS
# ---------------------------------------------------------
FULL_CIRCLE = 360.0
SIGN_DEGREE = 30.0
NAVAMSA_DIVISION = SIGN_DEGREE / 9.0  # 3.333333....

# ---------------------------------------------------------
# PLANET SPECIALIZATION (For Avastha Calculation)
# ---------------------------------------------------------
EXALTED_PLANETS = {
    "Sun": 1,  # Aries
    "Moon": 2,  # Taurus
    "Mars": 10, # Capricorn
    "Mercury": 6, # Virgo
    "Jupiter": 4, # Sagittarius
    "Venus": 12, # Pisces
    "Saturn": 7  # Libra
}

DEBILITATED_PLANETS = {
    "Sun": 7,  # Libra
    "Moon": 8,  # Scorpio
    "Mars": 4,  # Capricorn
    "Mercury": 12,  # Pisces
    "Jupiter": 10,  # Capricorn
    "Venus": 6,  # Virgo
    "Saturn": 1  # Aries
}

COMBUST_LIMITS = {
    "Sun": 17,  # Degrees
    "Moon": 12,
    "Mars": 8,
    "Mercury": 10,
    "Jupiter": 11,
    "Venus": 8,
    "Saturn": 15
}

# ---------------------------------------------------------
# PLANET SPECIALITIES (Used for classification)
# ---------------------------------------------------------
PLANET_SPECIAL_CLASSES = {
    "Sun": "luminary",
    "Moon": "luminary",
    "Mercury": "neutral",
    "Venus": "benefic",
    "Mars": "malefic",
    "Jupiter": "benefic",
    "Saturn": "malefic",
    "Rahu": "shadow",
    "Ketu": "shadow"
}

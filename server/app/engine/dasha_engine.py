from datetime import datetime, timedelta
from typing import Dict, Any

# ---------------------------------------------------------
# CONSTANTS
# ---------------------------------------------------------
NAKSHATRA_WIDTH = 13.333333333333334
DAYS_PER_YEAR = 365.2425
TOTAL_CYCLE_YEARS = 120

DASHA_LORDS = [
    "Ketu", "Venus", "Sun", "Moon", "Mars",
    "Rahu", "Jupiter", "Saturn", "Mercury"
]

DASHA_YEARS = {
    "Ketu": 7,
    "Venus": 20,
    "Sun": 6,
    "Moon": 10,
    "Mars": 7,
    "Rahu": 18,
    "Jupiter": 16,
    "Saturn": 19,
    "Mercury": 17,
}


# ---------------------------------------------------------
# PUBLIC API (FINAL – VERSION 1)
# ---------------------------------------------------------
def compute_vimshottari_dasha(
    *,
    moon_longitude: float,
    birth_date: datetime
) -> Dict[str, Any]:
    """
    Vimshottari Dasha – AstroSage parity (Version-1)

    - Keyword-only arguments (prevents wiring bugs)
    - Uses Moon longitude for Nakshatra
    - Anchors balance to birth date (no birth time)
    """

    # 1. Nakshatra index (0–26)
    nak_idx = int(moon_longitude // NAKSHATRA_WIDTH)
    lord_idx = nak_idx % 9

    start_lord = DASHA_LORDS[lord_idx]
    total_years = DASHA_YEARS[start_lord]

    elapsed = moon_longitude % NAKSHATRA_WIDTH
    remaining_ratio = 1.0 - (elapsed / NAKSHATRA_WIDTH)

    balance_days = int(remaining_ratio * total_years * DAYS_PER_YEAR)

    birth_date_only = birth_date.date()
    first_end = birth_date_only + timedelta(days=balance_days)

    # Build Mahadasha sequence
    sequence = DASHA_LORDS[lord_idx:] + DASHA_LORDS[:lord_idx]

    mahadashas = []
    current_start = birth_date_only
    current_end = first_end

    # --- First (Balance) Mahadasha ---
    mahadashas.append({
        "planet": start_lord,
        "start": current_start.strftime("%Y-%m-%d"),
        "end": current_end.strftime("%Y-%m-%d"),
        "duration": f"{balance_days} days (bal)",
        "antardasha": []
    })

    # --- Remaining Mahadashas ---
    for lord in sequence[1:]:
        years = DASHA_YEARS[lord]
        next_end = current_end.replace(year=current_end.year + years)

        mahadashas.append({
            "planet": lord,
            "start": current_end.strftime("%Y-%m-%d"),
            "end": next_end.strftime("%Y-%m-%d"),
            "duration": f"{years}y",
            "antardasha": []
        })

        current_end = next_end

    # --- Current Dasha Detection ---
    today = datetime.now().date()
    current = {"mahadasha": None, "antardasha": None}

    for md in mahadashas:
        s = datetime.strptime(md["start"], "%Y-%m-%d").date()
        e = datetime.strptime(md["end"], "%Y-%m-%d").date()
        if s <= today < e:
            current["mahadasha"] = md["planet"]
            break

    return {
        "mahadasha": mahadashas,
        "current": current
    }

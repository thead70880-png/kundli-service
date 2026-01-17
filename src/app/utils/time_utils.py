from datetime import datetime, timedelta
from typing import Dict
import swisseph as swe


class TimeComputationError(Exception):
    """Raised when time computation fails."""
    pass


def compute_time_context(
    date_str: str,
    time_str: str,
    timezone: float
) -> Dict[str, object]:
    """
    Computes Julian Day (UT) exactly as required by Swiss Ephemeris.
    Matches Jagannatha Hora when inputs are identical.
    """

    print("TIME_UTILS FILE:", __file__)
    print("INPUT DATE:", date_str, time_str, "TZ:", timezone)

    try:
        # ---------------------------------------------------------
        # 1. Parse LOCAL date and time
        # ---------------------------------------------------------
        full_time_str = f"{date_str} {time_str}".strip()
        local_datetime = None

        formats_to_try = [
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M",
            "%Y/%m/%d %H:%M:%S",
            "%d-%m-%Y %H:%M:%S",
        ]

        for fmt in formats_to_try:
            try:
                local_datetime = datetime.strptime(full_time_str, fmt)
                break
            except ValueError:
                continue

        if local_datetime is None:
            try:
                local_datetime = datetime.fromisoformat(full_time_str)
            except ValueError:
                raise TimeComputationError(
                    f"Could not parse date/time string: '{full_time_str}'"
                )

        # ---------------------------------------------------------
        # 2. Convert LOCAL time → UTC (ONCE, ONLY ONCE)
        # ---------------------------------------------------------
        offset_minutes = round(timezone * 60)
        utc_datetime = local_datetime - timedelta(minutes=offset_minutes)

        # ---------------------------------------------------------
        # 3. Convert UTC time → fractional hour
        # ---------------------------------------------------------
        hour_fraction = (
            utc_datetime.hour
            + utc_datetime.minute / 60.0
            + utc_datetime.second / 3600.0
        )

        # ---------------------------------------------------------
        # 4. Compute Julian Day (UT, Gregorian)
        # ---------------------------------------------------------
        julian_day_ut = swe.julday(
            utc_datetime.year,
            utc_datetime.month,
            utc_datetime.day,
            hour_fraction,
            swe.GREG_CAL
        )

        # ---------------------------------------------------------
        # 5. Safety validation
        # ---------------------------------------------------------
        if not isinstance(julian_day_ut, float):
            raise TimeComputationError("Julian Day is not a float")

        return {
            "local_datetime": local_datetime,
            "utc_datetime": utc_datetime,
            "julian_day": julian_day_ut,
            "timezone": timezone,
        }

    except Exception as exc:
        raise TimeComputationError(
            f"Time computation failed: {exc}"
        ) from exc

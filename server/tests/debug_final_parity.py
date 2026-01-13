import swisseph as swe

from app.core.swisseph_init import init_swisseph
from app.utils.time_utils import compute_time_context
from app.core.ephemeris import get_planet_longitude
from app.engine.houses import compute_ascendant

# -------------------------------------------------
# 1. INIT SWISS EPHEMERIS
# -------------------------------------------------
init_swisseph()

# -------------------------------------------------
# 2. INPUT (MATCHING JHORA)
# -------------------------------------------------
date_str = "2006-01-17"
time_str = "12:12:00"     # seconds = 00
timezone = 5.5            # IST

latitude = 28 + 50/60     # 28°50' N
longitude = 78 + 47/60    # 78°47' E

# -------------------------------------------------
# 3. TIME CONTEXT
# -------------------------------------------------
time_ctx = compute_time_context(
    date_str=date_str,
    time_str=time_str,
    timezone=timezone
)

jd = time_ctx["julian_day"]

print("\n--- TIME CHECK ---")
print("Local DT :", time_ctx["local_datetime"])
print("UTC DT   :", time_ctx["utc_datetime"])
print("Julian Day (UT):", jd)

# -------------------------------------------------
# 4. ASCENDANT CHECK
# -------------------------------------------------
asc = compute_ascendant(jd, latitude, longitude)

print("\n--- ASCENDANT CHECK ---")
print("Lagna Degree :", asc["lagna_degree"])
print("Lagna Sign   :", asc["lagna_sign"], "(1=Aries)")

# -------------------------------------------------
# 5. PLANETARY LONGITUDES (SIDEREAL)
# -------------------------------------------------
PLANETS = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mars": swe.MARS,
    "Mercury": swe.MERCURY,
    "Jupiter": swe.JUPITER,
    "Venus": swe.VENUS,
    "Saturn": swe.SATURN,
    "Rahu (True)": swe.TRUE_NODE,
}

print("\n--- SIDEREAL LONGITUDES (LAHIRI) ---")

for name, pid in PLANETS.items():
    lon = get_planet_longitude(jd, pid)
    print(f"{name:12s}: {lon:.6f}")

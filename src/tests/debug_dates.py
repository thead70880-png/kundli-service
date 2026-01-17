import swisseph as swe
from datetime import datetime, timedelta

swe.set_sid_mode(swe.SIDM_LAHIRI)

def get_positions(date_str, time_str, lat, lon_deg):
    dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S")
    # Convert IST to UTC
    dt_utc = dt - timedelta(hours=5.5)
    
    jd = swe.julday(dt_utc.year, dt_utc.month, dt_utc.day, 
                    dt_utc.hour + dt_utc.minute/60 + dt_utc.second/3600, 
                    swe.GREG_CAL)
    
    # Sun
    sun_xx, _ = swe.calc_ut(jd, swe.SUN, swe.FLG_SIDEREAL)
    sun_lon = sun_xx[0] % 360
    
    # Moon
    moon_xx, _ = swe.calc_ut(jd, swe.MOON, swe.FLG_SIDEREAL)
    moon_lon = moon_xx[0] % 360
    
    # Ascendant
    # houses(julday, lat, lon, hsys) -> returns (cusps, ascmc)
    # ascmc[0] is Ascendant
    # Note: lon in swisseph is decimal degrees. 
    _, ascmc = swe.houses(jd, lat, lon_deg, b'W')
    asc_lon = ascmc[0]
    
    print(f"--- {date_str} ---")
    print(f"Sun: {sun_lon:.2f} ({(sun_lon/30)+1:.1f})")
    print(f"Moon: {moon_lon:.2f} ({(moon_lon/30)+1:.1f})")
    print(f"Asc: {asc_lon:.2f} ({(asc_lon/30)+1:.1f})")

# Test Munna 14th vs 15th
print("Debugging Munna Date:")
get_positions("2005-11-14", "23:40:59", 27.1767, 78.0081)
get_positions("2005-11-15", "23:40:59", 27.1767, 78.0081)

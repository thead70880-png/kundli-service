from app.utils.time_utils import compute_time_context
from app.engine.chart_builder import build_kundli


if __name__ == "__main__":
    # --------------------------------------------------
    # Fixed reference chart (JHora verified)
    # --------------------------------------------------
    ctx = compute_time_context(
        date_str="2006-01-17",
        time_str="12:12:00",
        timezone=5.5
    )

    jd = ctx["julian_day"]
    lat = 28.8333   # Moradabad
    lon = 78.7833

    chart = build_kundli(jd, lat, lon)

    print("\n===== D9 DEBUG (BACKEND ONLY) =====")

    d1_houses = chart["D1"]["houses"]
    d9_houses = chart["D9"]["houses"]

    # Flatten D1 planets for easy lookup
    d1_planets = {}
    for h in d1_houses:
        for p in h["planets"]:
            d1_planets[p["name"]] = {
                "sign": h["sign"],
                "degree": p["degree"]
            }

    # Print D9 result planet-by-planet
    for h in d9_houses:
        for p in h["planets"]:
            name = p["name"]
            d1 = d1_planets.get(name)

            print(
                f"{name:>6} | "
                f"D1: Sign {d1['sign']} {d1['degree']:.2f}°  →  "
                f"D9: Sign {h['sign']}"
                f"{' (R)' if p.get('retrograde') else ''}"
            )

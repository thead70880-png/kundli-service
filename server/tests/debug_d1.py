from app.utils.time_utils import compute_time_context
from app.engine.chart_builder import build_kundli


if __name__ == "__main__":
    ctx = compute_time_context(
        date_str="2006-01-17",
        time_str="12:12:00",
        timezone=5.5
    )

    jd = ctx["julian_day"]

    print("\n===== TIME DEBUG =====")
    print("Local DT:", ctx["local_datetime"])
    print("UTC DT  :", ctx["utc_datetime"])
    print("Julian Day:", jd)

    chart = build_kundli(jd, 28.8333, 78.7833)

    print("\n===== D1 PLANETS (SIGN-WISE) =====")
    for h in chart["D1"]["houses"]:
        print(f"\nSign {h['sign']} | Lagna: {h['isLagna']}")
        for p in h["planets"]:
            r = " (R)" if p.get("retrograde") else ""
            print(f"  {p['name']:>6} {p['degree']:.2f}°{r}")

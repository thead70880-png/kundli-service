from app.engine.kundli_engine import generate_kundli

kundli = generate_kundli(
    date_str="1990-08-15",
    time_str="10:30:00",
    timezone=5.5,
    latitude=28.6139,
    longitude=77.2090,
    name="Regression Test"
)

print("\n--- SUMMARY ---")
for k, v in kundli["summary"].items():
    print(f"{k}: {v}")

print("\n--- PLANETARY TABLE (KEY FIELDS) ---")
for p in kundli["planets"]:
    if p["name"] in {"Sun", "Moon", "Saturn", "Rahu", "Ketu"}:
        print({
            "planet": p["name"],
            "sign": p["sign"],
            "house": p["house"],
            "degree": p["longitude_dms"],
            "nakshatra": p["nakshatra"],
            "pada": p["pada"],
            "retro": p["retrograde"],
            "combust": p["combust"],
        })

print("\n--- KARAKA ---")
print(kundli["karak"])

print("\n--- AVASTHA ---")
for a in kundli["avastha"]:
    if a["planet"] in {"Sun", "Moon", "Saturn"}:
        print(a)

print("\n--- VIMSHOTTARI (BIRTH) ---")
md0 = kundli["vimshottari"]["mahadasha"][0]
print(md0["planet"], md0["start"], md0["end"])

print("\n--- CURRENT DASHA ---")
print(kundli["vimshottari"]["current"])

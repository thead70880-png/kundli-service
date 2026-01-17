import os
import sys
from datetime import datetime

# Add the server directory to sys.path to allow importing 'app'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.engine.kundli_engine import generate_kundli
from app.core.swisseph_init import init_swisseph

def run_verification():
    init_swisseph()
    
    test_cases = [
        {
            "name": "Rajat Singh (Reference Case)",
            "date_str": "2006-01-24",
            "time_str": "23:59:59",
            "timezone": 5.5,
            "latitude": 28.8333, # Moradabad
            "longitude": 78.7833,
        },
        {
            "name": "Secondary Case (Debug File)",
            "date_str": "2006-01-17",
            "time_str": "12:12:00",
            "timezone": 5.5,
            "latitude": 28.8333,
            "longitude": 78.7833,
        }
    ]

    for case in test_cases:
        print(f"\n{'='*60}")
        print(f"VERIFYING CASE: {case['name']}")
        print(f"{'='*60}")
        
        try:
            result = generate_kundli(
                date_str=case['date_str'],
                time_str=case['time_str'],
                timezone=case['timezone'],
                latitude=case['latitude'],
                longitude=case['longitude'],
                name=case['name']
            )
            
            # 1. SUMMARY
            print("\n[SUMMARY]")
            s = result['summary']
            print(f"Lagna: {s['ascendant']} ({s['ascendant_nakshatra']}, Pada {s['ascendant_pada']})")
            print(f"Sun  : {s['sun']} ({s['sun_nakshatra']}, Pada {s['sun_pada']})")
            print(f"Moon : {s['moon']} ({s['moon_nakshatra']}, Pada {s['moon_pada']})")

            # 2. PLANETARY POSITIONS (D1)
            print("\n[PLANETARY POSITIONS - D1]")
            print(f"{'Planet':<12} {'Sign':<12} {'Degree':<12} {'Nakshatra':<15} {'Retro':<8}")
            for p in result['planets']:
                # Skip Asc as it's separate in result['planets'] sometimes but here it is included as 'Asc'
                print(f"{p['name']:<12} {p['sign']:<12} {p['longitude_dms']:<12} {p['nakshatra']:<15} {str(p['retrograde']):<8}")

            # 3. KARAKAS
            print("\n[CHARA KARAKAS]")
            for k, v in result['karak']['chara'].items():
                print(f"{k:<12}: {v}")

            # 4. AVASTHAS
            print("\n[AVASTHAS (DEEPTADI)]")
            for av in result['avastha']:
                print(f"{av['planet']:<12}: {av['avastha']}")

            # 5. VIMSHOTTARI DASHA (Current)
            print("\n[VIMSHOTTARI DASHA - CURRENT MAHADASHA]")
            vd = result['vimshottari']
            now = datetime.now()
            current_md = None
            for md in vd:
                start = datetime.fromisoformat(md['start'])
                end = datetime.fromisoformat(md['end'])
                if start <= now <= end:
                    current_md = md
                    break
            
            if current_md:
                print(f"Current Mahadasha: {current_md['planet']}")
                print(f"Period: {current_md['start']} to {current_md['end']}")
            else:
                print("No current Mahadasha found in range.")

            # 6. D9 (NAVAMSA) MATH ONLY (Ignoring rotation bug)
            print("\n[NAVAMSA (D9) SIGN MATH]")
            d9_planets = result['charts']['D9']['planets_raw']
            for p in d9_planets:
                print(f"{p['name']:<12}: Sign {p['sign']}")

        except Exception as e:
            print(f"ERROR: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    run_verification()

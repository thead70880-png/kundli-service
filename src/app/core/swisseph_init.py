# app/core/swisseph_init.py
import os
import swisseph as swe

def init_swisseph():
    swe.set_ephe_path(
        os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "ephemeris")
        )
    )

    # LOCK SIDEREAL MODE GLOBALLY
    swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0)

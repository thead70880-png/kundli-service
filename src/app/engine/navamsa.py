NAVAMSA_SIZE = 30 / 9  # 3.333333...

# 0-based sign index
# Aries = 0, Taurus = 1, ..., Pisces = 11

MOVABLE_SIGNS = {0, 3, 6, 9}     # Aries, Cancer, Libra, Capricorn
FIXED_SIGNS = {1, 4, 7, 10}     # Taurus, Leo, Scorpio, Aquarius
DUAL_SIGNS = {2, 5, 8, 11}      # Gemini, Virgo, Sagittarius, Pisces


def compute_navamsa_sign(sign_index: int, degree_in_sign: float) -> int:
    """
    Compute Navamsa (D9) sign index (0–11) using Parashara method.
    """

    if not (0 <= degree_in_sign < 30):
        raise ValueError("degree_in_sign must be between 0 and 30")

    navamsa_part = int(degree_in_sign / NAVAMSA_SIZE)  # 0–8

    if sign_index in MOVABLE_SIGNS:
        start = sign_index
    elif sign_index in FIXED_SIGNS:
        start = (sign_index + 8) % 12   # 9th from sign
    elif sign_index in DUAL_SIGNS:
        start = (sign_index + 4) % 12   # 5th from sign
    else:
        raise ValueError("Invalid sign index")

    return (start + navamsa_part) % 12

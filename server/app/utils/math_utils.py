def normalize_degree(deg: float) -> float:
    """
    Normalize any angle to 0–360 range.
    """
    return deg % 360.0


def sign_from_degree(deg: float) -> int:
    """
    Aries = 1 ... Pisces = 12
    """
    return int((deg % 360) // 30) + 1


def house_from_sign(planet_sign: int, lagna_sign: int) -> int:
    """
    Whole sign house calculation.
    """
    return ((planet_sign - lagna_sign + 12) % 12) + 1

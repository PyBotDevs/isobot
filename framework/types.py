"""An NKA Framework Module to check and verify various datatypes used across systems."""

def is_hex_color_code(num) -> bool:
    """Checks whether an integer is a valid hexadecimal code.\n\nReturns `True` if valid, returns `False` if invalid."""
    return isinstance(num, int) and 0x000000 <= num <= 0xFFFFFF

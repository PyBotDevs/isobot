"""The isobot framework module for specific client-dependent algorithms."""
# Imports
import random

# Functions
def chance(percentage: int) -> bool:
    """Gives a `True` or `False` outcome for a chance-based event, depending on the `percentage` of the `True` outcome."""
    probability_range = random.randint(1, 100)
    if probability_range <= percentage: return True
    else: return False

"""Checks the network status, by sending an HTTP request to Google's servers, and returns the status."""

import requests

def network_check() -> bool:
    """Checks the network status, by sending an HTTP request to Google's servers, and returns the status."""
    try:
        requests.get("https://www.google.com", timeout=3)
        return True
    except requests.exceptions.ConnectionError:
        return False

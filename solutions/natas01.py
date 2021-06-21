"""
natas1: view source, check comments
"""

import requests
from bs4 import BeautifulSoup

from natas_utils import *

LEVEL = 1

def solve(url: str, login: LevelLogin):
    response = requests.get(url, auth=login)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    # print(soup.prettify())
    content = soup.find("div", {"id": "content"})

    # print(content.prettify())

    # BS4 'contents' does not contain comment delimiters and each element is a
    # line from the source file
    # password is the last "word" in a comment after one line of text
    natas2_password = content.contents[1].strip().split()[-1]

    return natas2_password


if __name__ == "__main__":
    url, login = load_level(LEVEL)
    natas2_password = solve(url, login)

    if natas2_password:
        print("natas2:", natas2_password)
        store_level_password(LEVEL + 1, natas2_password)

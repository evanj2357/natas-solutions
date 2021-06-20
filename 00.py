import json
"""
natas0: just the entry point, flag displays on the page
"""

from natas_utils.natas_utils import load_level
import requests
from bs4 import BeautifulSoup

from natas_utils import *

LEVEL = 0
URL, LOGIN = load_level(LEVEL)

def main():
    response = requests.get(URL, auth=LOGIN)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    content = soup.find("div", {"id": "content"})

    # BS4 'contents' does not contain comment delimiters and each element is a
    # line from the source file
    # password is the last "word" in a comment after one line of text
    natas1_password = content.contents[1].strip().split()[-1]
    print("natas1:", natas1_password)

    store_level_password(LEVEL + 1, natas1_password)

if __name__ == "__main__":
    main()
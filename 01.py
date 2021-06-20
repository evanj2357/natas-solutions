import json
import requests
from bs4 import BeautifulSoup

from natas_utils import *

LEVEL = 1
URL, LOGIN = load_level(LEVEL)

def main():
    response = requests.get(URL, auth=LOGIN)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    # print(soup.prettify())
    content = soup.find("div", {"id": "content"})

    # print(content.prettify())

    # BS4 'contents' does not contain comment delimiters and each element is a
    # line from the source file
    # password is the last "word" in a comment after one line of text
    natas2_password = content.contents[1].strip().split()[-1]
    print("natas2:", natas2_password)

    store_level_password(LEVEL + 1, natas2_password)

if __name__ == "__main__":
    main()
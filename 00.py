import json
import requests
from bs4 import BeautifulSoup

with open("levels.json", "r") as datafile:
    NATAS_DATA = json.load(datafile)

LEVEL = 0
LEVEL_URL = NATAS_DATA["level_url_format"].replace("{LEVEL}", f"natas{LEVEL}")
LOGIN = NATAS_DATA["logins"][LEVEL]

if __name__ == "__main__":
    print(LEVEL_URL)
    print(LOGIN)

    response = requests.get(LEVEL_URL, auth=(LOGIN["username"], LOGIN["password"]))
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    content = soup.find("div", {"id": "content"})

    # BS4 'contents' does not contain comment delimiters and each element is a
    # line from the source file
    # password is the last "word" in a comment after one line of text
    natas1_password = content.contents[1].strip().split()[-1]
    print("natas1:", natas1_password)

    store_level_password(LEVEL + 1, natas2_password)
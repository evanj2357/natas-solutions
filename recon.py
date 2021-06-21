import html
import json
import requests
from bs4 import BeautifulSoup
import sys
from natas_utils import load_level

with open("levels.json", "r") as datafile:
    NATAS_DATA = json.load(datafile)

def main():
    if len(sys.argv) < 2:
        exit("Missing argument: natas level number")

    try:
        level = int(sys.argv[1])
    except:
        exit("invalid level number")

    if level < 0 or level > 34:
        exit("invalid level number")

    level_url, login = load_level(level)

    print(level_url)
    print(login)

    # allow users to pass other paths to retrieve
    path = ""
    if len(sys.argv) > 2:
        path = sys.argv[2]

    if not path.startswith('/'):
        path = '/' + path

    response = requests.get(level_url + path, auth=login)
    response.raise_for_status()

    text = html.unescape(response.text)

    soup = BeautifulSoup(text, "html.parser")
    print(soup.prettify())

    # content = soup.find("div", {"id": "content"})
    # print(content)

if __name__ == "__main__":
    main()
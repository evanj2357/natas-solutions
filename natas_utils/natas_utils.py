import json
import re
from bs4 import BeautifulSoup
import requests

from typing import Iterable, List, Optional, Tuple

from requests.sessions import Session

PW_FORMAT = re.compile(r"[a-zA-Z0-9]{32}")

with open("levels.json", "r") as datafile:
    NATAS_DATA = json.load(datafile)

level_url_format = NATAS_DATA["level_url_format"]

def flag_file_abspath(level_number: int) -> str:
    return NATAS_DATA["flag_path"] + f"natas{level_number}"

def load_level(level_number: int) -> Tuple[str, Tuple[str, str]]:
    level_url = level_url_format.format(level_number)
    login = (
        NATAS_DATA["logins"][level_number]["username"],
        NATAS_DATA["logins"][level_number]["password"],
    )

    return (level_url, login)

def store_level_password(level_number: int, password: str):
    NATAS_DATA["logins"][level_number]["password"] = password

    with open("levels.json", "w") as datafile:
        json.dump(NATAS_DATA, datafile)

def try_level_login(level_number: int, candidate_passwords: Iterable[str], session: Optional[Session] = None, debug: bool = False) -> Optional[str]:
    level_url = level_url_format.format(level_number)

    for pw in candidate_passwords:
        login = (
            f"natas{level_number}",
            pw,
        )
        response = session.get(level_url, auth=login) if session else requests.get(level_url, auth=login)
        if debug: print(pw, end=": ")

        if response.status_code == 200:
            if debug: print("SUCCESS")
            return pw

        if debug: print("FAIL")

    return None

def extract_candidate_passwords(response_text: str, in_html_body: bool = True) -> List[str]:
    contents = ""

    if in_html_body:
        soup = BeautifulSoup(response_text, "html.parser")
        body = soup.find("body")
        contents = body.text if body else ""
    else:
        contents = response_text

    return re.findall(PW_FORMAT, contents)
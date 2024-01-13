import re
import urllib.parse

import validators
from hashids import Hashids

from config import HASH_SALT

hashids = Hashids(salt=HASH_SALT)


def decode_string(encoded):
    decoded = "".join([chr(i) for i in hashids.decode(encoded)])
    return decoded


def is_valid_url(url):
    return validators.url(url)


def extract_gdrive_id(gdrive_link):
    if "drive.google.com" not in gdrive_link:
        return None
    match = re.match(
        r"^https://drive\.google\.com/file/d/([a-zA-Z0-9_-]+)/?.*$", gdrive_link
    )
    if match:
        return match.group(1)
    query_params = urllib.parse.parse_qs(urllib.parse.urlparse(gdrive_link).query)
    if "id" in query_params:
        return query_params["id"][0]
    return None

import os
import re
import urllib.parse
import string
import random
import validators
from hashids import Hashids
from pymongo import MongoClient

hash_salt = os.environ.get("HASH_SALT")
hashids = Hashids(salt=hash_salt)

# db setup
db_url = os.environ.get("MONGO_URL")
client = MongoClient(db_url)
db = client["mydb"]
collection = db["links"]


def decode_string(encoded):
    decoded = "".join([chr(i) for i in hashids.decode(encoded)])
    return decoded


def is_valid_url(url):
    return validators.url(url)

def gen_rand_str():
    r_str = str(''.join(random.choices(string.ascii_letters, k=8)))
    return r_str
    

def auto_increment_id():
    return int(collection.count_documents({})) + 1


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

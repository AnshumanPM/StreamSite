import os

HASH_SALT = os.environ.get("HASH_SALT")
DB_URL = os.environ.get("MONGO_URL")

# Optional
# Dl Urls In case your link banned then replace with new
OLD_DL_BASE_URL_1 = os.environ.get("OLD_DL_BASE_URL_1")
OLD_DL_BASE_URL_2 = os.environ.get("OLD_DL_BASE_URL_2")
NEW_DL_BASE_URL = os.environ.get("NEW_DL_BASE_URL")

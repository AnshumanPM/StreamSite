import os

HASH_SALT = str(os.environ.get("HASH_SALT"))
DB_URL = str(os.environ.get("MONGO_URL"))

# Optional
# Dl Urls In case your link banned then replace with new
OLD_DL_BASE_URL_1 = str(os.environ.get("OLD_DL_BASE_URL_1"))
OLD_DL_BASE_URL_2 = str(os.environ.get("OLD_DL_BASE_URL_2"))
OLD_DL_BASE_URL_3 = str(os.environ.get("OLD_DL_BASE_URL_3"))
NEW_DL_BASE_URL = str(os.environ.get("NEW_DL_BASE_URL"))
NEW_DL_BASE_URL_3 = str(os.environ.get("NEW_DL_BASE_URL_3"))

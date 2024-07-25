import os

HASH_SALT = str(os.environ.get("HASH_SALT"))
DB_URL = str(os.environ.get("MONGO_URL"))

# Optional
# Dl Urls In case your link banned then replace with new
NEW_DL_BASE_URL = str(os.environ.get("NEW_DL_BASE_URL"))
OLD_DL_BASE_URL = list(
    set(x for x in os.environ.get("OLD_DL_BASE_URL", "").split()))

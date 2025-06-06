import base64
import os

DB_URL = os.environ.get("MONGO_URL")
HASH_SALT = str(os.environ.get("HASH_SALT"))
CRYPTO_KEY_B64 = os.environ.get("CRYPTO_KEY_B64")

# Derived
CRYPTO_KEY = base64.b64decode(CRYPTO_KEY_B64)

# Optional
# Dl Urls In case your link banned then replace with new
NEW_DL_BASE_URL = str(os.environ.get("NEW_DL_BASE_URL"))
OLD_DL_BASE_URL = list(set(x for x in os.environ.get("OLD_DL_BASE_URL", "").split()))

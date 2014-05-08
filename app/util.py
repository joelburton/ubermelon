import hashlib
import config

# Create a password hash
def hash_password(password):
    return hashlib.md5( hashlib.md5(password).hexdigest() + config.PASSWORD_SALT + password).hexdigest()

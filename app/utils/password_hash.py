import hashlib
from passlib.hash import bcrypt


def hash_password(password):

    hashed_password = bcrypt.hash(password)

    return hashed_password

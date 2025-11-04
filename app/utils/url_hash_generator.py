import hashlib
import string

from config import settings

# Define Base62 alphabet
BASE62_ALPHABET = string.digits + string.ascii_uppercase + string.ascii_lowercase


def int_to_base62(num: int) -> str:
    """Convert an integer to a Base62 string."""
    if num == 0:
        return BASE62_ALPHABET[0]
    base62 = []
    while num:
        num, rem = divmod(num, 62)
        base62.append(BASE62_ALPHABET[rem])
    return "".join(reversed(base62))


def hash_to_base62_id(numeric_id: int, secret_salt: str, length: int = 8) -> str:
    """Hash numeric ID + salt into an 8-char Base62 unique ID."""
    # 1. Combine numeric ID with salt
    to_hash = f"{numeric_id}{secret_salt}".encode()

    # 2. Hash it
    hash_bytes = hashlib.blake2b(to_hash, digest_size=8).digest()  # fast & secure

    # 3. Convert to integer
    hash_int = int.from_bytes(hash_bytes, "big")

    # 4. Convert to Base62
    base62_str = int_to_base62(hash_int)

    # 5. Ensure fixed length (pad or trim)
    return base62_str[:length].rjust(length, BASE62_ALPHABET[0])


def generate_url_hash_id(numeric_id: int) -> str:
    """
    Public function to generate a product ID.
    Uses a persistent secret salt (should be set via environment variable in production).
    """
    return hash_to_base62_id(numeric_id, secret_salt=settings.HASH_SECRET_KEY)

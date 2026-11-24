import hashlib
import hmac
import os

ITERATIONS = 200_000

def hash_password(password: str) -> str:
    """Return 'iterations$salt$hash' using PBKDF2-SHA256 with a random salt."""
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, ITERATIONS)
    return f"{ITERATIONS}${salt.hex()}${digest.hex()}"

def is_hashed(stored: str) -> bool:
    parts = str(stored).split("$")
    return len(parts) == 3 and parts[0].isdigit()

def verify_password(password: str, stored: str) -> bool:
    if not stored:
        return False
    if not is_hashed(stored):  # old plaintext password from before this change
        return hmac.compare_digest(password.encode("utf-8"), str(stored).encode("utf-8"))
    iterations, salt_hex, digest_hex = stored.split("$")
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), bytes.fromhex(salt_hex), int(iterations)
    )
    return hmac.compare_digest(digest.hex(), digest_hex)

from datetime import datetime, timedelta, timezone

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerifyMismatchError

from app.core.config import settings #This is for importing the settings module from the app.core.config package, which contains configuration variables for the application.

_ph = PasswordHasher()  # Initialize the PasswordHasher instance for hashing and verifying passwords

def hash_password(password: str) -> str:
    return _ph.hash(password)  # Hash the provided password and return the hashed value

def verify_password(password: str, password_hash: str) -> bool:
    try:
        return _ph.verify(password_hash, password)
    except(VerifyMismatchError, InvalidHashError):
        return False  # Return False if the password does not match the hash or if the hash is invalid


def create_access_token(user_id: str) -> str:
    now = datetime.now(timezone.utc) #utc means Coordinated Universal Time, which is the primary time standard by which the world regulates clocks and time. It is the same worldwide and does not change with the seasons.
    payload = {
        "sub": str(user_id),
        "iat": now,
        "exp": now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),  # Set the expiration time for the token based on the configured duration
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)  # Encode the payload into a JWT token using the secret key and specified algorithm

def decode_access_token(token: str) -> int | None:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
            options={"require": ["exp", "iat", "sub"]}
        )
        return int(payload.get("sub"))  # Return the user ID from the token payload if decoding is successful
    except (jwt.PyJWTError, ValueError):
        return None  # Return None if there is an error decoding the token or if the user ID is not found
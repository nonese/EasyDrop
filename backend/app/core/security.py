from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

# Use pbkdf2_sha256 for stable compatibility on Python 3.9 environments.
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)


def create_token(sub: str, token_type: str, expire_min: int) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": sub,
        "typ": token_type,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=expire_min)).timestamp()),
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALG)


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])
    except JWTError as exc:
        raise ValueError("invalid token") from exc

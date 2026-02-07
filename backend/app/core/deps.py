from __future__ import annotations
from dataclasses import dataclass

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.security import decode_token
from app.db.session import get_db
from app.models.models import Device, User

bearer = HTTPBearer(auto_error=False)


@dataclass
class AuthSubject:
    id: str
    token_type: str
    role: str | None = None


def get_current_subject(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
    db: Session = Depends(get_db),
) -> AuthSubject:
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="missing token")

    try:
        payload = decode_token(credentials.credentials)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token")

    subject_id = payload.get("sub")
    token_type = payload.get("typ")

    if token_type == "admin":
        user = db.query(User).filter(User.id == subject_id).first()
        if not user:
            raise HTTPException(status_code=401, detail="user not found")
        return AuthSubject(id=user.id, token_type="admin", role=user.role)

    if token_type == "device":
        device = db.query(Device).filter(Device.id == subject_id).first()
        if not device:
            raise HTTPException(status_code=401, detail="device not found")
        return AuthSubject(id=device.id, token_type="device")

    raise HTTPException(status_code=401, detail="unsupported token type")


def require_admin_or_operator(subject: AuthSubject = Depends(get_current_subject)) -> AuthSubject:
    if subject.token_type != "admin" or subject.role not in {"admin", "operator"}:
        raise HTTPException(status_code=403, detail="insufficient permissions")
    return subject


def extract_bearer_token_from_request(request: Request) -> str | None:
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None
    return auth_header[7:]

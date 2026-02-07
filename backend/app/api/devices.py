import json
import secrets
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.deps import AuthSubject, get_current_subject, require_admin_or_operator
from app.core.security import create_token, now_iso
from app.db.session import get_db
from app.models.models import Device
from app.schemas.device import (
    DeviceLoginRequest,
    DeviceLoginResponse,
    DeviceOut,
    DeviceRegisterRequest,
    DeviceRegisterResponse,
    DeviceUpdateRequest,
)
from app.services.manifest import generate_manifest

router = APIRouter(prefix="/devices", tags=["devices"])


@router.post("/register", response_model=DeviceRegisterResponse)
def register_device(payload: DeviceRegisterRequest, db: Session = Depends(get_db)):
    if payload.type not in {"web", "android"}:
        raise HTTPException(status_code=400, detail="device type must be web/android")

    device_id = str(uuid.uuid4())
    secret = secrets.token_urlsafe(24)

    device = Device(
        id=device_id,
        name=payload.name,
        type=payload.type,
        secret=secret,
        last_seen_at=None,
        status="offline",
        meta_json=json.dumps(payload.meta or {}, ensure_ascii=False),
    )
    db.add(device)
    db.commit()

    return DeviceRegisterResponse(device_id=device_id, secret=secret)


@router.post("/login", response_model=DeviceLoginResponse)
def device_login(payload: DeviceLoginRequest, db: Session = Depends(get_db)):
    device = db.query(Device).filter(Device.id == payload.device_id).first()
    if not device or device.secret != payload.secret:
        raise HTTPException(status_code=401, detail="invalid device credentials")

    token = create_token(device.id, "device", settings.DEVICE_TOKEN_EXPIRE_MIN)
    return DeviceLoginResponse(device_token=token)


@router.get("", response_model=list[DeviceOut])
def list_devices(_: AuthSubject = Depends(require_admin_or_operator), db: Session = Depends(get_db)):
    return db.query(Device).order_by(Device.last_seen_at.desc().nullslast()).all()


@router.get("/{device_id}", response_model=DeviceOut)
def get_device(device_id: str, _: AuthSubject = Depends(require_admin_or_operator), db: Session = Depends(get_db)):
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="device not found")
    return device


@router.put("/{device_id}", response_model=DeviceOut)
def update_device(
    device_id: str,
    payload: DeviceUpdateRequest,
    _: AuthSubject = Depends(require_admin_or_operator),
    db: Session = Depends(get_db),
):
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="device not found")

    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(device, k, v)

    db.commit()
    return device


@router.get("/{device_id}/manifest")
def get_manifest(
    device_id: str,
    since_version: int = 0,
    subject: AuthSubject = Depends(get_current_subject),
    db: Session = Depends(get_db),
):
    if subject.token_type == "device" and subject.id != device_id:
        raise HTTPException(status_code=403, detail="cannot access other device manifest")
    if subject.token_type == "admin" and subject.role not in {"admin", "operator"}:
        raise HTTPException(status_code=403, detail="insufficient permissions")

    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="device not found")

    manifest = generate_manifest(db, device_id)
    manifest["changed"] = manifest["version"] != since_version
    return manifest

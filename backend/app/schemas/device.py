from __future__ import annotations
from typing import Any, Dict, Optional

from pydantic import BaseModel


class DeviceRegisterRequest(BaseModel):
    name: str
    type: str
    meta: Optional[Dict[str, Any]] = None


class DeviceRegisterResponse(BaseModel):
    device_id: str
    secret: str


class DeviceLoginRequest(BaseModel):
    device_id: str
    secret: str


class DeviceLoginResponse(BaseModel):
    device_token: str
    token_type: str = "bearer"


class DeviceOut(BaseModel):
    id: str
    name: str
    type: str
    last_seen_at: Optional[str] = None
    status: str
    meta_json: Optional[str] = None


class DeviceUpdateRequest(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = None

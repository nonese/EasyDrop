from __future__ import annotations
from pydantic import BaseModel


class DeviceRegisterRequest(BaseModel):
    name: str
    type: str
    meta: dict | None = None


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
    last_seen_at: str | None = None
    status: str
    meta_json: str | None = None


class DeviceUpdateRequest(BaseModel):
    name: str | None = None
    status: str | None = None

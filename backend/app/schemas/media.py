from __future__ import annotations
from pydantic import BaseModel


class MediaOut(BaseModel):
    id: str
    filename: str
    ext: str
    size_bytes: int
    sha256: str
    duration_ms: int | None
    mime: str
    storage_path: str
    created_by: str | None
    created_at: str


class MediaUploadResponse(BaseModel):
    media_id: str
    url: str
    sha256: str
    size_bytes: int

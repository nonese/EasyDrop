from __future__ import annotations
from typing import Optional

from pydantic import BaseModel


class MediaOut(BaseModel):
    id: str
    filename: str
    ext: str
    size_bytes: int
    sha256: str
    duration_ms: Optional[int]
    mime: str
    storage_path: str
    created_by: Optional[str]
    created_at: str


class MediaUploadResponse(BaseModel):
    media_id: str
    url: str
    sha256: str
    size_bytes: int

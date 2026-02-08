from __future__ import annotations
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class PlaylistCreateRequest(BaseModel):
    name: str


class PlaylistUpdateRequest(BaseModel):
    name: str


class PlaylistItemCreateRequest(BaseModel):
    media_id: str
    order_index: int
    play_duration_ms: Optional[int] = None


class PlaylistItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    playlist_id: str
    media_id: str
    order_index: int
    play_duration_ms: Optional[int]
    created_at: str


class PlaylistOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    created_by: Optional[str]
    created_at: str
    items: List[PlaylistItemOut] = Field(default_factory=list)

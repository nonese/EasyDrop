from __future__ import annotations
from pydantic import BaseModel


class PlaylistCreateRequest(BaseModel):
    name: str


class PlaylistUpdateRequest(BaseModel):
    name: str


class PlaylistItemCreateRequest(BaseModel):
    media_id: str
    order_index: int
    play_duration_ms: int | None = None


class PlaylistItemOut(BaseModel):
    id: str
    playlist_id: str
    media_id: str
    order_index: int
    play_duration_ms: int | None
    created_at: str


class PlaylistOut(BaseModel):
    id: str
    name: str
    created_by: str | None
    created_at: str
    items: list[PlaylistItemOut] = []

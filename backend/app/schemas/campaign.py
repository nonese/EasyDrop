from __future__ import annotations
from pydantic import BaseModel


class CampaignCreateRequest(BaseModel):
    name: str
    playlist_id: str
    start_at: str
    end_at: str
    week_mask: int | None = None
    daily_start: str | None = None
    daily_end: str | None = None
    priority: int = 0
    enabled: bool = True


class CampaignUpdateRequest(BaseModel):
    name: str | None = None
    playlist_id: str | None = None
    start_at: str | None = None
    end_at: str | None = None
    week_mask: int | None = None
    daily_start: str | None = None
    daily_end: str | None = None
    priority: int | None = None
    enabled: bool | None = None


class CampaignTargetRequest(BaseModel):
    device_ids: list[str]


class CampaignTargetOut(BaseModel):
    id: str
    campaign_id: str
    device_id: str


class CampaignOut(BaseModel):
    id: str
    name: str
    playlist_id: str
    start_at: str
    end_at: str
    week_mask: int | None
    daily_start: str | None
    daily_end: str | None
    priority: int
    enabled: bool
    created_by: str | None
    created_at: str
    targets: list[CampaignTargetOut] = []

from __future__ import annotations
from typing import List, Optional

from pydantic import BaseModel


class CampaignCreateRequest(BaseModel):
    name: str
    playlist_id: str
    start_at: str
    end_at: str
    week_mask: Optional[int] = None
    daily_start: Optional[str] = None
    daily_end: Optional[str] = None
    priority: int = 0
    enabled: bool = True


class CampaignUpdateRequest(BaseModel):
    name: Optional[str] = None
    playlist_id: Optional[str] = None
    start_at: Optional[str] = None
    end_at: Optional[str] = None
    week_mask: Optional[int] = None
    daily_start: Optional[str] = None
    daily_end: Optional[str] = None
    priority: Optional[int] = None
    enabled: Optional[bool] = None


class CampaignTargetRequest(BaseModel):
    device_ids: List[str]


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
    week_mask: Optional[int]
    daily_start: Optional[str]
    daily_end: Optional[str]
    priority: int
    enabled: bool
    created_by: Optional[str]
    created_at: str
    targets: List[CampaignTargetOut] = []

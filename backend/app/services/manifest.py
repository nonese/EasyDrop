from __future__ import annotations
import hashlib
import json
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.models import Campaign, CampaignTarget, Media, PlaylistItem


def _parse_iso(dt: str) -> datetime:
    return datetime.fromisoformat(dt.replace("Z", "+00:00"))


def _in_daily_window(now: datetime, daily_start: str | None, daily_end: str | None) -> bool:
    if not daily_start or not daily_end:
        return True
    now_hm = now.strftime("%H:%M")
    return daily_start <= now_hm <= daily_end


def _in_week_mask(now: datetime, week_mask: int | None) -> bool:
    if week_mask is None:
        return True
    bit = 1 << now.weekday()
    return (week_mask & bit) != 0


def _calculate_version(payload: dict) -> int:
    encoded = json.dumps(payload, ensure_ascii=True, sort_keys=True)
    h = hashlib.sha1(encoded.encode("utf-8")).hexdigest()[:8]
    return int(h, 16)


def generate_manifest(db: Session, device_id: str) -> dict:
    now = datetime.now(timezone.utc)

    campaigns = (
        db.query(Campaign)
        .join(CampaignTarget, CampaignTarget.campaign_id == Campaign.id)
        .filter(CampaignTarget.device_id == device_id, Campaign.enabled.is_(True))
        .all()
    )

    active: list[Campaign] = []
    for c in campaigns:
        if _parse_iso(c.start_at) <= now <= _parse_iso(c.end_at) and _in_week_mask(now, c.week_mask) and _in_daily_window(now, c.daily_start, c.daily_end):
            active.append(c)

    if not active:
        payload = {
            "device_id": device_id,
            "generated_at": now.isoformat(),
            "campaign": None,
            "playlist": None,
        }
        payload["version"] = _calculate_version(payload)
        return payload

    active.sort(key=lambda c: (c.priority, c.created_at), reverse=True)
    picked = active[0]

    items = (
        db.query(PlaylistItem, Media)
        .join(Media, Media.id == PlaylistItem.media_id)
        .filter(PlaylistItem.playlist_id == picked.playlist_id)
        .order_by(PlaylistItem.order_index.asc())
        .all()
    )

    playlist_items = []
    for item, media in items:
        media_type = "video" if media.mime.startswith("video/") else "image"
        playlist_items.append(
            {
                "media_id": media.id,
                "type": media_type,
                "url": f"/static/media/{media.id}.{media.ext}",
                "sha256": media.sha256,
                "size_bytes": media.size_bytes,
                "play_duration_ms": item.play_duration_ms,
            }
        )

    payload = {
        "device_id": device_id,
        "generated_at": now.isoformat(),
        "campaign": {
            "campaign_id": picked.id,
            "name": picked.name,
            "priority": picked.priority,
            "start_at": picked.start_at,
            "end_at": picked.end_at,
        },
        "playlist": {
            "playlist_id": picked.playlist_id,
            "items": playlist_items,
        },
    }
    payload["version"] = _calculate_version(payload)
    return payload

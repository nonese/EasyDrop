import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import AuthSubject, require_admin_or_operator
from app.core.security import now_iso
from app.db.session import get_db
from app.models.models import Campaign, CampaignTarget, Device, Playlist
from app.schemas.campaign import CampaignCreateRequest, CampaignOut, CampaignTargetRequest, CampaignUpdateRequest

router = APIRouter(prefix="/campaigns", tags=["campaigns"])


def _to_campaign_out(campaign: Campaign, db: Session) -> CampaignOut:
    targets = db.query(CampaignTarget).filter(CampaignTarget.campaign_id == campaign.id).all()
    return CampaignOut(
        id=campaign.id,
        name=campaign.name,
        playlist_id=campaign.playlist_id,
        start_at=campaign.start_at,
        end_at=campaign.end_at,
        week_mask=campaign.week_mask,
        daily_start=campaign.daily_start,
        daily_end=campaign.daily_end,
        priority=campaign.priority,
        enabled=campaign.enabled,
        created_by=campaign.created_by,
        created_at=campaign.created_at,
        targets=targets,
    )


@router.post("", response_model=CampaignOut)
def create_campaign(
    payload: CampaignCreateRequest,
    subject: AuthSubject = Depends(require_admin_or_operator),
    db: Session = Depends(get_db),
):
    playlist = db.query(Playlist).filter(Playlist.id == payload.playlist_id).first()
    if not playlist:
        raise HTTPException(status_code=404, detail="playlist not found")

    campaign = Campaign(
        id=str(uuid.uuid4()),
        name=payload.name,
        playlist_id=payload.playlist_id,
        start_at=payload.start_at,
        end_at=payload.end_at,
        week_mask=payload.week_mask,
        daily_start=payload.daily_start,
        daily_end=payload.daily_end,
        priority=payload.priority,
        enabled=payload.enabled,
        created_by=subject.id,
        created_at=now_iso(),
    )
    db.add(campaign)
    db.commit()
    return _to_campaign_out(campaign, db)


@router.get("", response_model=list[CampaignOut])
def list_campaigns(_: AuthSubject = Depends(require_admin_or_operator), db: Session = Depends(get_db)):
    campaigns = db.query(Campaign).order_by(Campaign.created_at.desc()).all()
    return [_to_campaign_out(c, db) for c in campaigns]


@router.get("/{campaign_id}", response_model=CampaignOut)
def get_campaign(campaign_id: str, _: AuthSubject = Depends(require_admin_or_operator), db: Session = Depends(get_db)):
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="campaign not found")
    return _to_campaign_out(campaign, db)


@router.put("/{campaign_id}", response_model=CampaignOut)
def update_campaign(
    campaign_id: str,
    payload: CampaignUpdateRequest,
    _: AuthSubject = Depends(require_admin_or_operator),
    db: Session = Depends(get_db),
):
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="campaign not found")

    updates = payload.model_dump(exclude_unset=True)
    if "playlist_id" in updates:
        playlist = db.query(Playlist).filter(Playlist.id == updates["playlist_id"]).first()
        if not playlist:
            raise HTTPException(status_code=404, detail="playlist not found")

    for key, value in updates.items():
        setattr(campaign, key, value)

    db.commit()
    return _to_campaign_out(campaign, db)


@router.post("/{campaign_id}/targets")
def bind_targets(
    campaign_id: str,
    payload: CampaignTargetRequest,
    _: AuthSubject = Depends(require_admin_or_operator),
    db: Session = Depends(get_db),
):
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="campaign not found")

    created = 0
    for device_id in payload.device_ids:
        device = db.query(Device).filter(Device.id == device_id).first()
        if not device:
            continue

        exists = db.query(CampaignTarget).filter(CampaignTarget.campaign_id == campaign_id, CampaignTarget.device_id == device_id).first()
        if exists:
            continue

        db.add(CampaignTarget(id=str(uuid.uuid4()), campaign_id=campaign_id, device_id=device_id))
        created += 1

    db.commit()
    return {"message": "ok", "created": created}


@router.delete("/targets/{target_id}")
def delete_target(target_id: str, _: AuthSubject = Depends(require_admin_or_operator), db: Session = Depends(get_db)):
    target = db.query(CampaignTarget).filter(CampaignTarget.id == target_id).first()
    if not target:
        raise HTTPException(status_code=404, detail="target not found")
    db.delete(target)
    db.commit()
    return {"message": "deleted"}

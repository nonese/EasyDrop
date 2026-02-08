from __future__ import annotations
import json
import uuid
from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.deps import AuthSubject, get_current_subject, require_admin_or_operator
from app.core.security import now_iso
from app.db.session import get_db
from app.models.models import PlaybackLog

router = APIRouter(prefix="/logs", tags=["logs"])


class ReportRequest(BaseModel):
    event: str
    campaign_id: Optional[str] = None
    media_id: Optional[str] = None
    ts: Optional[str] = None
    detail: Optional[Dict[str, Any]] = None


@router.post("/report")
def report_event(
    payload: ReportRequest,
    subject: AuthSubject = Depends(get_current_subject),
    db: Session = Depends(get_db),
):
    if subject.token_type != "device":
        return {"message": "ignored"}

    log = PlaybackLog(
        id=str(uuid.uuid4()),
        device_id=subject.id,
        campaign_id=payload.campaign_id,
        media_id=payload.media_id,
        event=payload.event,
        ts=payload.ts or now_iso(),
        detail_json=json.dumps(payload.detail or {}, ensure_ascii=False),
    )
    db.add(log)
    db.commit()
    return {"message": "ok"}


@router.get("/devices/{device_id}")
def list_device_logs(
    device_id: str,
    limit: int = 100,
    _: AuthSubject = Depends(require_admin_or_operator),
    db: Session = Depends(get_db),
):
    logs = (
        db.query(PlaybackLog)
        .filter(PlaybackLog.device_id == device_id)
        .order_by(PlaybackLog.ts.desc())
        .limit(limit)
        .all()
    )
    return logs

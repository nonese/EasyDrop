from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import AuthSubject, require_admin_or_operator
from app.db.session import get_db
from app.models.models import CampaignTarget

router = APIRouter(prefix="/campaign-targets", tags=["campaigns"])


@router.delete("/{target_id}")
def delete_campaign_target(target_id: str, _: AuthSubject = Depends(require_admin_or_operator), db: Session = Depends(get_db)):
    target = db.query(CampaignTarget).filter(CampaignTarget.id == target_id).first()
    if not target:
        raise HTTPException(status_code=404, detail="target not found")
    db.delete(target)
    db.commit()
    return {"message": "deleted"}

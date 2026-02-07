from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import AuthSubject, require_admin_or_operator
from app.db.session import get_db
from app.models.models import PlaylistItem

router = APIRouter(prefix="/playlist-items", tags=["playlists"])


@router.delete("/{item_id}")
def delete_playlist_item(item_id: str, _: AuthSubject = Depends(require_admin_or_operator), db: Session = Depends(get_db)):
    item = db.query(PlaylistItem).filter(PlaylistItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="item not found")
    db.delete(item)
    db.commit()
    return {"message": "deleted"}

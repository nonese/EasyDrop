import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import AuthSubject, require_admin_or_operator
from app.core.security import now_iso
from app.db.session import get_db
from app.models.models import Media, Playlist, PlaylistItem
from app.schemas.playlist import (
    PlaylistCreateRequest,
    PlaylistItemCreateRequest,
    PlaylistItemOut,
    PlaylistOut,
    PlaylistUpdateRequest,
)

router = APIRouter(prefix="/playlists", tags=["playlists"])


def _to_playlist_out(playlist: Playlist, db: Session) -> PlaylistOut:
    items = db.query(PlaylistItem).filter(PlaylistItem.playlist_id == playlist.id).order_by(PlaylistItem.order_index.asc()).all()
    item_out = [
        PlaylistItemOut(
            id=i.id,
            playlist_id=i.playlist_id,
            media_id=i.media_id,
            order_index=i.order_index,
            play_duration_ms=i.play_duration_ms,
            created_at=i.created_at,
        )
        for i in items
    ]
    return PlaylistOut(
        id=playlist.id,
        name=playlist.name,
        created_by=playlist.created_by,
        created_at=playlist.created_at,
        items=item_out,
    )


@router.post("", response_model=PlaylistOut)
def create_playlist(
    payload: PlaylistCreateRequest,
    subject: AuthSubject = Depends(require_admin_or_operator),
    db: Session = Depends(get_db),
):
    playlist = Playlist(
        id=str(uuid.uuid4()),
        name=payload.name,
        created_by=subject.id,
        created_at=now_iso(),
    )
    db.add(playlist)
    db.commit()
    return _to_playlist_out(playlist, db)


@router.get("", response_model=list[PlaylistOut])
def list_playlists(_: AuthSubject = Depends(require_admin_or_operator), db: Session = Depends(get_db)):
    playlists = db.query(Playlist).order_by(Playlist.created_at.desc()).all()
    return [_to_playlist_out(p, db) for p in playlists]


@router.get("/{playlist_id}", response_model=PlaylistOut)
def get_playlist(playlist_id: str, _: AuthSubject = Depends(require_admin_or_operator), db: Session = Depends(get_db)):
    playlist = db.query(Playlist).filter(Playlist.id == playlist_id).first()
    if not playlist:
        raise HTTPException(status_code=404, detail="playlist not found")
    return _to_playlist_out(playlist, db)


@router.put("/{playlist_id}", response_model=PlaylistOut)
def update_playlist(
    playlist_id: str,
    payload: PlaylistUpdateRequest,
    _: AuthSubject = Depends(require_admin_or_operator),
    db: Session = Depends(get_db),
):
    playlist = db.query(Playlist).filter(Playlist.id == playlist_id).first()
    if not playlist:
        raise HTTPException(status_code=404, detail="playlist not found")
    playlist.name = payload.name
    db.commit()
    return _to_playlist_out(playlist, db)


@router.post("/{playlist_id}/items")
def add_playlist_item(
    playlist_id: str,
    payload: PlaylistItemCreateRequest,
    _: AuthSubject = Depends(require_admin_or_operator),
    db: Session = Depends(get_db),
):
    playlist = db.query(Playlist).filter(Playlist.id == playlist_id).first()
    if not playlist:
        raise HTTPException(status_code=404, detail="playlist not found")

    media = db.query(Media).filter(Media.id == payload.media_id).first()
    if not media:
        raise HTTPException(status_code=404, detail="media not found")

    item = PlaylistItem(
        id=str(uuid.uuid4()),
        playlist_id=playlist_id,
        media_id=payload.media_id,
        order_index=payload.order_index,
        play_duration_ms=payload.play_duration_ms,
        created_at=now_iso(),
    )
    db.add(item)
    db.commit()
    return {"message": "created", "item_id": item.id}


@router.delete("/items/{item_id}")
def delete_playlist_item(item_id: str, _: AuthSubject = Depends(require_admin_or_operator), db: Session = Depends(get_db)):
    item = db.query(PlaylistItem).filter(PlaylistItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="item not found")
    db.delete(item)
    db.commit()
    return {"message": "deleted"}

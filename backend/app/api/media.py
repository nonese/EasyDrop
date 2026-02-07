import hashlib
import os
import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.deps import AuthSubject, require_admin_or_operator
from app.core.security import now_iso
from app.db.session import get_db
from app.models.models import Media
from app.schemas.media import MediaOut, MediaUploadResponse

router = APIRouter(prefix="/media", tags=["media"])


@router.post("/upload", response_model=MediaUploadResponse)
def upload_media(
    file: UploadFile = File(...),
    subject: AuthSubject = Depends(require_admin_or_operator),
    db: Session = Depends(get_db),
):
    if file.content_type not in settings.ALLOWED_MIME:
        raise HTTPException(status_code=400, detail="unsupported mime type")

    suffix = Path(file.filename or "").suffix.lower().lstrip(".")
    if not suffix:
        raise HTTPException(status_code=400, detail="file extension required")

    media_id = str(uuid.uuid4())
    target_path = settings.MEDIA_DIR / f"{media_id}.{suffix}"

    sha = hashlib.sha256()
    total_size = 0

    with target_path.open("wb") as f:
        while True:
            chunk = file.file.read(1024 * 1024)
            if not chunk:
                break
            total_size += len(chunk)
            if total_size > settings.MAX_UPLOAD_SIZE_BYTES:
                f.close()
                target_path.unlink(missing_ok=True)
                raise HTTPException(status_code=400, detail="file too large")
            sha.update(chunk)
            f.write(chunk)

    media = Media(
        id=media_id,
        filename=file.filename or f"{media_id}.{suffix}",
        ext=suffix,
        size_bytes=total_size,
        sha256=sha.hexdigest(),
        duration_ms=None,
        mime=file.content_type,
        storage_path=os.path.relpath(target_path, settings.BASE_DIR),
        created_by=subject.id,
        created_at=now_iso(),
    )
    db.add(media)
    db.commit()

    return MediaUploadResponse(
        media_id=media_id,
        url=f"/static/media/{media_id}.{suffix}",
        sha256=media.sha256,
        size_bytes=media.size_bytes,
    )


@router.get("", response_model=list[MediaOut])
def list_media(
    limit: int = 50,
    offset: int = 0,
    _: AuthSubject = Depends(require_admin_or_operator),
    db: Session = Depends(get_db),
):
    return db.query(Media).order_by(Media.created_at.desc()).limit(limit).offset(offset).all()


@router.get("/{media_id}", response_model=MediaOut)
def get_media(media_id: str, _: AuthSubject = Depends(require_admin_or_operator), db: Session = Depends(get_db)):
    media = db.query(Media).filter(Media.id == media_id).first()
    if not media:
        raise HTTPException(status_code=404, detail="media not found")
    return media


@router.delete("/{media_id}")
def delete_media(media_id: str, _: AuthSubject = Depends(require_admin_or_operator), db: Session = Depends(get_db)):
    media = db.query(Media).filter(Media.id == media_id).first()
    if not media:
        raise HTTPException(status_code=404, detail="media not found")

    disk_path = settings.BASE_DIR / media.storage_path
    disk_path.unlink(missing_ok=True)
    db.delete(media)
    db.commit()
    return {"message": "deleted"}

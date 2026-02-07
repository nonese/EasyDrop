from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api import auth, campaign_targets, campaigns, devices, logs, media, playlist_items, playlists, ws
from app.core.config import settings
from app.core.security import hash_password, now_iso
from app.db.session import Base, SessionLocal, engine
from app.models.models import User


def bootstrap():
    settings.STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    settings.MEDIA_DIR.mkdir(parents=True, exist_ok=True)
    settings.THUMB_DIR.mkdir(parents=True, exist_ok=True)
    settings.MANIFEST_DIR.mkdir(parents=True, exist_ok=True)

    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        admin = db.query(User).filter(User.username == settings.ADMIN_INIT_USERNAME).first()
        if not admin:
            db.add(
                User(
                    id="admin-seed-user",
                    username=settings.ADMIN_INIT_USERNAME,
                    password_hash=hash_password(settings.ADMIN_INIT_PASSWORD),
                    role="admin",
                    created_at=now_iso(),
                )
            )
            db.commit()


bootstrap()

app = FastAPI(title=settings.APP_NAME)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory=str(settings.STORAGE_DIR)), name="static")

app.include_router(auth.router, prefix=settings.API_PREFIX)
app.include_router(media.router, prefix=settings.API_PREFIX)
app.include_router(devices.router, prefix=settings.API_PREFIX)
app.include_router(playlists.router, prefix=settings.API_PREFIX)
app.include_router(playlist_items.router, prefix=settings.API_PREFIX)
app.include_router(campaigns.router, prefix=settings.API_PREFIX)
app.include_router(campaign_targets.router, prefix=settings.API_PREFIX)
app.include_router(logs.router, prefix=settings.API_PREFIX)
app.include_router(ws.router)


@app.get("/")
def health():
    return {"message": "ok"}

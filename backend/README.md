# EasyDrop Backend (MVP)

## Run

```bash
cd /Users/yaojiaqi/Programs/EasyDrop/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Default seeded admin account:
- username: `admin`
- password: `admin123`

You should change credentials in production using env:
- `ADMIN_INIT_USERNAME`
- `ADMIN_INIT_PASSWORD`
- `JWT_SECRET`

## Implemented APIs

- `POST /api/auth/login`
- `POST /api/media/upload`
- `GET /api/media`
- `GET /api/media/{id}`
- `DELETE /api/media/{id}`
- `POST /api/devices/register`
- `POST /api/devices/login`
- `GET /api/devices`
- `GET /api/devices/{id}`
- `PUT /api/devices/{id}`
- `GET /api/devices/{id}/manifest`
- `POST /api/playlists`
- `GET /api/playlists`
- `GET /api/playlists/{id}`
- `PUT /api/playlists/{id}`
- `POST /api/playlists/{id}/items`
- `DELETE /api/playlists/items/{item_id}`
- `POST /api/campaigns`
- `GET /api/campaigns`
- `GET /api/campaigns/{id}`
- `PUT /api/campaigns/{id}`
- `POST /api/campaigns/{id}/targets`
- `DELETE /api/campaigns/targets/{target_id}`
- `POST /api/logs/report`
- `GET /api/logs/devices/{device_id}`
- `WS /ws/device?token=DEVICE_TOKEN`

## Storage and DB

- DB: `/Users/yaojiaqi/Programs/EasyDrop/data/app.db`
- Media files: `/Users/yaojiaqi/Programs/EasyDrop/storage/media`
- Static URL base: `/static`

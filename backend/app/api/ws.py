import json
import uuid
from collections import defaultdict

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from app.core.security import decode_token, now_iso
from app.db.session import SessionLocal
from app.models.models import Device, PlaybackLog

router = APIRouter(tags=["ws"])


class DeviceConnectionManager:
    def __init__(self):
        self.connections: dict[str, set[WebSocket]] = defaultdict(set)

    async def connect(self, device_id: str, websocket: WebSocket):
        await websocket.accept()
        self.connections[device_id].add(websocket)

    def disconnect(self, device_id: str, websocket: WebSocket):
        self.connections[device_id].discard(websocket)


manager = DeviceConnectionManager()


def _set_device_status(db: Session, device_id: str, status: str):
    device = db.query(Device).filter(Device.id == device_id).first()
    if device:
        device.status = status
        device.last_seen_at = now_iso()
        db.commit()


@router.websocket("/ws/device")
async def device_ws(websocket: WebSocket):
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=4001)
        return

    try:
        payload = decode_token(token)
        if payload.get("typ") != "device":
            raise ValueError("bad token")
        device_id = payload.get("sub")
    except Exception:
        await websocket.close(code=4002)
        return

    if not device_id:
        await websocket.close(code=4003)
        return

    with SessionLocal() as db:
        _set_device_status(db, device_id, "online")

    await manager.connect(device_id, websocket)

    try:
        while True:
            data = await websocket.receive_json()
            msg_type = data.get("type")

            with SessionLocal() as db:
                _set_device_status(db, device_id, "online")

                if msg_type == "heartbeat":
                    await websocket.send_json({"type": "heartbeat_ack", "ts": now_iso()})
                elif msg_type == "report":
                    log = PlaybackLog(
                        id=str(uuid.uuid4()),
                        device_id=device_id,
                        campaign_id=data.get("campaign_id"),
                        media_id=data.get("media_id"),
                        event=data.get("event", "unknown"),
                        ts=data.get("ts") or now_iso(),
                        detail_json=json.dumps(data.get("detail") or {}, ensure_ascii=False),
                    )
                    db.add(log)
                    db.commit()
                elif msg_type == "hello":
                    await websocket.send_json({"type": "hello_ack", "device_id": device_id})
                else:
                    await websocket.send_json({"type": "error", "message": "unsupported message type"})

    except WebSocketDisconnect:
        with SessionLocal() as db:
            _set_device_status(db, device_id, "offline")
        manager.disconnect(device_id, websocket)

from sqlalchemy import Boolean, Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.db.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Text, primary_key=True)
    username = Column(Text, unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    role = Column(Text, nullable=False)
    created_at = Column(Text, nullable=False)


class Device(Base):
    __tablename__ = "devices"

    id = Column(Text, primary_key=True)
    name = Column(Text, nullable=False)
    type = Column(Text, nullable=False)
    secret = Column(Text, nullable=False)
    last_seen_at = Column(Text, nullable=True)
    status = Column(Text, nullable=False)
    meta_json = Column(Text, nullable=True)


class Media(Base):
    __tablename__ = "media"

    id = Column(Text, primary_key=True)
    filename = Column(Text, nullable=False)
    ext = Column(Text, nullable=False)
    size_bytes = Column(Integer, nullable=False)
    sha256 = Column(Text, nullable=False)
    duration_ms = Column(Integer, nullable=True)
    mime = Column(Text, nullable=False)
    storage_path = Column(Text, nullable=False)
    created_by = Column(Text, ForeignKey("users.id"), nullable=True)
    created_at = Column(Text, nullable=False)


class Playlist(Base):
    __tablename__ = "playlists"

    id = Column(Text, primary_key=True)
    name = Column(Text, nullable=False)
    created_by = Column(Text, ForeignKey("users.id"), nullable=True)
    created_at = Column(Text, nullable=False)

    items = relationship("PlaylistItem", back_populates="playlist", cascade="all, delete-orphan")


class PlaylistItem(Base):
    __tablename__ = "playlist_items"

    id = Column(Text, primary_key=True)
    playlist_id = Column(Text, ForeignKey("playlists.id"), nullable=False)
    media_id = Column(Text, ForeignKey("media.id"), nullable=False)
    order_index = Column(Integer, nullable=False)
    play_duration_ms = Column(Integer, nullable=True)
    created_at = Column(Text, nullable=False)

    playlist = relationship("Playlist", back_populates="items")


class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Text, primary_key=True)
    name = Column(Text, nullable=False)
    playlist_id = Column(Text, ForeignKey("playlists.id"), nullable=False)
    start_at = Column(Text, nullable=False)
    end_at = Column(Text, nullable=False)
    week_mask = Column(Integer, nullable=True)
    daily_start = Column(Text, nullable=True)
    daily_end = Column(Text, nullable=True)
    priority = Column(Integer, nullable=False, default=0)
    enabled = Column(Boolean, nullable=False, default=True)
    created_by = Column(Text, ForeignKey("users.id"), nullable=True)
    created_at = Column(Text, nullable=False)


class CampaignTarget(Base):
    __tablename__ = "campaign_targets"

    id = Column(Text, primary_key=True)
    campaign_id = Column(Text, ForeignKey("campaigns.id"), nullable=False)
    device_id = Column(Text, ForeignKey("devices.id"), nullable=False)


class DeviceState(Base):
    __tablename__ = "device_state"

    device_id = Column(Text, ForeignKey("devices.id"), primary_key=True)
    current_campaign_id = Column(Text, nullable=True)
    current_playlist_id = Column(Text, nullable=True)
    client_version = Column(Text, nullable=True)
    last_manifest_version = Column(Integer, nullable=False, default=0)
    last_error = Column(Text, nullable=True)


class PlaybackLog(Base):
    __tablename__ = "playback_logs"

    id = Column(Text, primary_key=True)
    device_id = Column(Text, ForeignKey("devices.id"), nullable=False)
    campaign_id = Column(Text, nullable=True)
    media_id = Column(Text, nullable=True)
    event = Column(Text, nullable=False)
    ts = Column(Text, nullable=False)
    detail_json = Column(Text, nullable=True)

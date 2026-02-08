export interface MediaItem {
  id: string
  filename: string
  ext: string
  size_bytes: number
  sha256: string
  mime: string
  storage_path: string
  created_at: string
}

export interface DeviceItem {
  id: string
  name: string
  type: 'web' | 'android' | string
  status: string
  last_seen_at: string | null
  meta_json: string | null
}

export interface PlaylistItem {
  id: string
  playlist_id: string
  media_id: string
  order_index: number
  play_duration_ms: number | null
  created_at: string
}

export interface Playlist {
  id: string
  name: string
  created_by: string | null
  created_at: string
  items: PlaylistItem[]
}

export interface CampaignTarget {
  id: string
  campaign_id: string
  device_id: string
}

export interface Campaign {
  id: string
  name: string
  playlist_id: string
  start_at: string
  end_at: string
  week_mask: number | null
  daily_start: string | null
  daily_end: string | null
  priority: number
  enabled: boolean
  created_by: string | null
  created_at: string
  targets: CampaignTarget[]
}

export interface PlaybackLog {
  id: string
  device_id: string
  campaign_id: string | null
  media_id: string | null
  event: string
  ts: string
  detail_json: string | null
}

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import api from '@/api/client'
import type { MediaItem, Playlist } from '@/types'

const playlists = ref<Playlist[]>([])
const media = ref<MediaItem[]>([])

const newName = ref('')
const targetPlaylistId = ref('')
const mediaId = ref('')
const orderIndex = ref(0)
const duration = ref<number | null>(null)

const selected = computed(() => playlists.value.find((p) => p.id === targetPlaylistId.value))

const fetchData = async () => {
  const [pRes, mRes] = await Promise.all([api.get<Playlist[]>('/api/playlists'), api.get<MediaItem[]>('/api/media')])
  playlists.value = pRes.data
  media.value = mRes.data
  if (!targetPlaylistId.value && playlists.value[0]) {
    targetPlaylistId.value = playlists.value[0].id
  }
}

const createPlaylist = async () => {
  if (!newName.value.trim()) return
  await api.post('/api/playlists', { name: newName.value.trim() })
  newName.value = ''
  await fetchData()
}

const addItem = async () => {
  if (!targetPlaylistId.value || !mediaId.value) return
  await api.post(`/api/playlists/${targetPlaylistId.value}/items`, {
    media_id: mediaId.value,
    order_index: Number(orderIndex.value),
    play_duration_ms: duration.value,
  })
  await fetchData()
}

const removeItem = async (itemId: string) => {
  await api.delete(`/api/playlist-items/${itemId}`)
  await fetchData()
}

onMounted(fetchData)
</script>

<template>
  <section class="grid-two">
    <article class="glass card">
      <h3>创建播放单</h3>
      <div class="stack">
        <input class="input" v-model="newName" placeholder="如：商场大屏循环" />
        <button class="btn" @click="createPlaylist">创建播放单</button>
      </div>
      <h4>播放单列表</h4>
      <ul class="plain-list">
        <li v-for="p in playlists" :key="p.id">
          <button class="tab tiny" :class="{ active: p.id === targetPlaylistId }" @click="targetPlaylistId = p.id">
            {{ p.name }}（{{ p.items.length }}项）
          </button>
        </li>
      </ul>
    </article>

    <article class="glass card">
      <h3>添加播放项</h3>
      <div class="stack">
        <select class="input" v-model="mediaId">
          <option value="">选择素材</option>
          <option v-for="m in media" :key="m.id" :value="m.id">{{ m.filename }}</option>
        </select>
        <input class="input" type="number" v-model="orderIndex" placeholder="顺序（0开始）" />
        <input class="input" type="number" v-model="duration" placeholder="图片时长(ms，可空)" />
        <button class="btn" @click="addItem">添加</button>
      </div>

      <h4>当前播放项</h4>
      <ul class="plain-list">
        <li v-for="item in selected?.items || []" :key="item.id" class="row-between">
          <span>#{{ item.order_index }} - {{ item.media_id.slice(0, 8) }}</span>
          <button class="btn danger" @click="removeItem(item.id)">删除</button>
        </li>
      </ul>
    </article>
  </section>
</template>

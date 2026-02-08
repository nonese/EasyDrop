<script setup lang="ts">
import { onMounted, ref } from 'vue'
import api from '@/api/client'
import type { MediaItem } from '@/types'

const items = ref<MediaItem[]>([])
const file = ref<File | null>(null)
const loading = ref(false)

const fetchList = async () => {
  const { data } = await api.get<MediaItem[]>('/api/media')
  items.value = data
}

const upload = async () => {
  if (!file.value) return
  loading.value = true
  try {
    const form = new FormData()
    form.append('file', file.value)
    await api.post('/api/media/upload', form, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    file.value = null
    await fetchList()
  } catch (err: any) {
    alert(err?.response?.data?.detail || '上传失败')
  } finally {
    loading.value = false
  }
}

const removeItem = async (id: string) => {
  await api.delete(`/api/media/${id}`)
  await fetchList()
}

onMounted(fetchList)
</script>

<template>
  <section class="grid-two">
    <article class="glass card">
      <h3>上传素材</h3>
      <p class="muted">支持 mp4/webm/jpeg/png</p>
      <div class="stack">
        <input type="file" @change="file = ($event.target as HTMLInputElement).files?.[0] || null" />
        <button class="btn" :disabled="!file || loading" @click="upload">{{ loading ? '上传中...' : '上传' }}</button>
      </div>
    </article>

    <article class="glass card">
      <h3>素材列表</h3>
      <div class="table-wrap">
        <table class="table">
          <thead>
            <tr>
              <th>ID</th>
              <th>文件名</th>
              <th>类型</th>
              <th>大小(MB)</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="m in items" :key="m.id">
              <td>{{ m.id.slice(0, 8) }}</td>
              <td>{{ m.filename }}</td>
              <td>{{ m.mime }}</td>
              <td>{{ (m.size_bytes / 1024 / 1024).toFixed(2) }}</td>
              <td class="actions">
                <a class="link-btn" :href="`http://127.0.0.1:8000/static/media/${m.id}.${m.ext}`" target="_blank">预览</a>
                <button class="btn danger" @click="removeItem(m.id)">删除</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </article>
  </section>
</template>

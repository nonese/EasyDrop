<script setup lang="ts">
import { ref } from 'vue'
import api from '@/api/client'
import type { PlaybackLog } from '@/types'

const deviceId = ref('')
const logs = ref<PlaybackLog[]>([])

const fetchLogs = async () => {
  if (!deviceId.value.trim()) return
  const { data } = await api.get<PlaybackLog[]>(`/api/logs/devices/${deviceId.value.trim()}?limit=100`)
  logs.value = data
}
</script>

<template>
  <article class="glass card">
    <h3>播放日志查询</h3>
    <div class="row-inline">
      <input class="input" v-model="deviceId" placeholder="输入完整 device_id" />
      <button class="btn" @click="fetchLogs">查询最近100条</button>
    </div>

    <div class="table-wrap" style="margin-top: 14px">
      <table class="table">
        <thead>
          <tr>
            <th>时间</th>
            <th>事件</th>
            <th>媒体</th>
            <th>任务</th>
            <th>详情</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="log in logs" :key="log.id">
            <td>{{ log.ts }}</td>
            <td>{{ log.event }}</td>
            <td>{{ log.media_id || '-' }}</td>
            <td>{{ log.campaign_id || '-' }}</td>
            <td>{{ log.detail_json || '-' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </article>
</template>

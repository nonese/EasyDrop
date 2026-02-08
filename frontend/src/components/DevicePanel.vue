<script setup lang="ts">
import { onMounted, ref } from 'vue'
import api from '@/api/client'
import type { DeviceItem } from '@/types'

const devices = ref<DeviceItem[]>([])

const fetchList = async () => {
  const { data } = await api.get<DeviceItem[]>('/api/devices')
  devices.value = data
}

const pullManifest = async (deviceId: string) => {
  const { data } = await api.get(`/api/devices/${deviceId}/manifest?since_version=0`)
  alert(JSON.stringify(data, null, 2))
}

onMounted(fetchList)
</script>

<template>
  <article class="glass card">
    <h3>设备列表</h3>
    <p class="muted">状态来自心跳与 WebSocket 在线检测</p>
    <div class="table-wrap">
      <table class="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>名称</th>
            <th>类型</th>
            <th>状态</th>
            <th>最近心跳</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="d in devices" :key="d.id">
            <td>{{ d.id.slice(0, 8) }}</td>
            <td>{{ d.name }}</td>
            <td>{{ d.type }}</td>
            <td><span class="chip" :class="d.status">{{ d.status }}</span></td>
            <td>{{ d.last_seen_at || '-' }}</td>
            <td><button class="btn" @click="pullManifest(d.id)">查看 Manifest</button></td>
          </tr>
        </tbody>
      </table>
    </div>
  </article>
</template>

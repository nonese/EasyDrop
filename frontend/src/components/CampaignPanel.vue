<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import api from '@/api/client'
import type { Campaign, DeviceItem, Playlist } from '@/types'

const campaigns = ref<Campaign[]>([])
const playlists = ref<Playlist[]>([])
const devices = ref<DeviceItem[]>([])
const page = ref(1)
const pageSize = 5

const form = ref({
  name: '',
  playlist_id: '',
  start_at: new Date().toISOString(),
  end_at: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString(),
  priority: 0,
  enabled: true,
})
const targetCampaign = ref('')
const selectedDeviceIds = ref<string[]>([])
const totalPages = computed(() => Math.max(1, Math.ceil(campaigns.value.length / pageSize)))
const pagedCampaigns = computed(() => {
  const start = (page.value - 1) * pageSize
  return campaigns.value.slice(start, start + pageSize)
})

const ensurePageInRange = () => {
  if (page.value > totalPages.value) page.value = totalPages.value
  if (page.value < 1) page.value = 1
}

const fetchData = async () => {
  const [cRes, pRes, dRes] = await Promise.all([
    api.get<Campaign[]>('/api/campaigns'),
    api.get<Playlist[]>('/api/playlists'),
    api.get<DeviceItem[]>('/api/devices'),
  ])
  campaigns.value = cRes.data
  playlists.value = pRes.data
  devices.value = dRes.data
  if (!form.value.playlist_id && playlists.value[0]) form.value.playlist_id = playlists.value[0].id
  if (!targetCampaign.value && campaigns.value[0]) targetCampaign.value = campaigns.value[0].id
  if (targetCampaign.value && !campaigns.value.find((c) => c.id === targetCampaign.value)) {
    targetCampaign.value = campaigns.value[0]?.id || ''
  }
  ensurePageInRange()
}

const createCampaign = async () => {
  await api.post('/api/campaigns', form.value)
  form.value.name = ''
  await fetchData()
}

const bindTargets = async () => {
  if (!targetCampaign.value || selectedDeviceIds.value.length === 0) return
  await api.post(`/api/campaigns/${targetCampaign.value}/targets`, { device_ids: selectedDeviceIds.value })
  await fetchData()
}

const deleteCampaign = async (campaign: Campaign) => {
  if (!confirm(`确认删除任务「${campaign.name}」吗？`)) return
  await api.delete(`/api/campaigns/${campaign.id}`)
  await fetchData()
}

onMounted(fetchData)
</script>

<template>
  <section class="grid-two">
    <article class="glass card">
      <h3>创建投放任务</h3>
      <div class="stack">
        <input class="input" v-model="form.name" placeholder="投放任务名称" />
        <select class="input" v-model="form.playlist_id">
          <option value="">选择播放单</option>
          <option v-for="p in playlists" :key="p.id" :value="p.id">{{ p.name }}</option>
        </select>
        <label>
          开始时间（ISO）
          <input class="input" v-model="form.start_at" />
        </label>
        <label>
          结束时间（ISO）
          <input class="input" v-model="form.end_at" />
        </label>
        <input class="input" type="number" v-model="form.priority" placeholder="优先级" />
        <label class="row-inline">
          <input type="checkbox" v-model="form.enabled" /> 启用
        </label>
        <button class="btn" @click="createCampaign">创建任务</button>
      </div>
    </article>

    <article class="glass card">
      <h3>任务绑定设备</h3>
      <div class="stack">
        <select class="input" v-model="targetCampaign">
          <option value="">选择任务</option>
          <option v-for="c in campaigns" :key="c.id" :value="c.id">{{ c.name }}</option>
        </select>
        <label v-for="d in devices" :key="d.id" class="row-inline">
          <input type="checkbox" :value="d.id" v-model="selectedDeviceIds" />
          {{ d.name }}（{{ d.type }} / {{ d.status }}）
        </label>
        <button class="btn" @click="bindTargets">绑定选中设备</button>
      </div>

      <h4>任务列表</h4>
      <ul class="plain-list">
        <li v-for="c in pagedCampaigns" :key="c.id" class="row-between">
          <span>{{ c.name }} - 优先级 {{ c.priority }} - 绑定 {{ c.targets.length }} 台设备</span>
          <button class="btn danger" @click="deleteCampaign(c)">删除</button>
        </li>
      </ul>
      <div class="row-inline" style="margin-top: 10px">
        <button class="btn ghost" :disabled="page <= 1" @click="page -= 1">上一页</button>
        <span>第 {{ page }} / {{ totalPages }} 页（共 {{ campaigns.length }} 条）</span>
        <button class="btn ghost" :disabled="page >= totalPages" @click="page += 1">下一页</button>
      </div>
    </article>
  </section>
</template>

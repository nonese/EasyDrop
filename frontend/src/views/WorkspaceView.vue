<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { getApiBaseUrl, setApiBaseUrl } from '@/api/baseUrl'
import MediaPanel from '@/components/MediaPanel.vue'
import DevicePanel from '@/components/DevicePanel.vue'
import PlaylistPanel from '@/components/PlaylistPanel.vue'
import CampaignPanel from '@/components/CampaignPanel.vue'
import LogsPanel from '@/components/LogsPanel.vue'

const tabs = [
  { key: 'media', label: '素材管理' },
  { key: 'devices', label: '设备管理' },
  { key: 'playlists', label: '播放单' },
  { key: 'campaigns', label: '投放任务' },
  { key: 'logs', label: '播放日志' },
] as const

type TabKey = (typeof tabs)[number]['key']
const active = ref<TabKey>('media')
const backendUrl = ref(getApiBaseUrl())
const auth = useAuthStore()
const router = useRouter()

const saveBackend = () => {
  if (!backendUrl.value.trim()) {
    alert('后端地址不能为空')
    return
  }
  setApiBaseUrl(backendUrl.value)
  backendUrl.value = getApiBaseUrl()
  alert(`后端地址已更新为：${backendUrl.value}`)
}

const logout = async () => {
  auth.logout()
  await router.push('/login')
}
</script>

<template>
  <div class="workspace-shell">
    <div class="aurora a1"></div>
    <div class="aurora a2"></div>
    <header class="glass topbar">
      <div>
        <h2>EasyDrop 投放控制台</h2>
        <p class="muted">当前角色：{{ auth.role }}</p>
      </div>
      <div class="row-inline">
        <input v-model="backendUrl" class="input compact" placeholder="后端地址" />
        <button class="btn ghost" @click="saveBackend">保存地址</button>
        <button class="btn ghost" @click="logout">退出登录</button>
      </div>
    </header>

    <nav class="glass tabs">
      <button
        v-for="item in tabs"
        :key="item.key"
        class="tab"
        :class="{ active: active === item.key }"
        @click="active = item.key"
      >
        {{ item.label }}
      </button>
    </nav>

    <section class="content">
      <MediaPanel v-if="active === 'media'" />
      <DevicePanel v-else-if="active === 'devices'" />
      <PlaylistPanel v-else-if="active === 'playlists'" />
      <CampaignPanel v-else-if="active === 'campaigns'" />
      <LogsPanel v-else />
    </section>
  </div>
</template>

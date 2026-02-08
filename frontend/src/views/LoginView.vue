<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { getApiBaseUrl, setApiBaseUrl } from '@/api/baseUrl'

const form = reactive({ username: 'admin', password: 'admin123' })
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
}

const submit = async () => {
  try {
    await auth.login(form.username, form.password)
    await router.push('/')
  } catch (err: any) {
    alert(err?.response?.data?.detail || '登录失败')
  }
}
</script>

<template>
  <main class="auth-shell">
    <div class="aurora a1"></div>
    <div class="aurora a2"></div>
    <section class="glass card auth-card">
      <h1>EasyDrop 管理后台</h1>
      <p class="muted">淡蓝毛玻璃主题 · 广告投放系统</p>
      <div class="row-inline">
        <input v-model="backendUrl" class="input compact" placeholder="后端地址，如 http://127.0.0.1:8000" />
        <button class="btn ghost" type="button" @click="saveBackend">保存后端地址</button>
      </div>
      <form @submit.prevent="submit" class="stack">
        <label>
          用户名
          <input v-model="form.username" class="input" placeholder="请输入用户名" />
        </label>
        <label>
          密码
          <input v-model="form.password" type="password" class="input" placeholder="请输入密码" />
        </label>
        <button class="btn" :disabled="auth.loading">{{ auth.loading ? '登录中...' : '登录' }}</button>
      </form>
    </section>
  </main>
</template>

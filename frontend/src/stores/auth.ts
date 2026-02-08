import { defineStore } from 'pinia'
import api from '@/api/client'

interface LoginResponse {
  access_token: string
  token_type: string
  role: string
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('admin_token') || '',
    role: localStorage.getItem('admin_role') || '',
    loading: false,
  }),
  getters: {
    isAuthed: (state) => Boolean(state.token),
  },
  actions: {
    async login(username: string, password: string) {
      this.loading = true
      try {
        const { data } = await api.post<LoginResponse>('/api/auth/login', { username, password })
        this.token = data.access_token
        this.role = data.role
        localStorage.setItem('admin_token', data.access_token)
        localStorage.setItem('admin_role', data.role)
      } finally {
        this.loading = false
      }
    },
    logout() {
      this.token = ''
      this.role = ''
      localStorage.removeItem('admin_token')
      localStorage.removeItem('admin_role')
    },
  },
})

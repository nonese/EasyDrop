const KEY = 'api_base_url'
const DEFAULT_BASE = (import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000').replace(/\/+$/, '')

export function getApiBaseUrl(): string {
  return (localStorage.getItem(KEY) || DEFAULT_BASE).replace(/\/+$/, '')
}

export function setApiBaseUrl(url: string): void {
  localStorage.setItem(KEY, (url || '').trim().replace(/\/+$/, ''))
}

export function getDefaultApiBaseUrl(): string {
  return DEFAULT_BASE
}

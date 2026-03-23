import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/api'

export const useUserStore = defineStore('user', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('token') || null)

  const isLoggedIn = computed(() => !!token.value)

  async function login(username, password) {
    const response = await api.post('/api/auth/login', { username, password })
    token.value = response.data.access_token
    user.value = response.data.user
    localStorage.setItem('token', token.value)
    api.setToken(token.value)
  }

  async function register(username, email, password) {
    await api.post('/api/auth/register', { username, email, password })
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
  }

  // Set token on API if already logged in
  if (token.value) {
    api.setToken(token.value)
  }

  return { user, token, isLoggedIn, login, register, logout }
})

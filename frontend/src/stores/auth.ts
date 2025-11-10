import { defineStore } from 'pinia'

type AuthState = {
  token: string | null
  role: string | null
  userId: number | null
  username: string | null
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    token: localStorage.getItem('token'),
    role: localStorage.getItem('role'),
    userId: localStorage.getItem('vp.userId') ? Number(localStorage.getItem('vp.userId')) : null,
    username: localStorage.getItem('vp.username'),
  }),
  getters: {
    isAuthenticated: (state): boolean => {
      return state.token !== null && state.role !== null
    },
    isAdmin: (state): boolean => {
      return state.role === 'admin'
    },
  },
  actions: {
    logoutLocal() {
      this.token = null
      this.role = null
      this.userId = null
      this.username = null
      localStorage.removeItem('token')
      localStorage.removeItem('role')
      localStorage.removeItem('vp.userId')
      localStorage.removeItem('vp.username')
    },
    setUserId(id: number | null) {
      this.userId = id
      if (id === null) {
        localStorage.removeItem('vp.userId')
      } else {
        localStorage.setItem('vp.userId', String(id))
      }
    },
    setUsername(username: string | null) {
      this.username = username
      if (username === null) {
        localStorage.removeItem('vp.username')
      } else {
        localStorage.setItem('vp.username', username)
      }
    },
  },
})



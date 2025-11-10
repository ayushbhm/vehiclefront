<script lang="ts">
import { defineComponent, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { authApi } from '../services/api'

export default defineComponent({
  name: 'Navbar',
  setup() {
    const auth = useAuthStore()
    const router = useRouter()
    const isAdmin = computed(() => auth.isAuthenticated && auth.isAdmin)
    const isUser = computed(() => auth.isAuthenticated && !auth.isAdmin)
    async function logout() {
      try {
        await authApi.logout()
      } catch {}
      auth.logoutLocal()
      router.replace({ name: 'login' })
    }
    return { auth, isAdmin, isUser, logout }
  },
})
</script>

<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container">
      <router-link class="navbar-brand" to="/">Vehicle Parking App - V2</router-link>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
        aria-controls="navbarNav"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0" v-if="isAdmin">
          <li class="nav-item"><router-link class="nav-link" to="/admin/dashboard">Dashboard</router-link></li>
          <li class="nav-item"><router-link class="nav-link" to="/admin/parking-lots">Parking Lots</router-link></li>
          <li class="nav-item"><router-link class="nav-link" to="/admin/users">Users</router-link></li>
          <li class="nav-item"><router-link class="nav-link" to="/admin/parking-status">Status</router-link></li>
          <li class="nav-item"><router-link class="nav-link" to="/admin/reports">Reports</router-link></li>
        </ul>
        <ul class="navbar-nav me-auto mb-2 mb-lg-0" v-else-if="isUser">
          <li class="nav-item"><router-link class="nav-link" to="/user/dashboard">Dashboard</router-link></li>
          <li class="nav-item"><router-link class="nav-link" to="/user/book">Book</router-link></li>
          <li class="nav-item"><router-link class="nav-link" to="/user/current-parking">Current</router-link></li>
          <li class="nav-item"><router-link class="nav-link" to="/user/history">History</router-link></li>
        </ul>
        <ul class="navbar-nav ms-auto">
          <template v-if="auth.isAuthenticated">
            <li class="nav-item">
              <button class="btn btn-outline-light btn-sm" @click="logout">Logout</button>
            </li>
          </template>
          <template v-else>
            <li class="nav-item"><router-link class="nav-link" to="/login">Login</router-link></li>
            <li class="nav-item"><router-link class="nav-link" to="/register">Register</router-link></li>
          </template>
        </ul>
      </div>
    </div>
  </nav>
</template>

<style scoped></style>



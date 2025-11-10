<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { authApi } from '../services/api'
import { useAuthStore } from '../stores/auth'
import { useNotifyStore } from '../stores/notify'

const username = ref('')
const password = ref('')
const loading = ref(false)
const router = useRouter()
const auth = useAuthStore()
const notify = useNotifyStore()

async function onSubmit() {
  loading.value = true
  try {
    const response = await authApi.login(username.value, password.value)
    // Update localStorage
    localStorage.setItem('token', response.access_token)
    localStorage.setItem('role', response.role)
    // Update store state
    auth.token = response.access_token
    auth.role = response.role
    auth.setUsername(username.value)
    // Set user_id from response
    if (response.user_id) {
      auth.setUserId(response.user_id)
    }
    notify.add('Logged in successfully', 'success')
    if (response.role === 'admin') {
      router.push('/admin/dashboard')
    } else {
      router.push('/user/dashboard')
    }
  } catch {
    notify.add('Login failed', 'danger')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="row justify-content-center">
    <div class="col-md-6">
      <div class="card">
        <div class="card-body">
          <h4 class="card-title mb-3">Login</h4>
          <form @submit.prevent="onSubmit">
            <div class="mb-3">
              <label class="form-label">Username</label>
              <input v-model="username" class="form-control" required />
            </div>
            <div class="mb-3">
              <label class="form-label">Password</label>
              <input v-model="password" type="password" class="form-control" required />
            </div>
            <button class="btn btn-primary" :disabled="loading">
              <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
              Login
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>



<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { authApi } from '../services/api'
import { useNotifyStore } from '../stores/notify'

const username = ref('')
const password = ref('')
const loading = ref(false)
const router = useRouter()
const notify = useNotifyStore()

async function onSubmit() {
  loading.value = true
  try {
    await authApi.register(username.value, password.value)
    notify.add('Registration successful. Please login.', 'success')
    router.replace({ name: 'login' })
  } catch {
    notify.add('Registration failed', 'danger')
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
          <h4 class="card-title mb-3">Register</h4>
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
              Register
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>



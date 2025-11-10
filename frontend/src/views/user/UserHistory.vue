<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useAuthStore } from '../../stores/auth'
import { userApi } from '../../services/api'
import { useNotifyStore } from '../../stores/notify'

const auth = useAuthStore()
const notify = useNotifyStore()
const reservations = ref<any[]>([])
const loading = ref(false)

async function load() {
  if (!auth.userId) return
  loading.value = true
  try {
    reservations.value = await userApi.listReservations(auth.userId)
  } catch {
    notify.add('Failed to load history', 'danger')
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>

<template>
  <div>
    <div class="d-flex align-items-center justify-content-between mb-3">
      <h3>History</h3>
      <div class="input-group" style="max-width: 260px">
        <span class="input-group-text">User ID</span>
        <input
          class="form-control"
          type="number"
          :value="auth.userId ?? ''"
          @input="auth.setUserId(($event.target as HTMLInputElement).value ? Number(($event.target as HTMLInputElement).value) : null)"
          placeholder="Set your numeric ID"
        />
        <button class="btn btn-outline-primary" @click="load">Load</button>
      </div>
    </div>
    <div v-if="!auth.userId" class="alert alert-info">
      Set your User ID to view your reservation history.
    </div>
    <div v-else>
      <div v-if="loading" class="text-muted">Loading...</div>
      <div v-else class="table-responsive">
        <table class="table table-striped">
          <thead>
            <tr>
              <th>ID</th>
              <th>Lot</th>
              <th>Spot</th>
              <th>Start</th>
              <th>End</th>
              <th>Cost</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="r in reservations" :key="r.id">
              <td>{{ r.id }}</td>
              <td>{{ r.lot_name }}</td>
              <td>{{ r.spot_id }}</td>
              <td>{{ r.parking_timestamp }}</td>
              <td>{{ r.leaving_timestamp || '-' }}</td>
              <td>{{ r.cost ?? 0 }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<style scoped></style>



<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
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
    notify.add('Failed to load reservations', 'danger')
  } finally {
    loading.value = false
  }
}

const activeCount = computed(
  () => reservations.value.filter((r) => !r.leaving_timestamp).length,
)
const historyCount = computed(
  () => reservations.value.filter((r) => !!r.leaving_timestamp).length,
)
const totalCost = computed(
  () =>
    reservations.value
      .filter((r) => !!r.leaving_timestamp)
      .reduce((s, r) => s + (r.cost || 0), 0),
)

onMounted(load)
</script>

<template>
  <div>
    <div class="d-flex align-items-center justify-content-between mb-3">
      <h3>User Dashboard</h3>
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

    <div class="row g-3">
      <div class="col-md-4">
        <div class="card text-bg-primary">
          <div class="card-body">
            <div class="d-flex justify-content-between">
              <div>
                <div class="h6">Active Parkings</div>
                <div class="display-6">{{ activeCount }}</div>
              </div>
              <i class="bi bi-car-front" style="font-size: 2rem"></i>
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card text-bg-success">
          <div class="card-body">
            <div class="h6">History Count</div>
            <div class="display-6">{{ historyCount }}</div>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card text-bg-dark">
          <div class="card-body">
            <div class="h6">Total Spent</div>
            <div class="display-6">₹{{ totalCost }}</div>
          </div>
        </div>
      </div>
    </div>

    <div class="mt-4">
      <h5>Recent Reservations</h5>
      <div v-if="loading" class="text-muted">Loading...</div>
      <div v-else>
        <div v-if="reservations.length === 0" class="text-muted">No reservations yet.</div>
        <div v-else class="table-responsive">
          <table class="table table-sm table-striped">
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
              <tr v-for="r in reservations.slice(0, 5)" :key="r.id">
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
  </div>
</template>

<style scoped></style>



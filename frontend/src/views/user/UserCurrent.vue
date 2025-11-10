<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { useAuthStore } from '../../stores/auth'
import { userApi } from '../../services/api'
import { useNotifyStore } from '../../stores/notify'

const auth = useAuthStore()
const notify = useNotifyStore()
const reservations = ref<any[]>([])
const loading = ref(false)
const actionLoading = ref<number | null>(null)

async function load() {
  if (!auth.userId) return
  loading.value = true
  try {
    reservations.value = await userApi.listReservations(auth.userId)
  } catch {
    notify.add('Failed to load active parking', 'danger')
  } finally {
    loading.value = false
  }
}
const active = computed(() => reservations.value.filter((r) => !r.leaving_timestamp))
async function release(resId: number) {
  actionLoading.value = resId
  try {
    await userApi.releaseReservation(resId)
    notify.add('Spot released', 'success')
    // redirect to history
    window.location.href = '/user/history'
  } finally {
    actionLoading.value = null
  }
  await load()
}
onMounted(load)
</script>

<template>
  <div>
    <div class="d-flex align-items-center justify-content-between mb-3">
      <h3>Current Parking</h3>
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
      Set your User ID to view and release active parking.
    </div>
    <div v-else>
      <div v-if="loading" class="text-muted">Loading...</div>
      <div v-else>
        <div v-if="active.length === 0" class="text-muted">No active parking.</div>
        <div v-else class="table-responsive">
          <table class="table table-striped">
            <thead>
              <tr>
                <th>ID</th>
                <th>Lot</th>
                <th>Spot</th>
                <th>Entry</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="r in active" :key="r.id">
                <td>{{ r.id }}</td>
                <td>{{ r.lot_name }}</td>
                <td>{{ r.spot_id }}</td>
                <td>{{ r.parking_timestamp }}</td>
                <td>
                  <button
                    class="btn btn-sm btn-danger"
                    @click="release(r.id)"
                    :disabled="actionLoading === r.id"
                  >
                    <span v-if="actionLoading === r.id" class="spinner-border spinner-border-sm me-2"></span>
                    Release
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>



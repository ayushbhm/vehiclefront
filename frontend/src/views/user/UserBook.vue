<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { lotsApi, userApi } from '../../services/api'
import { useNotifyStore } from '../../stores/notify'

const lots = ref<any[]>([])
const loading = ref(false)
const actionLoading = ref<number | null>(null)
const notify = useNotifyStore()

async function load() {
  loading.value = true
  try {
    lots.value = await lotsApi.listLots()
  } catch {
    notify.add('Failed to load lots', 'danger')
  } finally {
    loading.value = false
  }
}
async function book(lotId: number) {
  actionLoading.value = lotId
  try {
    await userApi.bookSpot(lotId)
    notify.add('Spot booked successfully', 'success')
    // redirect to current parking
    window.location.href = '/user/current-parking'
  } catch {
    notify.add('Booking failed', 'danger')
  } finally {
    actionLoading.value = null
  }
  await load()
}

onMounted(load)
</script>

<template>
  <div>
    <h3 class="mb-3">Book Parking</h3>
    <div v-if="loading" class="text-muted">Loading...</div>
    <div v-else class="row g-3">
      <div class="col-md-6" v-for="lot in lots" :key="lot.id">
        <div class="card h-100">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-start">
              <div>
                <h5 class="card-title">{{ lot.name }}</h5>
                <div class="text-muted">{{ lot.address }} ({{ lot.pincode }})</div>
              </div>
              <span class="badge text-bg-primary">₹ {{ lot.price }}</span>
            </div>
            <div class="mt-3">
              <span class="badge text-bg-success me-2">Available: {{ lot.available }}</span>
              <span class="badge text-bg-danger">Occupied: {{ lot.occupied }}</span>
            </div>
          </div>
          <div class="card-footer bg-transparent border-0">
            <button
              class="btn btn-primary w-100"
              :disabled="lot.available === 0 || actionLoading === lot.id"
              @click="book(lot.id)"
            >
              <span v-if="actionLoading === lot.id" class="spinner-border spinner-border-sm me-2"></span>
              Book First Available Spot
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>



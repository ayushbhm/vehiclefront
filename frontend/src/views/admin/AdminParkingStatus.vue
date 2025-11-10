<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { lotsApi } from '../../services/api'
import { useNotifyStore } from '../../stores/notify'

const notify = useNotifyStore()

const lots = ref<any[]>([])
const selectedLotId = ref<number | null>(null)
const selectedLot = ref<any | null>(null)
const loading = ref(false)

async function loadLots() {
  lots.value = await lotsApi.listLots()
  if (lots.value.length > 0) {
    selectedLotId.value = lots.value[0].id
    await loadLotDetail()
  }
}
async function loadLotDetail() {
  if (!selectedLotId.value) return
  loading.value = true
  try {
    selectedLot.value = await lotsApi.getLot(selectedLotId.value)
  } catch {
    notify.add('Failed to load lot detail', 'danger')
  } finally {
    loading.value = false
  }
}

onMounted(loadLots)
</script>

<template>
  <div>
    <h3 class="mb-3">Parking Status</h3>
    <div class="row g-3 align-items-end">
      <div class="col-md-4">
        <label class="form-label">Select Lot</label>
        <select class="form-select" v-model.number="selectedLotId" @change="loadLotDetail">
          <option v-for="l in lots" :key="l.id" :value="l.id">{{ l.name }}</option>
        </select>
      </div>
    </div>

    <div class="mt-4">
      <div v-if="loading" class="text-muted">Loading...</div>
      <div v-else-if="selectedLot">
        <div class="row g-2">
          <div class="col-6 col-sm-4 col-md-3 col-lg-2" v-for="s in selectedLot.spots" :key="s.id">
            <div
              class="p-3 text-center rounded"
              :class="s.status === 'A' ? 'bg-success-subtle border border-success' : 'bg-danger-subtle border border-danger'"
            >
              <div class="fw-semibold">Spot {{ s.id }}</div>
              <div class="small">{{ s.status === 'A' ? 'Available' : 'Occupied' }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>



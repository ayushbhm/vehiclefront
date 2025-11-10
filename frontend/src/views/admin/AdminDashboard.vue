<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { lotsApi } from '../../services/api'
import { useNotifyStore } from '../../stores/notify'
import SimplePieChart from '../../components/charts/SimplePieChart.vue'

const lots = ref<any[]>([])
const loading = ref(false)
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
const totalSpots = computed(() =>
  lots.value.reduce((s, l) => s + (l.total_spots || 0), 0),
)
const occupied = computed(() =>
  lots.value.reduce((s, l) => s + (l.occupied || 0), 0),
)
const available = computed(() =>
  lots.value.reduce((s, l) => s + (l.available || 0), 0),
)

onMounted(load)
</script>

<template>
  <div>
    <h3 class="mb-3">Admin Dashboard</h3>
    <div v-if="loading" class="text-muted">Loading...</div>
    <div v-else>
      <div class="row g-3">
        <div class="col-md-4">
          <div class="card">
            <div class="card-body">
              <div class="h6">Total Spots</div>
              <div class="display-6">{{ totalSpots }}</div>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card">
            <div class="card-body">
              <div class="h6">Occupied</div>
              <div class="display-6 text-danger">{{ occupied }}</div>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card">
            <div class="card-body">
              <div class="h6">Available</div>
              <div class="display-6 text-success">{{ available }}</div>
            </div>
          </div>
        </div>
      </div>
      <div class="row mt-4">
        <div class="col-12">
          <div class="card">
            <div class="card-body">
              <div class="h6 mb-3">Occupancy Summary</div>
              <div style="height: 300px">
                <SimplePieChart :labels="['Available', 'Occupied']" :data="[available, occupied]" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>



<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { lotsApi } from '../../services/api'
import { useNotifyStore } from '../../stores/notify'
import SimpleBarChart from '../../components/charts/SimpleBarChart.vue'
import SimplePieChart from '../../components/charts/SimplePieChart.vue'

const notify = useNotifyStore()

const lots = ref<any[]>([])
const loading = ref(false)

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

onMounted(load)
</script>

<template>
  <div>
    <h3 class="mb-3">Reports</h3>
    <div v-if="loading" class="text-muted">Loading...</div>
    <div v-else>
      <div class="row g-3">
        <div class="col-md-6">
          <div class="card">
            <div class="card-body">
              <div class="h6 mb-3">Occupancy by Lot</div>
              <div style="height: 300px">
                <SimpleBarChart
                  :labels="lots.map(l => l.name)"
                  :data="lots.map(l => l.occupied)"
                  title="Occupied"
                />
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card">
            <div class="card-body">
              <div class="h6 mb-3">Availability by Lot</div>
              <div style="height: 300px">
                <SimpleBarChart
                  :labels="lots.map(l => l.name)"
                  :data="lots.map(l => l.available)"
                  title="Available"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="row g-3 mt-1">
        <div class="col-12">
          <div class="card">
            <div class="card-body">
              <div class="h6 mb-3">Overall Split</div>
              <div style="height: 300px">
                <SimplePieChart
                  :labels="['Total Available', 'Total Occupied']"
                  :data="[
                    lots.reduce((s,l)=>s+ (l.available||0),0),
                    lots.reduce((s,l)=>s+ (l.occupied||0),0)
                  ]"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>



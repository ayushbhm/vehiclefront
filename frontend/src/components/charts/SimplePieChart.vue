<script setup lang="ts">
import { Pie } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from 'chart.js'
import { computed } from 'vue'

ChartJS.register(Title, Tooltip, Legend, ArcElement)

const props = defineProps<{
  labels: string[]
  data: number[]
}>()

const chartData = computed(() => ({
  labels: props.labels,
  datasets: [
    {
      backgroundColor: ['#198754', '#dc3545', '#0d6efd', '#ffc107'],
      data: props.data,
    },
  ],
}))
</script>

<template>
  <Pie :data="chartData" :options="{ responsive: true, maintainAspectRatio: false }" />
</template>

<style scoped>
div {
  height: 280px;
}
</style>



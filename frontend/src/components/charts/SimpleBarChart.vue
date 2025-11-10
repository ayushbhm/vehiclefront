<script setup lang="ts">
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
} from 'chart.js'
import { computed } from 'vue'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const props = defineProps<{
  labels: string[]
  data: number[]
  title?: string
}>()

const chartData = computed(() => ({
  labels: props.labels,
  datasets: [
    {
      label: props.title || 'Data',
      backgroundColor: '#0d6efd',
      data: props.data,
    },
  ],
}))
</script>

<template>
  <Bar :data="chartData" :options="{ responsive: true, maintainAspectRatio: false }" />
</template>

<style scoped>
div {
  height: 280px;
}
</style>



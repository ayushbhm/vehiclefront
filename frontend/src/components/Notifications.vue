<script lang="ts">
import { defineComponent } from 'vue'
import { useNotifyStore } from '../stores/notify'

export default defineComponent({
  name: 'Notifications',
  setup() {
    const notify = useNotifyStore()
    return { notify }
  },
})
</script>

<template>
  <div aria-live="polite" aria-atomic="true">
    <div class="position-fixed top-0 end-0 p-3" style="z-index: 1080">
      <div v-for="n in notify.items" :key="n.id" class="alert alert-dismissible fade show" :class="`alert-${n.variant}`" role="alert">
        {{ n.message }}
        <button type="button" class="btn-close" aria-label="Close" @click="notify.remove(n.id)"></button>
      </div>
    </div>
  </div>
</template>

<style scoped></style>



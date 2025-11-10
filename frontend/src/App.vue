<script setup lang="ts">
import Notifications from './components/Notifications.vue'
import Navbar from './components/Navbar.vue'
import { useRoute } from 'vue-router'
import { computed } from 'vue'
const route = useRoute()
const showTopNav = computed(() => !route.path.startsWith('/admin'))
</script>

<template>
  <div>
    <Navbar v-if="showTopNav" />
    <main class="py-4">
      <div class="container">
        <Notifications />
        <router-view />
      </div>
    </main>
  </div>
</template>

<style scoped></style>

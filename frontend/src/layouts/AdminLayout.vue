<script setup lang="ts">
import { RouterView } from 'vue-router'
</script>

<template>
  <div class="container-fluid">
    <div class="row">
      <aside class="col-md-3 col-lg-2 d-md-block bg-light sidebar collapse show min-vh-100">
        <div class="position-sticky pt-3">
          <ul class="nav flex-column">
            <li class="nav-item"><router-link class="nav-link" to="/admin/dashboard">Dashboard</router-link></li>
            <li class="nav-item"><router-link class="nav-link" to="/admin/parking-lots">Parking Lots</router-link></li>
            <li class="nav-item"><router-link class="nav-link" to="/admin/parking-status">Parking Status</router-link></li>
            <li class="nav-item"><router-link class="nav-link" to="/admin/users">Users</router-link></li>
            <li class="nav-item"><router-link class="nav-link" to="/admin/reports">Reports</router-link></li>
          </ul>
        </div>
      </aside>
      <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4 py-3">
        <RouterView />
      </main>
    </div>
  </div>
</template>

<style scoped></style>



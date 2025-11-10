<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { lotsApi, adminLotsForms } from '../../services/api'
import { useNotifyStore } from '../../stores/notify'

const notify = useNotifyStore()

const lots = ref<any[]>([])
const loading = ref(false)
const creating = ref(false)
const editingId = ref<number | null>(null)
const deletingId = ref<number | null>(null)

const form = reactive({
  name: '',
  price: 0,
  address: '',
  pincode: '',
  max_spots: 0,
})

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

function startCreate() {
  creating.value = true
  Object.assign(form, { name: '', price: 0, address: '', pincode: '', max_spots: 0 })
}

async function submitCreate() {
  try {
    await adminLotsForms.create(form)
    notify.add('Lot created', 'success')
    creating.value = false
    await load()
  } catch {
    notify.add('Create failed', 'danger')
  }
}

function startEdit(l: any) {
  editingId.value = l.id
  Object.assign(form, {
    name: l.name,
    price: l.price,
    address: l.address,
    pincode: l.pincode,
    max_spots: l.total_spots,
  })
}
async function submitEdit() {
  if (!editingId.value) return
  try {
    await adminLotsForms.update(editingId.value, form)
    notify.add('Lot updated', 'success')
    editingId.value = null
    await load()
  } catch {
    notify.add('Update failed', 'danger')
  }
}

async function del(lotId: number) {
  deletingId.value = lotId
  try {
    await adminLotsForms.remove(lotId)
    notify.add('Lot deleted', 'success')
    await load()
  } catch {
    notify.add('Delete failed. Ensure all spots are empty.', 'danger')
  } finally {
    deletingId.value = null
  }
}

onMounted(load)
</script>

<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h3>Parking Lots</h3>
      <button class="btn btn-primary" @click="startCreate">Create Lot</button>
    </div>
    <div v-if="loading" class="text-muted">Loading...</div>
    <div v-else class="table-responsive">
      <table class="table table-striped">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Price</th>
            <th>Address</th>
            <th>Pincode</th>
            <th>Total</th>
            <th>Occupied</th>
            <th>Available</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="l in lots" :key="l.id">
            <td>{{ l.id }}</td>
            <td>{{ l.name }}</td>
            <td>{{ l.price }}</td>
            <td>{{ l.address }}</td>
            <td>{{ l.pincode }}</td>
            <td>{{ l.total_spots }}</td>
            <td>{{ l.occupied }}</td>
            <td>{{ l.available }}</td>
            <td class="text-end">
              <button class="btn btn-sm btn-outline-secondary me-2" @click="startEdit(l)">Edit</button>
              <button class="btn btn-sm btn-outline-danger" :disabled="deletingId===l.id" @click="del(l.id)">
                <span v-if="deletingId===l.id" class="spinner-border spinner-border-sm me-1"></span>
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Create Modal (simple inline section) -->
    <div v-if="creating || editingId" class="card mt-4">
      <div class="card-body">
        <h5 class="card-title">{{ editingId ? 'Edit Lot' : 'Create Lot' }}</h5>
        <div class="row g-3">
          <div class="col-md-6">
            <label class="form-label">Name</label>
            <input v-model="form.name" class="form-control" />
          </div>
          <div class="col-md-6">
            <label class="form-label">Price</label>
            <input v-model.number="form.price" type="number" step="0.01" class="form-control" />
          </div>
          <div class="col-md-6">
            <label class="form-label">Address</label>
            <input v-model="form.address" class="form-control" />
          </div>
          <div class="col-md-6">
            <label class="form-label">Pincode</label>
            <input v-model="form.pincode" class="form-control" />
          </div>
          <div class="col-md-6">
            <label class="form-label">Max Spots</label>
            <input v-model.number="form.max_spots" type="number" class="form-control" />
          </div>
        </div>
        <div class="mt-3">
          <button v-if="!editingId" class="btn btn-primary me-2" @click="submitCreate">Create</button>
          <button v-else class="btn btn-primary me-2" @click="submitEdit">Save</button>
          <button class="btn btn-outline-secondary" @click="creating=false; editingId=null">Cancel</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>



import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import { attachResponseInterceptors, registerAuthResolver } from './services/api'
import { useNotifyStore } from './stores/notify'
import { useAuthStore } from './stores/auth'

const app = createApp(App)

const pinia = createPinia()
app.use(pinia)
app.use(router)

// Register one global Axios interceptor to surface errors
// after Pinia is active so the store can be used.
const notify = useNotifyStore()
const auth = useAuthStore()

registerAuthResolver(() => ({
  role: auth.role,
  userId: auth.userId,
  username: auth.username,
  token: auth.token,
}))

attachResponseInterceptors((message) => {
  notify.add(message, 'danger')
})

app.mount('#app')

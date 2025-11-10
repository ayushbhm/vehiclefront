import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import AdminLayout from '../layouts/AdminLayout.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: () => import('../views/Landing.vue') },
    { path: '/login', name: 'login', component: () => import('../views/Login.vue') },
    { path: '/register', name: 'register', component: () => import('../views/Register.vue') },
    // User
    { path: '/user/dashboard', name: 'user-dashboard', component: () => import('../views/user/UserDashboard.vue'), meta: { requiresAuth: true, role: 'user' } },
    { path: '/user/book', name: 'user-book', component: () => import('../views/user/UserBook.vue'), meta: { requiresAuth: true, role: 'user' } },
    { path: '/user/current-parking', name: 'user-current', component: () => import('../views/user/UserCurrent.vue'), meta: { requiresAuth: true, role: 'user' } },
    { path: '/user/history', name: 'user-history', component: () => import('../views/user/UserHistory.vue'), meta: { requiresAuth: true, role: 'user' } },
    // Admin with sidebar layout
    {
      path: '/admin',
      component: AdminLayout,
      meta: { requiresAuth: true, role: 'admin' },
      children: [
        { path: 'dashboard', name: 'admin-dashboard', component: () => import('../views/admin/AdminDashboard.vue') },
        { path: 'parking-lots', name: 'admin-lots', component: () => import('../views/admin/AdminLots.vue') },
        { path: 'users', name: 'admin-users', component: () => import('../views/admin/AdminUsers.vue') },
        { path: 'parking-status', name: 'admin-status', component: () => import('../views/admin/AdminParkingStatus.vue') },
        { path: 'reports', name: 'admin-reports', component: () => import('../views/admin/AdminReports.vue') },
      ],
    },
    { path: '/:pathMatch(.*)*', name: 'not-found', component: () => import('../views/NotFound.vue') },
  ],
})

router.beforeEach((to) => {
  const auth = useAuthStore()
  if (to.meta?.requiresAuth) {
    if (!auth.isAuthenticated) {
      return { name: 'login' }
    }
    if (to.meta?.role === 'admin' && !auth.isAdmin) {
      return { name: 'user-dashboard' }
    }
    if (to.meta?.role === 'user' && auth.isAdmin) {
      return { name: 'admin-dashboard' }
    }
  }
  return true
})

export default router

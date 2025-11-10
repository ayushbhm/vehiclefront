import axios, { type InternalAxiosRequestConfig } from 'axios'
import type { AxiosRequestHeaders } from 'axios'

type AuthSnapshot = {
  role: string | null
  userId: number | null
  username: string | null
  token: string | null
}

let authResolver: (() => AuthSnapshot | null | undefined) | null = null

// Axios instance with session cookies for Flask-Login
export const apiClient = axios.create({
  baseURL: '/',
  withCredentials: true,
})

function ensureHeadersObject(headers?: AxiosRequestHeaders | (Partial<AxiosRequestHeaders> & Record<string, unknown>)) {
  if (!headers) {
    return {} as AxiosRequestHeaders & Record<string, unknown>
  }
  if (typeof (headers as any).set === 'function') {
    return headers
  }
  return { ...(headers as Record<string, unknown>) } as AxiosRequestHeaders & Record<string, unknown>
}

apiClient.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  const resolver = authResolver
  if (resolver) {
    const snapshot = resolver()
    if (snapshot && snapshot.token && snapshot.role) {
      const headers = (config.headers = ensureHeadersObject(config.headers))
      const role = snapshot.role
      
      // Add Authorization header with token
      if (typeof (headers as any).set === 'function') {
        ;(headers as any).set('Authorization', `Bearer ${snapshot.token}`)
        ;(headers as any).set('X-Client-Role', role)
        if (snapshot.userId !== null && snapshot.userId !== undefined) {
          ;(headers as any).set('X-Client-UserId', String(snapshot.userId))
        } else {
          ;(headers as any).delete?.('X-Client-UserId')
        }
        if (snapshot.username) {
          ;(headers as any).set('X-Client-Username', snapshot.username)
        } else {
          ;(headers as any).delete?.('X-Client-Username')
        }
      } else {
        ;(headers as any)['Authorization'] = `Bearer ${snapshot.token}`
        ;(headers as any)['X-Client-Role'] = role
        if (snapshot.userId !== null && snapshot.userId !== undefined) {
          ;(headers as any)['X-Client-UserId'] = String(snapshot.userId)
        } else {
          delete (headers as any)['X-Client-UserId']
        }
        if (snapshot.username) {
          ;(headers as any)['X-Client-Username'] = snapshot.username
        } else {
          delete (headers as any)['X-Client-Username']
        }
      }
    }
  }
  return config
})

export function registerAuthResolver(resolver: () => AuthSnapshot | null | undefined) {
  authResolver = resolver
}

// Helper to send application/x-www-form-urlencoded for Flask form endpoints
function toFormUrlEncoded(payload: Record<string, string | number>): string {
  const params = new URLSearchParams()
  Object.entries(payload).forEach(([k, v]) => params.append(k, String(v)))
  return params.toString()
}

// Global error handling can be attached by the app (e.g., toasts)
export function attachResponseInterceptors(
  onError: (message: string, status?: number) => void,
) {
  apiClient.interceptors.response.use(
    (r) => r,
    (error) => {
      const status = error?.response?.status
      const message =
        error?.response?.data?.error ||
        error?.response?.data?.message ||
        error?.message ||
        'Request failed'
      onError(message, status)
      if (status === 401 || status === 403) {
        // let router guards handle redirection; no-op here
      }
      return Promise.reject(error)
    },
  )
}

// Auth & Session
export const authApi = {
  async login(username: string, password: string) {
    const { data } = await apiClient.post<{ access_token: string; role: string; user_id: number }>(
      '/login',
      { username, password },
      {
        headers: { 'Content-Type': 'application/json' },
      },
    )
    return data
  },
  async register(username: string, password: string) {
    return apiClient.post(
      '/register',
      toFormUrlEncoded({ username, password }),
      {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      },
    )
  },
  async logout() {
    return apiClient.get('/logout')
  },
}

// Public APIs
export const lotsApi = {
  async listLots() {
    // GET /api/lots -> [{ id, name, price, address, pincode, total_spots, occupied, available }]
    const { data } = await apiClient.get('/api/lots')
    return data
  },
  async getLot(lotId: number) {
    // GET /api/lots/:id -> { id, name, price, address, pincode, total_spots, spots: [{id,status}] }
    const { data } = await apiClient.get(`/api/lots/${lotId}`)
    return data
  },
}

// Admin-only helper APIs
export const adminLotsForms = {
  async create(payload: {
    name: string
    price: number
    address: string
    pincode: string
    max_spots: number
  }) {
    const { data } = await apiClient.post(
      '/admin/lots/create',
      payload,
      { headers: { 'Content-Type': 'application/json', 'X-Requested-With': 'XMLHttpRequest' } },
    )
    return data
  },
  async update(
    lotId: number,
    payload: {
      name: string
      price: number
      address: string
      pincode: string
      max_spots: number
    },
  ) {
    const { data } = await apiClient.post(
      `/admin/lots/edit/${lotId}`,
      payload,
      { headers: { 'Content-Type': 'application/json', 'X-Requested-With': 'XMLHttpRequest' } },
    )
    return data
  },
  async remove(lotId: number) {
    const { data } = await apiClient.post(
      `/admin/lots/delete/${lotId}`,
      {},
      { headers: { 'Content-Type': 'application/json', 'X-Requested-With': 'XMLHttpRequest' } },
    )
    return data
  },
}

// User actions
export const userApi = {
  // There is no /api/me; caller should pass known userId when needed.
  async listReservations(userId: number) {
    const { data } = await apiClient.get(`/api/user/${userId}/reservations`)
    return data
  },
  async bookSpot(lotId: number) {
    const { data } = await apiClient.post(
      `/user/book/${lotId}`,
      {},
      { headers: { 'Content-Type': 'application/json', 'X-Requested-With': 'XMLHttpRequest' } },
    )
    return data
  },
  async releaseReservation(reservationId: number) {
    const { data } = await apiClient.post(
      `/user/release/${reservationId}`,
      {},
      { headers: { 'Content-Type': 'application/json', 'X-Requested-With': 'XMLHttpRequest' } },
    )
    return data
  },
}



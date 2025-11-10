import { defineStore } from 'pinia'

export type NotifyItem = {
  id: number
  message: string
  variant: 'success' | 'danger' | 'warning' | 'info'
}

let nextId = 1

export const useNotifyStore = defineStore('notify', {
  state: () => ({
    items: [] as NotifyItem[],
  }),
  actions: {
    add(message: string, variant: NotifyItem['variant'] = 'info', timeoutMs = 3000) {
      const id = nextId++
      this.items.push({ id, message, variant })
      if (timeoutMs > 0) {
        setTimeout(() => this.remove(id), timeoutMs)
      }
    },
    remove(id: number) {
      this.items = this.items.filter((n) => n.id !== id)
    },
    clear() {
      this.items = []
    },
  },
})



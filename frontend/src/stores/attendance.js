import { defineStore } from 'pinia'
import attendanceService from '@/services/attendanceService'

export const useAttendanceStore = defineStore('attendance', {
  state: () => ({
    sessions: [],
    attendance: [],
    loading: false,
    error: null
  }),

  actions: {
    async fetchSessions() {
      this.loading = true
      try {
        const response = await attendanceService.getSessions()
        this.sessions = response.data.results || response.data
      } catch (err) {
        this.error = err
      } finally {
        this.loading = false
      }
    },

    async fetchAttendanceBySession(sessionId) {
      this.loading = true
      try {
        const response = await attendanceService.getAttendanceBySession(sessionId)
        this.attendance = response.data.results || response.data
      } catch (err) {
        this.error = err
      } finally {
        this.loading = false
      }
    },

    async bulkSubmit(payload) {
      const response = await attendanceService.bulkCreate(payload)
      return response.data
    }
  }
})
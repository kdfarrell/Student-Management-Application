import { scheduleService } from '@/services/scheduleService'
import { defineStore } from 'pinia'


export const useScheduleStore = defineStore('schedule', {

	state: () => ({
		schedules: [],
		count: 0,
		pageSize: 10,
		currentPage: 1,
		loading: false,
		error: null,
	}),

	actions: {

		async fetchSchedules(params = {}) {
			this.loading = true
			this.error = null

			try {
				const queryParams = (params.date_from && params.date_to)
					? { ...params }
					: { page: this.currentPage, ...params }

				const response = await scheduleService.getSchedules(queryParams)
				this.schedules = response.data.results || []
				this.count = response.data.count || 0
			}
			catch (error) {
				this.error = error.message
			}
			finally {
				this.loading = false
			}
		},

		async goToPage(page) {
			this.currentPage = page
			await this.fetchSchedules()
		},

		async fetchSchedule(id) {
			const response = await scheduleService.getSchedule(id)
			return response.data
		},

		async createSchedule(data) {
			const response = await scheduleService.createSchedule(data)
			this.schedules.push(response.data)
			return response.data
		},

		async updateSchedule(id, data) {
			const response = await scheduleService.updateSchedule(id, data)
			const index = this.schedules.findIndex(s => s.id === id)

			if (index !== -1) {
				this.schedules[index] = response.data
			}

			return response.data
		},

		async deleteSchedule(id) {
			await scheduleService.deleteSchedule(id)
			this.schedules = this.schedules.filter(s => s.id != id)
		}
	}
})
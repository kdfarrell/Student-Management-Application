import { defineStore } from 'pinia'
import { auditService } from '../services/auditService'

export const useAuditStore = defineStore('audit', {

	state: () => ({
		audits: [],
		count: 0,
		pageSize: 10,
		currentPage: 1,
		loading: false,
		error: null,
		filters: {
			action: '',
			target_model: '',
			search: '',
			date_from: '',
			date_to: '',
		},
	}),

	actions: {

		async fetchAudits(params = {}) {
			this.loading = true
			this.error = null
			try {
				const query = {
					page: this.currentPage,
					...this.filters,
					...params,
				}
				Object.keys(query).forEach((key) => {
					if (query[key] === '' || query[key] == null) {
						delete query[key]
					}
				})
				const response = await auditService.getAudits(query)
				this.audits = response.data.results
				this.count = response.data.count
				this.pageSize = response.data.page_size || 10
			} catch (error) {
				this.error = error.message
			} finally {
				this.loading = false
			}
		},

		async goToPage(page) {
			if (page === this.currentPage) return
			this.currentPage = page
			await this.fetchAudits()
		},

		async applyFilters(filters = {}) {
			this.filters = { ...this.filters, ...filters }
			this.currentPage = 1
			await this.fetchAudits()
		},

		async clearFilters() {
			this.filters = {
				action: '',
				target_model: '',
				search: '',
				date_from: '',
				date_to: '',
			}
			this.currentPage = 1
			await this.fetchAudits()
		},

		async fetchAudit(id) {
			const response = await auditService.getAudit(id)
			return response.data
		},

	},

})
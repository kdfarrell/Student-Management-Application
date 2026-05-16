import dashboardService from '@/services/dashboardService'
import { defineStore } from 'pinia'

export const useDashboardStore = defineStore('dashboard', {
	state: () => ({
		stats: null,
		atRiskList: [],
		gradeRanges: null,
		attendanceOverview: [],
		loading: false,
		error: null,
	}),

	actions: {
		async fetchDashboard() {
			this.loading = true
			this.error = null
			try {
				const response = await dashboardService.getDashboard()
				const data = response.data
				this.stats = {
					total_students: data.total_students,
					total_courses: data.total_courses,
					sessions_this_week: data.sessions_this_week,
					at_risk_count: data.at_risk_count,
				}
				this.atRiskList = data.at_risk_list
				this.gradeRanges = data.grade_ranges
				this.attendanceOverview = data.attendace_overview_list
			}
			catch (err) {
				this.error = err.response?.data?.detail || 'Failed to load dashboard data'
			}
			finally {
				this.loading = false
			}
		},
	},
})
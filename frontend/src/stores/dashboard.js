import { defineStore } from 'pinia'
import dashboardService from '@/services/dashboardService'

export const useDashboardStore = defineStore('dashboard', {
  state: () => ({
    stats: null,
    atRiskList: [],
    gradeRanges: null,
    attendanceOverview: [],
    // ✨ Added state property to track assessment types count
    assessmentDistribution: null, 
    recentActivity: [],
    loading: false,
    error: null,
  }),

  getters: {
    // You can add tracking getters here if needed down the line
  },

  actions: {
    async fetchDashboard() {
      this.loading = true
      this.error = null
      try {
        const response = await dashboardService.getDashboard()
        const data = response.data

        // Unpack global numeric stats
        this.stats = {
          total_students: data.total_students,
          total_courses: data.total_courses,
          sessions_this_week: data.sessions_this_week,
          at_risk_count: data.at_risk_count,
        }

        // Unpack list and chart objects safely matching backend key names
        this.atRiskList = data.at_risk_list || []
        this.gradeRanges = data.grade_ranges || null
        this.attendanceOverview = data.attendance_overview_list || []
        
        // ✨ Map the new backend data to your local store state
        this.assessmentDistribution = data.assessment_distribution || null
        
        // Fallback placeholder block if your backend doesn't serve activity items yet
        this.recentActivity = data.recent_activity || [
          { detail: 'Grade report generated for Course', timestamp: 'Just now' },
          { detail: 'Attendance roster updated for morning sessions', timestamp: '2 hours ago' }
        ]

      } catch (err) {
        console.error('Error fetching dashboard details:', err)
        this.error = 'Failed to load dashboard data. Please try again later.'
      } finally {
        this.loading = false
      }
    },
  },
})
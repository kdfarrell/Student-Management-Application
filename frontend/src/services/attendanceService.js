import api from './api'

export default {
	getSessions() {
		return api.get('/sessions/')
	},
	getAttendanceBySession(sessionId) {
		return api.get(`/attendance/?session=${sessionId}`)
	},
	bulkCreate(payload) {
		return api.post('/attendance/bulk-create/', payload)
	},
	getAttendanceSummary(studentId) {
		return api.get(`/students/${studentId}/attendance-summary/`)
	}
}
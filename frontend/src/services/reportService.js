import api from './api'

export const reportService = {
	getGradeReport(studentId, courseId) {
		return api.get('reports/grade/', {
			params: { student_id: studentId, course_id: courseId },
			responseType: 'blob',
		})
	},

	getAttendanceReport(studentId) {
		return api.get('reports/attendance/', {
			params: { student_id: studentId },
			responseType: 'blob',
		})
	},

	getCourseGradeReport(courseId) {
		return api.get('reports/course-grade/', {
			params: { course_id: courseId },
			responseType: 'blob',
		})
	},

	sendEmailReport(payload) {
		return api.post('reports/email/', payload)
	}
}
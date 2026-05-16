import api from './api'

export const courseService = {

	// Courses

	getCourses(params = {}) {
		return api.get('courses/', { params })
	},

	getCourse(id) {
		return api.get(`courses/${id}`)
	},

	createCourse(data) {
		return api.post('courses/', data)
	},

	updateCourse(id, data) {
		return api.put(`courses/${id}/`, data)
	},

	deleteCourse(id) {
		return api.delete(`courses/${id}/`)
	},


	// Subjects

	getSubjects(params = {}) {
		return api.get('subjects/', { params })
	},

	getSubject(id) {
		return api.get(`subject/${id}/`)
	},

	createSubject(data) {
		return api.post('subjects/', data)
	},

	updateSubject(id, data) {
		return api.put(`subjects/${id}/`, data)
	},

	deleteSubject(id) {
		return api.delete(`subjects/${id}/`)
	},


	// Enrollments

	getEnrollments(params = {}) {
		return api.get('enrollment/', { params })
	},

	getEnrollment(id) {
		return api.get(`enrollment/${id}/`)
	},

	createEnrollment(data) {
		return api.post('enrollment/', data)
	},

	updateEnrollment(id, data) {
		return api.patch(`enrollment/${id}/`, data)
	},

	deleteEnrollment(id) {
		return api.delete(`enrollment/${id}/`)
	}
}
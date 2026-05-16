import { courseService } from '@/services/courseService'
import { defineStore } from 'pinia'

export const useCourseStore = defineStore('courses', {

	state: () => ({
		courses: [],
		coursesCount: 0,

		subjects: [],
		subjectsCount: 0,

		enrollments: [],
		enrollmentsCount: 0,

		pageSize: 10,
		currentPage: 1,
		loading: false,
		error: null
	}),

	actions: {

		async fetchCourses(params = {}) {
			this.loading = true
			this.error = null

			try {
				const response = await courseService.getCourses({ page: this.currentPage, ...params })
				this.courses = [...response.data.results]
				this.coursesCount = response.data.coursesCount
				this.pageSize = response.data.page_size
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
			await this.fetchCourses()
		},

		async fetchCourse(id) {
			const response = await courseService.getCourse(id)
			return response.data
		},

		async createCourse(data) {
			const response = await courseService.createCourse(data)
			this.courses.push(response.data)
			return response.data
		},

		async updateCourse(id, data) {
			const response = await courseService.updateCourse(id, data)
			const index = this.courses.findIndex(c => c.id === id)

			if (index !== -1) {
				this.courses.splice(index, 1, response.data)
			}

			return response.data
		},

		async deleteCourse(id) {
			await courseService.deleteCourse(id)
			this.courses = this.courses.filter(c => c.id != id)
		},


		// Subjects

		async fetchSubjects(params = {}) {
			this.loading = true
			this.error = null

			try {
				const response = await courseService.getSubjects({ page: this.currentPage, ...params })
				this.subjects = response.data.results
				this.subjectCount = response.data.coursesCount
				this.pageSize = response.data.page_size
			}
			catch (error) {
				this.error = error.message
			}
			finally {
				this.loading = false
			}
		},

		async fetchSubject(id) {
			const response = await courseService.getSubject(id)
			return response.data
		},

		async createSubject(data) {
			const response = await courseService.createSubject(data)
			this.subjects.push(response.data)
			return response.data
		},

		async updateSubject(id, data) {
			const response = await courseService.updateSubject(id, data)
			const index = this.subjects.findIndex(c => c.id === id)

			if (index !== -1) {
				this.subjects[index] = response.data
			}
			return response.data
		},

		async deleteSubject(id) {
			await courseService.deleteSubject(id)
			this.subjects = this.subjects.filter(s => s.id != id)
		},


		// Enrollment 

		async fetchEnrollments(params = {}) {
			this.loading = true
			this.error = null

			try {
				const response = await courseService.getEnrollments({ page: 1, page_size: 100, ...params })
				this.enrollments = response.data.results
				this.enrollmentsCount = response.data.count
				return this.enrollments
			}
			catch (error) {
				this.error = error.message
			}
			finally {
				this.loading = false
			}
		},

		async fetchEnrollment(id) {
			const response = await courseService.getEnrollment(id)
			return response.data
		},

		async createEnrollment(data) {
			const response = await courseService.createEnrollment(data)
			this.enrollments.push(response.data)
			return response.data
		},

		async updateEnrollment(id, data) {
			const response = await courseService.updateEnrollment(id, data)
			const index = this.enrollments.findIndex(e => e.id === id)

			if (index !== -1) {
				this.enrollments[index] = response.data
			}

			return response.data
		},

		async deleteEnrollment(id) {
			await courseService.deleteEnrollment(id)
			this.enrollments = this.enrollments.filter(e => e.id != id)
		}
	}
})
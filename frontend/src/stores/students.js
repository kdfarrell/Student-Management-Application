import { defineStore } from 'pinia'
import { studentService } from '../services/studentService'


export const useStudentStore = defineStore('students', {

    state: () => ({
        students: [],
        count: 0,
        pageSize: 10,
        currentPage: 1,
        loading: false,
        error: null,
    }),

    actions: {

        async fetchStudents(params = {}) {
            this.loading = true
            this.error = null
            try {
                const response = await studentService.getStudents({ page: this.currentPage, ...params })
                this.students = response.data.results
                this.count = response.data.count
                this.pageSize = response.data.page_size
            } catch (error) {
                this.error = error.message
            } finally {
                this.loading = false
            }
        },

        async goToPage(page) {
            this.currentPage = page
            await this.fetchStudents()
        },

        async fetchStudent(id) {
            const response = await studentService.getStudent(id)
            return response.data
        },

        async createStudent(data) {
            const response = await studentService.createStudent(data)
            this.students.push(response.data)
            return response.data
        },

        async updateStudent(id, data) {
            const response = await studentService.updateStudent(id, data)
            const index = this.students.findIndex( s => s.id === id)

            if (index !== -1 ) {
                this.students[index] = response.data
            }
            return response.data
        },

        async deleteStudent(id) {
            await studentService.deleteStudent(id)
            this.students = this.students.filter(s => s.id != id)
        },
    }

})
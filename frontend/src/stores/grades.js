import { defineStore } from 'pinia'
import { gradeService } from '@/services/gradeService'

export const useGradesStore = defineStore('grades', {
    state: () => ({
        assessments: [],
        grades: [],
        studentReport: [],
        loading: false,
        error: null,
    }),

    actions: {
        async fetchAssessments(subjectId) {
            this.loading = true
            try {
                const res = await gradeService.getAssessments({ subject: subjectId })
                this.assessments = res.data.results ?? res.data
            } catch (e) {
                this.error = e
            } finally {
                this.loading = false
            }
        },

        async createAssessment(data) {
            const res = await gradeService.createAssessment(data)
            this.assessments.push(res.data)
        },

        async updateAssessment(id, data) {
            const res = await gradeService.updateAssessment(id, data)
            const index = this.assessments.findIndex(a => a.id === id)
            if (index !== -1) this.assessments[index] = res.data
        },

        async deleteAssessment(id) {
            await gradeService.deleteAssessment(id)
            this.assessments = this.assessments.filter(a => a.id !== id)
        },

        async fetchGrades(assessmentId) {
            this.loading = true
            try {
                const res = await gradeService.getGrades({ assessment: assessmentId })
                this.grades = res.data.results ?? res.data
            } catch (e) {
                this.error = e
            } finally {
                this.loading = false
            }
        },

        async fetchStudentReport(studentId) {
            const res = await gradeService.getStudentReport(studentId)
            this.studentReport = res.data
        },
    }
})
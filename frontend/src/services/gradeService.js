import api from './api'

export const gradeService = {

    // Assessments

    getAssessments(params = {}) {
        return api.get('grades/assessments/', { params })
    },

    getAssessment(id) {
        return api.get(`grades/assessments/${id}/`)
    },

    createAssessment(data) {
        return api.post('grades/assessments/', data)
    },

    updateAssessment(id, data) {
        return api.put(`grades/assessments/${id}/`, data)
    },

    deleteAssessment(id) {
        return api.delete(`grades/assessments/${id}/`)
    },


    // Grades

    getGrades(params = {}) {
        return api.get('grades/grades/', { params })
    },

    getGrade(id) {
        return api.get(`grades/grades/${id}/`)
    },

    createGrade(data) {
        return api.post('grades/grades/', data)
    },

    updateGrade(id, data) {
        return api.patch(`grades/grades/${id}/`, data)
    },

    deleteGrade(id) {
        return api.delete(`grades/grades/${id}/`)
    },


    // Reports

    getStudentReport(studentId) {
        return api.get('grades/grades/student-report/', { params: { student_id: studentId } })
    }

}
import { getApiErrorMessage } from '@/utils/apiError'
import { reportService } from '@/services/reportService'
import { defineStore } from 'pinia'

export const useReportsStore = defineStore('reports', () => {

	function triggerDownload(blob, filename) {
		const url = window.URL.createObjectURL(new Blob([blob], { type: 'application/pdf' }))
		const link = document.createElement('a')
		link.href = url
		link.setAttribute('download', filename)
		document.body.appendChild(link)
		link.click()
		link.remove()
		window.URL.revokeObjectURL(url)
	}

	async function downloadGradeReport(studentId, courseId) {
		const response = await reportService.getGradeReport(studentId, courseId)
		triggerDownload(response.data, `grade_report_${studentId}_${courseId}.pdf`)
	}

	async function downloadAttendanceReport(studentId) {
		const response = await reportService.getAttendanceReport(studentId)
		triggerDownload(response.data, `attendance_report_${studentId}.pdf`)
	}

	async function downloadCourseGradeReport(courseId) {
		const response = await reportService.getCourseGradeReport(courseId)
		triggerDownload(response.data, `course_grade_report_${courseId}.pdf`)
	}

	async function sendEmailReport(payload) {
		await reportService.sendEmailReport(payload)
	}

	return {
		downloadGradeReport,
		downloadAttendanceReport,
		downloadCourseGradeReport,
		sendEmailReport,
		getApiErrorMessage,
	}
})

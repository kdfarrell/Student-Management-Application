<template>
	<div class="space-y-4">
		<div class="space-y-2">
			<Label>Student</Label>
			<Select v-model="selectedStudent" :disabled="loadingOptions">
				<SelectTrigger>
					<SelectValue :placeholder="loadingOptions ? 'Loading students...' : 'Select a student'" />
				</SelectTrigger>
				<SelectContent>
					<SelectItem v-for="s in students" :key="s.id" :value="String(s.id)">
						{{ s.first_name }} {{ s.last_name }}
					</SelectItem>
				</SelectContent>
			</Select>
		</div>

		<div class="space-y-2">
			<Label>Course</Label>
			<Select v-model="selectedCourse" :disabled="loadingOptions">
				<SelectTrigger>
					<SelectValue :placeholder="loadingOptions ? 'Loading courses...' : 'Select a course'" />
				</SelectTrigger>
				<SelectContent>
					<SelectItem v-for="c in courses" :key="c.id" :value="String(c.id)">
						{{ c.name }}
					</SelectItem>
				</SelectContent>
			</Select>
		</div>

		<div class="flex gap-2 pt-2">
			<Button class="flex-1" :disabled="!canDownload || downloading"
				@click="handleDownload">
				<Download class="w-4 h-4 mr-2" />
				{{ downloading ? 'Generating...' : 'Download PDF' }}
			</Button>
			<Button variant="outline" :disabled="!canDownload || downloading" @click="openEmailModal">
				<Mail class="w-4 h-4" />
			</Button>
		</div>

		<EmailReportModal v-if="showEmailModal" :student-id="selectedStudent" :course-id="selectedCourse"
			report-type="grade" :student-email="selectedStudentEmail" @close="showEmailModal = false" />
	</div>
</template>

<script setup>
import { Button } from '@/components/ui/button'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { courseService } from '@/services/courseService'
import { studentService } from '@/services/studentService'
import { useReportsStore } from '@/stores/reports'
import { getApiErrorMessage } from '@/utils/apiError'
import { Download, Mail } from 'lucide-vue-next'
import { computed, onMounted, ref } from 'vue'
import { toast } from 'vue-sonner'
import EmailReportModal from './EmailReportModal.vue'

const reportsStore = useReportsStore()

const selectedStudent = ref('')
const selectedCourse = ref('')
const showEmailModal = ref(false)
const downloading = ref(false)
const loadingOptions = ref(true)

const students = ref([])
const courses = ref([])

const canDownload = computed(() => selectedStudent.value && selectedCourse.value && !loadingOptions.value)

const selectedStudentEmail = computed(() => {
	const s = students.value.find(s => String(s.id) === selectedStudent.value)
	return s ? s.email : ''
})

onMounted(async () => {
	try {
		const [studentsRes, coursesRes] = await Promise.all([
			studentService.getStudents({ page: 1, page_size: 100 }),
			courseService.getCourses({ page: 1, page_size: 100 }),
		])
		students.value = studentsRes.data.results
		courses.value = coursesRes.data.results
	} catch {
		toast.error('Failed to load students or courses.')
	} finally {
		loadingOptions.value = false
	}
})

async function handleDownload() {
	downloading.value = true
	try {
		await reportsStore.downloadGradeReport(selectedStudent.value, selectedCourse.value)
		toast.success('Grade report downloaded successfully.')
	} catch (err) {
		toast.error(await getApiErrorMessage(err, 'Failed to download grade report.'))
	} finally {
		downloading.value = false
	}
}

function openEmailModal() {
	showEmailModal.value = true
}
</script>

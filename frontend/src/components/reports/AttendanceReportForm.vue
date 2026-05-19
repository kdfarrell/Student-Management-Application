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

		<div class="flex gap-2 pt-2">
			<Button class="flex-1" :disabled="!canDownload || downloading" @click="handleDownload">
				<Download class="w-4 h-4 mr-2" />
				{{ downloading ? 'Generating...' : 'Download PDF' }}
			</Button>
			<Button variant="outline" :disabled="!canDownload || downloading" @click="openEmailModal">
				<Mail class="w-4 h-4" />
			</Button>
		</div>

		<EmailReportModal v-if="showEmailModal" :student-id="selectedStudent" report-type="attendance"
			:student-email="selectedStudentEmail" @close="showEmailModal = false" />
	</div>
</template>

<script setup>
import { Button } from '@/components/ui/button'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { studentService } from '@/services/studentService'
import { useReportsStore } from '@/stores/reports'
import { getApiErrorMessage } from '@/utils/apiError'
import { Download, Mail } from 'lucide-vue-next'
import { computed, onMounted, ref } from 'vue'
import { toast } from 'vue-sonner'
import EmailReportModal from './EmailReportModal.vue'

const reportsStore = useReportsStore()

const selectedStudent = ref('')
const showEmailModal = ref(false)
const downloading = ref(false)
const loadingOptions = ref(true)
const students = ref([])

const canDownload = computed(() => selectedStudent.value && !loadingOptions.value)

const selectedStudentEmail = computed(() => {
	const s = students.value.find(s => String(s.id) === selectedStudent.value)
	return s ? s.email : ''
})

onMounted(async () => {
	try {
		const response = await studentService.getStudents({ page: 1, page_size: 100 })
		students.value = response.data.results
	} catch {
		toast.error('Failed to load students.')
	} finally {
		loadingOptions.value = false
	}
})

async function handleDownload() {
	downloading.value = true
	try {
		await reportsStore.downloadAttendanceReport(selectedStudent.value)
		toast.success('Attendance report downloaded successfully.')
	} catch (err) {
		toast.error(await getApiErrorMessage(err, 'Failed to download attendance report.'))
	} finally {
		downloading.value = false
	}
}

function openEmailModal() {
	showEmailModal.value = true
}
</script>

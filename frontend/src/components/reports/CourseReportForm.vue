<template>
	<div class="space-y-4">
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

		<Button class="w-full mt-2" :disabled="!canDownload || downloading" @click="handleDownload">
			<Download class="w-4 h-4 mr-2" />
			{{ downloading ? 'Generating...' : 'Download PDF' }}
		</Button>
	</div>
</template>

<script setup>
import { Button } from '@/components/ui/button'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { courseService } from '@/services/courseService'
import { useReportsStore } from '@/stores/reports'
import { getApiErrorMessage } from '@/utils/apiError'
import { Download } from 'lucide-vue-next'
import { computed, onMounted, ref } from 'vue'
import { toast } from 'vue-sonner'

const reportsStore = useReportsStore()

const selectedCourse = ref('')
const downloading = ref(false)
const loadingOptions = ref(true)
const courses = ref([])

const canDownload = computed(() => selectedCourse.value && !loadingOptions.value)

onMounted(async () => {
	try {
		const response = await courseService.getCourses({ page: 1, page_size: 100 })
		courses.value = response.data.results
	} catch {
		toast.error('Failed to load courses.')
	} finally {
		loadingOptions.value = false
	}
})

async function handleDownload() {
	downloading.value = true
	try {
		await reportsStore.downloadCourseGradeReport(selectedCourse.value)
		toast.success('Course grade report downloaded successfully.')
	} catch (err) {
		toast.error(await getApiErrorMessage(err, 'Failed to download course report.'))
	} finally {
		downloading.value = false
	}
}
</script>

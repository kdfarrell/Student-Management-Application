<script setup>
import { useCourseStore } from '@/stores/courses.js'
import { useStudentStore } from '@/stores/students.js'
import { computed, onMounted, ref, watch } from 'vue'

import { Button } from '@/components/ui/button'
import { Checkbox } from '@/components/ui/checkbox'
import {
	Dialog,
	DialogContent,
	DialogFooter,
	DialogHeader,
	DialogTitle,
} from '@/components/ui/dialog'
import { Input } from '@/components/ui/input'
import { toast } from 'vue-sonner'

const props = defineProps({
	open: { type: Boolean, default: false },
	courseId: { type: [Number, String], default: null },
	enrollments: { type: Array, default: () => [] }
})

const emit = defineEmits(['update:open', 'enrolled'])

const courseStore = useCourseStore()
const studentStore = useStudentStore()

const selectedIds = ref([])
const error = ref(null)
const search = ref('')
const currentPage = ref(1)

const enrolledActiveIds = computed(() =>
	props.enrollments.filter(e => e.status === 'active').map(e => e.student.id)
)

async function loadStudents() {
	await studentStore.fetchStudents({ search: search.value, page: currentPage.value })
}

onMounted(async () => {
	await loadStudents()
})

watch(search, () => {
	currentPage.value = 1
	loadStudents()
})

const totalPages = computed(() =>
	Math.ceil(studentStore.count / studentStore.pageSize)
)

function isEnrolled(studentId) {
	return enrolledActiveIds.value.includes(studentId)
}

function toggleStudent(id) {
	if (isEnrolled(id)) return
	const index = selectedIds.value.indexOf(id)
	if (index === -1) {
		selectedIds.value.push(id)
	} else {
		selectedIds.value.splice(index, 1)
	}
}

function isSelected(id) {
	return selectedIds.value.includes(id)
}

async function handleEnroll() {
	if (selectedIds.value.length === 0) {
		error.value = 'Please select at least one student'
		return
	}

	error.value = null

	try {
		await Promise.all(
			selectedIds.value.map(studentId =>
				courseStore.createEnrollment({
					student_id: studentId,
					course_id: parseInt(props.courseId),
					status: 'active'
				})
			)
		)
		toast.success(`${selectedIds.value.length} student(s) enrolled successfully.`)
		emit('enrolled')
		emit('update:open', false)
		selectedIds.value = []
		search.value = ''
		currentPage.value = 1
	} catch {
		toast.error('Failed to enroll students.')
	}
}
</script>

<template>
	<Dialog :open="open" @update:open="emit('update:open', $event)">
		<DialogContent class="max-h-[90vh] overflow-y-auto">
			<DialogHeader>
				<DialogTitle>Enroll Students</DialogTitle>
			</DialogHeader>

			<div class="grid gap-4 py-4">
				<Input v-model="search" placeholder="Search students..." />

				<div class="border rounded-md divide-y">
					<div v-if="studentStore.students.length === 0" class="p-4 text-sm text-muted-foreground">
						No students found.
					</div>
					<!-- The row handles the click event natively -->
					<div v-for="student in studentStore.students" :key="student.id"
						class="flex items-center gap-3 px-4 py-2 select-none"
						:class="isEnrolled(student.id) ? 'opacity-40 cursor-not-allowed' : 'cursor-pointer hover:bg-muted'"
						@click="toggleStudent(student.id)">

						<!-- @click.stop prevents double-firing, and v-model keeps the visual box synced perfectly -->
						<Checkbox :model-value="isSelected(student.id) || isEnrolled(student.id)"
							:disabled="isEnrolled(student.id)" @click.stop="toggleStudent(student.id)" />

						<div class="flex-1">
							<p class="font-medium text-sm">{{ student.first_name }} {{ student.last_name }}</p>
							<p class="text-xs text-muted-foreground">{{ student.email }}</p>
						</div>
						<span v-if="isEnrolled(student.id)" class="text-xs text-muted-foreground">Enrolled</span>
					</div>
				</div>

				<span v-if="error" class="text-sm text-red-500">{{ error }}</span>

				<div class="text-sm text-muted-foreground" v-if="selectedIds.length > 0">
					{{ selectedIds.length }} student{{ selectedIds.length === 1 ? '' : 's' }} selected
				</div>

				<div v-if="totalPages > 1" class="flex items-center justify-between text-sm">
					<Button variant="outline" size="sm" :disabled="currentPage === 1"
						@click="currentPage--; loadStudents()">Previous</Button>
					<span class="text-muted-foreground">Page {{ currentPage }} of {{ totalPages }}</span>
					<Button variant="outline" size="sm" :disabled="currentPage >= totalPages"
						@click="currentPage++; loadStudents()">Next</Button>
				</div>
			</div>

			<DialogFooter>
				<Button variant="outline" class="cursor-pointer" @click="emit('update:open', false)">Cancel</Button>
				<Button class="cursor-pointer" :disabled="selectedIds.length === 0 && !error" @click="handleEnroll">
					Enroll {{ selectedIds.length > 0 ? `(${selectedIds.length})` : '' }}
				</Button>
			</DialogFooter>
		</DialogContent>
	</Dialog>
</template>
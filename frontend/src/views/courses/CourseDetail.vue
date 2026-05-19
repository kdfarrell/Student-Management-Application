<script setup>
import ConfirmDialog from '@/components/common/ConfirmDialog.vue'
import EnrollStudentModal from "@/components/courses/EnrollStudentModal.vue"
import SubjectModal from "@/components/courses/SubjectModal.vue"
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { useCourseStore } from '@/stores/courses'
import { Pencil, Plus, Trash2 } from 'lucide-vue-next'
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { toast } from 'vue-sonner'

const route = useRoute()
const courseStore = useCourseStore()

const course = ref(null)
const subjects = ref([])
const enrollments = ref([])

const openSubjectModal = ref(false)
const selectedSubject = ref(null)
const openEnrollModal = ref(false)

const openConfirm = ref(false)
const confirmAction = ref(null)

onMounted(async () => {
	course.value = await courseStore.fetchCourse(route.params.id)
	subjects.value = course.value.subjects
	await courseStore.fetchEnrollments({ course: route.params.id })
	const filtered = courseStore.enrollments.filter(e => e.status === 'active')
	enrollments.value = [...filtered]
})

async function deleteSubject(id) {
	try {
		await courseStore.deleteSubject(id)
		subjects.value = subjects.value.filter(s => s.id !== id)
		toast.success('Subject removed.')
	} catch {
		toast.error('Failed to remove subject.')
	}
}

async function removeStudent(enrollmentId) {
	try {
		await courseStore.deleteEnrollment(enrollmentId)
		enrollments.value = enrollments.value.filter(e => e.id !== enrollmentId)
		toast.success('Student removed from course.')
	} catch {
		toast.error('Failed to remove student.')
	}
}

async function refreshCourse() {
	course.value = await courseStore.fetchCourse(route.params.id)
	subjects.value = course.value.subjects
}

async function refreshEnrollments() {
	await courseStore.fetchEnrollments({ course: route.params.id })
	enrollments.value = courseStore.enrollments.filter(e => e.status === 'active')
}


function confirmRemove(enrollmentId) {
	confirmAction.value = () => removeStudent(enrollmentId)
	openConfirm.value = true
}

</script>

<template>
	<div v-if="course" class="space-y-4">

		<!-- Course Info -->
		<Card>
			<CardContent class="pt-4 pb-4">
				<div class="flex items-center justify-between">
					<div>
						<h1 class="text-2xl font-bold">{{ course.name }}</h1>
						<p class="text-muted-foreground text-sm mt-1">{{ course.description }}</p>
					</div>
					<span :class="course.is_active ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'"
						class="text-xs px-2 py-1 rounded-full font-medium shrink-0 ml-4">
						{{ course.is_active ? 'Active' : 'Inactive' }}
					</span>
				</div>
			</CardContent>
		</Card>

		<!-- Subjects + Enrollments -->
		<div class="grid grid-cols-1 lg:grid-cols-2 gap-4">

			<!-- Subjects -->
			<Card>
				<CardHeader class="pb-2">
					<div class="flex items-center justify-between">
						<CardTitle>Subjects</CardTitle>
						<Button size="sm" class="cursor-pointer"
							@click="selectedSubject = null; openSubjectModal = true">
							<Plus class="w-4 h-4 mr-1" /> Add Subject
						</Button>
					</div>
				</CardHeader>
				<CardContent>
					<div v-if="subjects.length === 0" class="text-muted-foreground text-sm">No subjects yet.</div>
					<div v-for="subject in subjects" :key="subject.id"
						class="flex items-center justify-between py-2 border-b last:border-0">
						<div>
							<p class="font-medium">{{ subject.name }}</p>
							<p class="text-sm text-muted-foreground">{{ subject.description }} · Weight: {{
								subject.weight }}</p>
						</div>
						<div class="flex gap-2">
							<Button variant="ghost" size="icon"
								@click="selectedSubject = subject; openSubjectModal = true">
								<Pencil class="w-4 h-4" />
							</Button>
							<Button variant="ghost" size="icon" class="text-red-500 hover:text-red-700 hover:bg-red-50"
								@click="deleteSubject(subject.id)">
								<Trash2 class="w-4 h-4" />
							</Button>
						</div>
					</div>
				</CardContent>
			</Card>

			<!-- Enrolled Students -->
			<Card>
				<CardHeader class="pb-2">
					<div class="flex items-center justify-between">
						<CardTitle>Enrolled Students</CardTitle>
						<Button size="sm" class="cursor-pointer" @click="openEnrollModal = true">
							<Plus class="w-4 h-4 mr-1" /> Enroll Student
						</Button>
					</div>
				</CardHeader>
				<CardContent>
					<div v-if="enrollments.length === 0" class="text-muted-foreground text-sm">No students enrolled.
					</div>
					<div v-for="enrollment in enrollments" :key="enrollment.id"
						class="flex items-center justify-between py-2 border-b last:border-0">
						<div>
							<p class="font-medium">{{ enrollment.student.first_name }} {{ enrollment.student.last_name
								}}</p>
							<p class="text-sm text-muted-foreground">{{ enrollment.student.email }}</p>
						</div>
						<div class="flex items-center gap-2">

							<Button v-if="enrollment.status === 'active'" variant="ghost" size="sm"
								class="text-red-500 hover:text-red-700 cursor-pointer"
								@click="confirmRemove(enrollment.id)">
								Remove
							</Button>
						</div>
					</div>
				</CardContent>
			</Card>

		</div>
	</div>
	<div v-else class="text-muted-foreground">Loading...</div>

	<SubjectModal :key="selectedSubject?.id || 'new-subject'" :subject="selectedSubject" :open="openSubjectModal"
		@update:open="openSubjectModal = $event" @saved="refreshCourse" />

	<EnrollStudentModal :open="openEnrollModal" :courseId="route.params.id" :enrollments="enrollments"
		@update:open="openEnrollModal = $event" @enrolled="refreshEnrollments" />

	<ConfirmDialog :open="openConfirm" title="Remove Student"
		message="Are you sure you want to remove this student from the course?" confirm-label="Remove"
		@update:open="openConfirm = $event" @confirm="confirmAction" />
</template>
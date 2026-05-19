<script setup>

import {
	Card,
	CardContent,
	CardDescription,
	CardFooter,
	CardHeader,
	CardTitle,
} from '@/components/ui/card';

import ConfirmDialog from '@/components/common/ConfirmDialog.vue'
import { Button } from '@/components/ui/button';
import { useCourseStore } from '@/stores/courses';
import { computed, onMounted, ref } from 'vue';

import { BookOpen, SquarePen, Trash2, Users } from 'lucide-vue-next';

import CourseModal from "@/components/courses/CourseModal.vue";
import { toast } from 'vue-sonner'

const courseStore = useCourseStore()

onMounted(async () => {
	await courseStore.fetchCourses({ page: 1, page_size: 100 })
	await courseStore.fetchSubjects({ page: 1, page_size: 200 })
	await courseStore.fetchEnrollments()
})

const selectedCourse = ref(null)
const openModal = ref(false)
const openConfirm = ref(false)
const courseToDelete = ref(null)
const courses = computed(() => courseStore.courses)

const deleteMessage = computed(() => {
	if (!courseToDelete.value) return 'This action cannot be undone.'
	return `Delete "${courseToDelete.value.name}"? This removes its subjects, sessions, and enrollments.`
})

function promptDelete(course) {
	courseToDelete.value = course
	openConfirm.value = true
}

async function confirmDelete() {
	if (!courseToDelete.value) return
	try {
		await courseStore.deleteCourse(courseToDelete.value.id)
		toast.success('Course deleted.')
	} catch {
		toast.error('Failed to delete course.')
	} finally {
		courseToDelete.value = null
	}
}

</script>

<template>

	<div class="flex mb-4">
		<Button class="cursor-pointer" @click="selectedCourse = null; openModal = true">
			Add Course
		</Button>
	</div>


	<div class="grid grid-cols-1 md:grid-cols-3 gap-6">
		<Card v-for="course in courses" :key="course.id" class="hover:shadow-lg transition-shadow duration-200">
			<CardHeader class="pb-2">
				<div class="flex items-center justify-between">
					<CardTitle class="text-lg">{{ course.name }}</CardTitle>
					<span :class="course.is_active ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'"
						class="text-xs px-2 py-1 rounded-full font-medium">
						{{ course.is_active ? 'Active' : 'Inactive' }}
					</span>
				</div>
				<CardDescription>{{ course.description }}</CardDescription>
			</CardHeader>
			<CardContent class="pb-2">
				<div class="flex gap-6 text-sm text-muted-foreground">
					<span class="flex items-center gap-1">
						<BookOpen class="w-4 h-4" />
						{{ course?.subjects?.length || 0 }}
						{{ course?.subjects?.length === 1 ? 'Subject' : 'Subjects' }}
					</span>
					<span class="flex items-center gap-1">
						<Users class="w-4 h-4" />
						{{ course?.enrolled_students_count || 0 }}
						{{ course?.enrolled_students_count === 1 ? 'Student' : 'Students' }}
					</span>
				</div>
			</CardContent>
			<CardFooter class="pt-2 flex gap-2">
				<Button class="cursor-pointer flex-1" @click="$router.push(`/courses/${course.id}`)">View
					Details</Button>
				<Button class="cursor-pointer" variant="outline" size="icon"
					@click="selectedCourse = course; openModal = true">
					<SquarePen class="w-4 h-4" />
				</Button>
				<Button class="cursor-pointer" variant="destructive" size="icon" @click="promptDelete(course)">
					<Trash2 class="w-4 h-4" />
				</Button>
			</CardFooter>
		</Card>
	</div>

	<CourseModal :key="selectedCourse?.id || 'new-course'" :course="selectedCourse" :open="openModal"
		@update:open="openModal = $event" @saved="courseStore.fetchCourses({ page: 1, page_size: 100 })" />

	<ConfirmDialog
		:open="openConfirm"
		title="Delete Course?"
		:message="deleteMessage"
		confirm-label="Delete Course"
		cancel-label="Cancel"
		@update:open="openConfirm = $event"
		@confirm="confirmDelete"
	/>

</template>

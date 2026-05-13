<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useCourseStore } from '@/stores/courses.js'
import { useStudentStore } from '@/stores/students.js'

import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogFooter,
} from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'

const props = defineProps({
    open: { type: Boolean, default: false },
    courseId: { type: [Number, String], default: null },
    enrollments: { type: Array, default: () => [] }
})

const emit = defineEmits(['update:open', 'enrolled'])

const courseStore = useCourseStore()
const studentStore = useStudentStore()

const selectedStudentId = ref(null)
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

const totalPages = computed(() => {
    return Math.ceil(studentStore.count / studentStore.pageSize)
})

function isEnrolled(studentId) {
    return enrolledActiveIds.value.includes(studentId)
}

function selectStudent(id) {
    selectedStudentId.value = id
    error.value = null
}

async function handleEnroll() {
    if (!selectedStudentId.value) {
        error.value = 'Please select a student'
        return
    }

    error.value = null

    await courseStore.createEnrollment({
        student_id: parseInt(selectedStudentId.value),
        course_id: parseInt(props.courseId),
        status: 'active'
    })

    emit('enrolled')
    emit('update:open', false)
    selectedStudentId.value = null
    search.value = ''
    currentPage.value = 1
}
</script>

<template>
    <Dialog :open="open" @update:open="emit('update:open', $event)">
        <DialogContent class="max-h-[90vh] overflow-y-auto">
            <DialogHeader>
                <DialogTitle>Enroll Student</DialogTitle>
            </DialogHeader>

            <div class="grid gap-4 py-4">
                <!-- Search -->
                <Input v-model="search" placeholder="Search students..." />

                <!-- Student List -->
                <div class="border rounded-md divide-y">
                    <div v-if="studentStore.students.length === 0" class="p-4 text-sm text-muted-foreground">
                        No students found.
                    </div>
                    <div
                        v-for="student in studentStore.students"
                        :key="student.id"
                        class="flex items-center justify-between px-4 py-2"
                        :class="isEnrolled(student.id) ? 'opacity-40 cursor-not-allowed' : 'cursor-pointer hover:bg-muted'"
                        @click="!isEnrolled(student.id) && selectStudent(student.id)">
                        <div>
                            <p class="font-medium text-sm">{{ student.first_name }} {{ student.last_name }}</p>
                            <p class="text-xs text-muted-foreground">{{ student.email }}</p>
                        </div>
                        <div class="flex items-center gap-2">
                            <span v-if="isEnrolled(student.id)" class="text-xs text-muted-foreground">Enrolled</span>
                            <div v-else-if="selectedStudentId === student.id"
                                class="w-3 h-3 rounded-full bg-primary" />
                        </div>
                    </div>
                </div>

                <span v-if="error" class="text-sm text-red-500">{{ error }}</span>

                <!-- Pagination -->
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
                <Button class="cursor-pointer" @click="handleEnroll">Enroll</Button>
            </DialogFooter>
        </DialogContent>
    </Dialog>
</template>
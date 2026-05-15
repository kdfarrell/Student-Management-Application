<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useCourseStore } from '@/stores/courses'
import AssessmentList from '@/components/grades/AssessmentList.vue'
import GradeEntry from '@/components/grades/GradeEntry.vue'

import { useGradesStore } from '@/stores/grades'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue
} from '@/components/ui/select'

const coursesStore = useCourseStore()

onMounted(async () => {
  await coursesStore.fetchCourses()
})

const courses = computed(() => coursesStore.courses)
const selectedCourseId = ref(localStorage.getItem('grades_course') ?? '')
const selectedSubjectId = ref(localStorage.getItem('grades_subject') ?? '')
const selectedAssessmentId = ref(null)

const filteredSubjects = computed(() => {
  if (!coursesStore.courses.length) return []
  const course = coursesStore.courses.find(c => String(c.id) === selectedCourseId.value)
  return course?.subjects ?? []
})

watch(selectedCourseId, (val) => {
  localStorage.setItem('grades_course', val)
  selectedSubjectId.value = ''
  selectedAssessmentId.value = null
})

watch(selectedSubjectId, (val) => {
  localStorage.setItem('grades_subject', val)
  selectedAssessmentId.value = null
})

function handleAssessmentSelect(id) {
  selectedAssessmentId.value = id
}

const gradesStore = useGradesStore()

watch(() => coursesStore.courses, (courses) => {
  if (courses.length && selectedSubjectId.value) {
    gradesStore.fetchAssessments(Number(selectedSubjectId.value))
  }
})
</script>

<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold mb-6">Grades</h1>

    <div class="flex gap-6">
      <!-- Left panel: course + subject selector -->
      <div class="w-64 shrink-0 space-y-4">
        <div>
          <label class="text-sm font-medium">Course</label>
          <Select v-model="selectedCourseId">
            <SelectTrigger class="w-full mt-1">
              <SelectValue placeholder="Select course" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem v-for="course in courses" :key="course.id" :value="String(course.id)">
                {{ course.name }}
              </SelectItem>
            </SelectContent>
          </Select>
        </div>

        <div v-if="selectedCourseId">
          <label class="text-sm font-medium">Subject</label>
          <Select v-model="selectedSubjectId">
            <SelectTrigger class="w-full mt-1">
              <SelectValue placeholder="Select subject" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem v-for="subject in filteredSubjects" :key="subject.id" :value="String(subject.id)">
                {{ subject.name }}
              </SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>

      <!-- Right panel: assessments + grade entry -->
      <div class="flex-1">
        <div v-if="!selectedSubjectId" class="text-muted-foreground text-sm">
          Select a course and subject to view grades.
        </div>

        <div v-else>
          <AssessmentList
            :subject-id="Number(selectedSubjectId)"
            @select="handleAssessmentSelect"
          />

          <GradeEntry
            v-if="selectedAssessmentId"
            :assessment-id="selectedAssessmentId"
            :course-id="Number(selectedCourseId)"
            class="mt-6"
          />
        </div>
      </div>
    </div>
  </div>
</template>
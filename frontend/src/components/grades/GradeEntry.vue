<template>
  <div>
    <div class="flex items-center justify-between mb-3">
      <h2 class="text-lg font-semibold">Grade Entry</h2>
      <Button @click="saveAll" :disabled="loading">
        {{ loading ? 'Saving...' : 'Save All' }}
      </Button>
    </div>

    <div v-if="loadingStudents" class="text-sm text-muted-foreground">Loading students...</div>

    <Table v-else>
      <TableHeader>
        <TableRow>
          <TableHead>Student</TableHead>
          <TableHead>Score (max: {{ maxScore }})</TableHead>
          <TableHead>Feedback</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        <TableRow v-for="row in rows" :key="row.studentId">
          <TableCell>{{ row.name }}</TableCell>
          <TableCell>
            <Input
              v-model="row.score"
              type="number"
              :max="maxScore"
              :min="0"
              class="w-24"
            />
            <p v-if="row.error" class="text-xs text-red-500">{{ row.error }}</p>
          </TableCell>
          <TableCell>
            <Input v-model="row.feedback" placeholder="Optional" />
          </TableCell>
        </TableRow>
      </TableBody>
    </Table>

    <p v-if="saveError" class="text-sm text-red-500 mt-2">{{ saveError }}</p>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useGradesStore } from '@/stores/grades'
import { useCourseStore } from '@/stores/courses'
import { gradeService } from '@/services/gradeService'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import {
  Table, TableHeader, TableRow, TableHead, TableBody, TableCell
} from '@/components/ui/table'
import { toast } from 'vue-sonner'

const props = defineProps({
  assessmentId: { type: Number, required: true },
  courseId: { type: Number, required: true },
})

const gradesStore = useGradesStore()
const coursesStore = useCourseStore()
const rows = ref([])
const maxScore = ref(100)
const loading = ref(false)
const loadingStudents = ref(false)
const saveError = ref('')

watch(() => props.assessmentId, async (id) => {
  if (!id) return
  loadingStudents.value = true

  await gradesStore.fetchGrades(id)

  const assessment = gradesStore.assessments.find(a => a.id === id)
  if (assessment) maxScore.value = assessment.max_score

  const enrollments = await coursesStore.fetchEnrollments({ course: props.courseId })
  const existingGrades = gradesStore.grades

  rows.value = enrollments.map(enrollment => {
    const existing = existingGrades.find(g => g.student.id === enrollment.student.id)
    return {
      studentId: enrollment.student.id,
      gradeId: existing?.id ?? null,
      name: `${enrollment.student.first_name} ${enrollment.student.last_name}`,
      score: existing?.score ?? '',
      feedback: existing?.feedback ?? '',
      error: '',
    }
  })

  loadingStudents.value = false
}, { immediate: true })

async function saveAll() {
  let valid = true
  rows.value.forEach(row => {
    row.error = ''
    if (row.score === '' || row.score === null) {
      row.error = 'Required'
      valid = false
    } else if (Number(row.score) > Number(maxScore.value)) {
      row.error = `Max is ${maxScore.value}`
      valid = false
    }
  })
  if (!valid) return

  loading.value = true
  saveError.value = ''
  try {
    for (const row of rows.value) {
      const payload = {
        student_id: row.studentId,
        assessment_id: props.assessmentId,
        score: row.score,
        feedback: row.feedback,
      }
      if (row.gradeId) {
        await gradeService.updateGrade(row.gradeId, payload)
      } else {
        await gradeService.createGrade(payload)
      }
    }
    toast.success('Grades saved successfully.')
  } catch {
    saveError.value = 'Failed to save some grades.'
    toast.error('Failed to save grades.')
  } finally {
    loading.value = false
  }
}

</script>
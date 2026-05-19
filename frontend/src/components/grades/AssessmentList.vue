<template>
  <div>
    <div class="flex items-center justify-between mb-3">
      <h2 class="text-lg font-semibold">Assessments</h2>
      <Button size="sm" class="cursor-pointer" @click="openCreate">Add Assessment</Button>
    </div>

    <div v-if="store.loading" class="text-sm text-muted-foreground">Loading...</div>

    <div v-else-if="store.assessments.length === 0" class="text-sm text-muted-foreground">
      No assessments yet.
    </div>

    <div v-else class="space-y-2">
      <div
        v-for="assessment in store.assessments"
        :key="assessment.id"
        class="flex items-center justify-between border rounded px-4 py-2 cursor-pointer hover:bg-muted"
        :class="{ 'bg-muted': selectedId === assessment.id }"
        @click="$emit('select', assessment.id)"
      >
        <div>
          <p class="font-medium text-sm">{{ assessment.name }}</p>
          <p class="text-xs text-muted-foreground">{{ assessment.assessment_type }} · Max: {{ assessment.max_score }}</p>
        </div>
        <div class="flex gap-2">
          <Button variant="ghost" size="sm" class="cursor-pointer" @click.stop="openEdit(assessment)">Edit</Button>
          <Button variant="ghost" size="sm" class="cursor-pointer" @click.stop="handleDelete(assessment.id)">Delete</Button>
        </div>
      </div>
    </div>

    <AssessmentModal
      v-if="showModal"
      :key="editTarget?.id ?? 'new'"
      :subject-id="subjectId"
      :assessment="editTarget"
      @close="showModal = false"
      @saved="showModal = false"
    />
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useGradesStore } from '@/stores/grades'
import { Button } from '@/components/ui/button'
import AssessmentModal from './AssessmentModal.vue'
import { toast } from 'vue-sonner'

const props = defineProps({
  subjectId: { type: Number, required: true },
  selectedId: { type: Number, default: null },
})

defineEmits(['select'])

const store = useGradesStore()
const showModal = ref(false)
const editTarget = ref(null)

watch(() => props.subjectId, (id) => {
  if (id) store.fetchAssessments(id)
}, { immediate: true })

function openCreate() {
  editTarget.value = null
  showModal.value = true
}

function openEdit(assessment) {
  editTarget.value = assessment
  showModal.value = true
}

async function handleDelete(id) {
  try {
    await store.deleteAssessment(id)
    toast.success('Assessment deleted.')
  } catch {
    toast.error('Failed to delete assessment.')
  }
}
</script>
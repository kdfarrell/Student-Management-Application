<script setup>
import { Button } from '@/components/ui/button'
import { Calendar } from '@/components/ui/calendar'
import { Dialog, DialogContent, DialogFooter, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { useGradesStore } from '@/stores/grades'
import { CalendarIcon } from 'lucide-vue-next'
import { ref, watch } from 'vue'

const props = defineProps({
  subjectId: { type: Number, required: true },
  assessment: { type: Object, default: null },
})

const emit = defineEmits(['close', 'saved'])
const store = useGradesStore()
const loading = ref(false)
const error = ref('')
const dateOpen = ref(false)

const form = ref({
  name: '',
  max_score: '',
  date: '',
  assessment_type: 'exam',
  subject_id: props.subjectId,
})


watch(() => props.assessment, (val) => {
  console.log('assessment prop:', val)
  form.value = {
    name: val?.name ?? '',
    max_score: val?.max_score ?? '',
    date: val?.date ?? '',
    assessment_type: val?.assessment_type ?? 'exam',
    subject_id: props.subjectId,
  }
}, { immediate: true })

function handleDateSelect(val) {
  if (!val) return
  const d = new Date(val)
  form.value.date = d.toISOString().split('T')[0]
  dateOpen.value = false
}

async function handleSave() {
  if (!form.value.name || !form.value.max_score || !form.value.date) {
    error.value = 'All fields are required.'
    return
  }
  loading.value = true
  try {
    if (props.assessment) {
      await store.updateAssessment(props.assessment.id, form.value)
    } else {
      await store.createAssessment(form.value)
    }
    emit('saved')
  } catch {
    error.value = 'Failed to save.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <Dialog :open="true" @update:open="$emit('close')">
    <DialogContent>
      <DialogHeader>
        <DialogTitle>{{ assessment ? 'Edit Assessment' : 'Add Assessment' }}</DialogTitle>
      </DialogHeader>

      <div class="space-y-4">
        <div>
          <Label class="pb-2">Name</Label>
          <Input v-model="form.name" placeholder="e.g. Midterm Exam" />
        </div>
        <div>
          <Label class="pb-2">Max Score</Label>
          <Input v-model="form.max_score" type="number" />
        </div>
        <div>
          <Label class="pb-2">Date</Label>
          <Popover v-model:open="dateOpen">
            <PopoverTrigger as-child>
              <Button variant="outline" class="w-full justify-start text-left font-normal cursor-pointer">
                <CalendarIcon class="mr-2 h-4 w-4" />
                {{ form.date || 'Pick a date' }}
              </Button>
            </PopoverTrigger>
            <PopoverContent class="w-auto p-0">
              <Calendar @update:model-value="handleDateSelect" />
            </PopoverContent>
          </Popover>
        </div>
        <div>
          <Label class="pb-2">Type</Label>
          <Select v-model="form.assessment_type">
            <SelectTrigger class="w-full cursor-pointer">
              <SelectValue placeholder="Select type" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="test">Test</SelectItem>
              <SelectItem value="assignment">Assignment</SelectItem>
              <SelectItem value="exam">Exam</SelectItem>
              <SelectItem value="quiz">Quiz</SelectItem>
            </SelectContent>
          </Select>
        </div>
        <p v-if="error" class="text-sm text-red-500">{{ error }}</p>
      </div>

      <DialogFooter>
        <Button variant="outline" class="cursor-pointer" @click="$emit('close')">Cancel</Button>
        <Button class="cursor-pointer" @click="handleSave" :disabled="loading">
          {{ loading ? 'Saving...' : 'Save' }}
        </Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>
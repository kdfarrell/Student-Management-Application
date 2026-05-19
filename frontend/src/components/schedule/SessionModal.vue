<script setup>
import { useCourseStore } from '@/stores/courses'
import { useScheduleStore } from '@/stores/scheduling'
import { computed, onMounted, ref, watch } from 'vue'


import { Button } from '@/components/ui/button'
import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Textarea } from '@/components/ui/textarea'


import ConfirmDialog from '@/components/common/ConfirmDialog.vue'
import { toast } from 'vue-sonner'

const props = defineProps({
  open: { type: Boolean, required: true },
  sessionData: { type: Object, default: null },
  defaultDate: { type: String, default: '' }
})

const emit = defineEmits(['update:open', 'refresh'])

const scheduleStore = useScheduleStore()
const courseStore = useCourseStore()

const isConfirmDeleteDialogOpen = ref(false)

onMounted(async () => {
  await courseStore.fetchSubjects({ page: 1, page_size: 200 })
})

const subjects = computed(() => {
  return courseStore.subjects || []
})

const form = ref({
  id: null,
  subject: '',
  date: '',
  start_time: '',
  end_time: '',
  room: '',
  notes: ''
})

watch(() => props.open, (isOpen) => {
  if (isOpen) {
    if (props.sessionData) {
      const targetSubjectId = typeof props.sessionData.subject === 'object' 
        ? props.sessionData.subject?.id 
        : props.sessionData.subject

      form.value = {
        id: props.sessionData.id,
        subject: targetSubjectId ? targetSubjectId.toString() : '',
        date: props.sessionData.date ? props.sessionData.date.split('T')[0] : '',
        start_time: props.sessionData.start_time || '',
        end_time: props.sessionData.end_time || '',
        room: props.sessionData.room || '',
        notes: props.sessionData.notes || ''
      }
    } else {
      form.value = {
        id: null,
        subject: '',
        date: props.defaultDate || '',
        start_time: '',
        end_time: '',
        room: '',
        notes: ''
      }
    }
  }
})

const updateOpenState = (value) => {
  emit('update:open', value)
}

const handleSubmit = async () => {
  try {
    const payload = {
      ...form.value,
      subject: parseInt(form.value.subject, 10)
    }

    if (form.value.id) {
      await scheduleStore.updateSchedule(form.value.id, payload)
      toast.success('Session updated successfully.')
    } else {
      await scheduleStore.createSchedule(payload)
      toast.success('Session created successfully.')
    }

    emit('refresh')
    updateOpenState(false)
  } catch {
    toast.error('Failed to save session.')
  }
}

const handleDeleteConfirm = async () => {
  if (!form.value.id) return
  
  try {
    await scheduleStore.deleteSchedule(form.value.id)
    toast.success('Session deleted.')
    updateOpenState(false)
    emit('refresh')
  } catch {
    toast.error('Failed to delete session.')
  }
}
</script>

<template>
  <!-- Main Form Dialog -->
  <Dialog :open="open" @update:open="updateOpenState">
    <DialogContent class="sm:max-w-[425px]">
      <DialogHeader>
        <DialogTitle class="text-lg font-bold">
          {{ form.id ? 'Edit Session' : 'Add New Session' }}
        </DialogTitle>
      </DialogHeader>

      <form @submit.prevent="handleSubmit" class="space-y-4 py-2 text-left">

        <div class="space-y-1.5">
          <Label for="subject" class="text-xs font-semibold uppercase text-muted-foreground tracking-wide">Subject</Label>
          <Select v-model="form.subject" required>
            <SelectTrigger id="subject" class="w-full">
              <SelectValue placeholder="Select a subject" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem v-for="subj in subjects" :key="subj.id" :value="subj.id.toString()">
                {{ subj.name }}
              </SelectItem>
            </SelectContent>
          </Select>
        </div>

        <div class="space-y-1.5">
          <Label for="date" class="text-xs font-semibold uppercase text-muted-foreground tracking-wide">Date</Label>
          <Input id="date" type="date" v-model="form.date" required />
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div class="space-y-1.5">
            <Label for="start_time" class="text-xs font-semibold uppercase text-muted-foreground tracking-wide">Start Time</Label>
            <Input id="start_time" type="time" v-model="form.start_time" required />
          </div>
          <div class="space-y-1.5">
            <Label for="end_time" class="text-xs font-semibold uppercase text-muted-foreground tracking-wide">End Time</Label>
            <Input id="end_time" type="time" v-model="form.end_time" required />
          </div>
        </div>

        <div class="space-y-1.5">
          <Label for="room" class="text-xs font-semibold uppercase text-muted-foreground tracking-wide">Room / Location</Label>
          <Input id="room" type="text" placeholder="e.g. Room 302, Hall A" v-model="form.room" />
        </div>

        <div class="space-y-1.5">
          <Label for="notes" class="text-xs font-semibold uppercase text-muted-foreground tracking-wide">Notes</Label>
          <Textarea id="notes" placeholder="Enter session updates or reminders..." v-model="form.notes" class="resize-none" rows="3" />
        </div>

        <DialogFooter class="pt-4 border-t flex flex-col-reverse sm:flex-row sm:justify-between gap-2 sm:gap-0">
          <!-- Left side: Danger Zone Action -->
          <div>
            <Button 
              v-if="form.id" 
              type="button" 
              variant="destructive" 
              class="w-full sm:w-auto"
              @click="isConfirmDeleteDialogOpen = true"
            >
              Delete Session
            </Button>
          </div>

          <!-- Right side: Core updates handlers -->
          <div class="flex flex-col sm:flex-row gap-2">
            <Button type="button" variant="outline" @click="updateOpenState(false)">
              Cancel
            </Button>
            <Button type="submit" :disabled="scheduleStore.loading">
              {{ form.id ? 'Save Changes' : 'Create Session' }}
            </Button>
          </div>
        </DialogFooter>

      </form>
    </DialogContent>
  </Dialog>

  <ConfirmDialog
    v-model:open="isConfirmDeleteDialogOpen"
    title="Delete Session?"
    message="Are you absolutely sure you want to remove this session? This action cannot be undone."
    confirmLabel="Yes, Delete Session"
    cancelLabel="Keep Session"
    @confirm="handleDeleteConfirm"
  />
</template>
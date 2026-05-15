<template>
  <div class="space-y-4">
    <div v-if="loading" class="text-sm text-muted-foreground">Loading...</div>

    <div v-else-if="report.length === 0" class="text-sm text-muted-foreground">
      No grade data available.
    </div>

    <div v-else>
      <div v-for="item in report" :key="item.subject" class="border rounded p-4">
        <div class="flex items-center justify-between">
          <p class="font-medium">{{ item.subject }}</p>
          <Badge :class="badgeClass(item.weighted_average)">
            {{ item.weighted_average }}%
          </Badge>
        </div>
        <p class="text-xs text-muted-foreground mt-1">Weight: {{ item.weight }}</p>
      </div>

      <div class="border rounded p-4 mt-4 bg-muted">
        <p class="font-semibold">Overall Average</p>
        <Badge :class="badgeClass(overallAverage)">{{ overallAverage }}%</Badge>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, watch } from 'vue'
import { useGradesStore } from '@/stores/grades'
import { Badge } from '@/components/ui/badge'

const props = defineProps({
  studentId: { type: Number, required: true },
})

const store = useGradesStore()
const loading = computed(() => store.loading)
const report = computed(() => store.studentReport)

watch(() => props.studentId, (id) => {
  if (id) store.fetchStudentReport(id)
}, { immediate: true })

const overallAverage = computed(() => {
  if (!report.value.length) return 0
  const total = report.value.reduce((sum, item) => sum + item.weighted_average, 0)
  return Math.round(total / report.value.length)
})

function badgeClass(score) {
  if (score >= 70) return 'bg-green-100 text-green-800'
  if (score >= 50) return 'bg-yellow-100 text-yellow-800'
  return 'bg-red-100 text-red-800'
}
</script>
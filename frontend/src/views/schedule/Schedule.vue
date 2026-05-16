<script setup>
import { useScheduleStore } from '@/stores/scheduling'
import { CalendarDate, fromDate, getLocalTimeZone } from '@internationalized/date'
import { computed, onMounted, ref, watch } from 'vue'

// Shadcn Vue Component Imports
import { Button } from '@/components/ui/button'
import { Calendar } from '@/components/ui/calendar'
import { Separator } from '@/components/ui/separator'

// Import the updated Shadcn-based modal
import SessionModal from '@/components/schedule/SessionModal.vue'

// State & Store Setup
const date = ref(fromDate(new Date(), getLocalTimeZone()))
const scheduleStore = useScheduleStore()

// Modal Sync Control
const isModalOpen = ref(false)
const selectedSession = ref(null)
const targetDate = ref('')

// Format a JS Date to YYYY-MM-DD using local time (avoids UTC offset shift)
const toLocalDateString = (d) => {
	const yyyy = d.getFullYear()
	const mm = String(d.getMonth() + 1).padStart(2, '0')
	const dd = String(d.getDate()).padStart(2, '0')
	return `${yyyy}-${mm}-${dd}`
}

// Calculate the 7 days of the current selected week
const weekDays = computed(() => {
	const jsDate = date.value.toDate(getLocalTimeZone())
	const currentDayOfWeek = jsDate.getDay()

	const weekStart = new Date(jsDate)
	weekStart.setDate(jsDate.getDate() - currentDayOfWeek)

	const days = []
	for (let i = 0; i < 7; i++) {
		const day = new Date(weekStart)
		day.setDate(weekStart.getDate() + i)

		days.push({
			dateString: toLocalDateString(day),
			dayName: day.toLocaleDateString('en-US', { weekday: 'short' }),
			dayNumber: day.getDate()
		})
	}
	return days
})

// Derive the week's start and end date strings from the selected date
const weekRange = computed(() => {
	const jsDate = date.value.toDate(getLocalTimeZone())
	const currentDayOfWeek = jsDate.getDay()

	const weekStart = new Date(jsDate)
	weekStart.setDate(jsDate.getDate() - currentDayOfWeek)

	const weekEnd = new Date(weekStart)
	weekEnd.setDate(weekStart.getDate() + 6)

	return {
		date_from: toLocalDateString(weekStart),
		date_to: toLocalDateString(weekEnd)
	}
})

// Fetch sessions scoped to the currently visible week
const fetchWeekSessions = async () => {
	await scheduleStore.fetchSchedules(weekRange.value)
}

// Fetch on mount, and re-fetch whenever the selected date changes
onMounted(async () => {
	await fetchWeekSessions()
})

watch(date, async () => {
	await fetchWeekSessions()
})

// Filter store schedules matching a specific column date string
const getSessionsForDay = (dateString) => {
	if (!scheduleStore.schedules) return []
	return scheduleStore.schedules.filter(session => {
		if (!session.date) return false
		return session.date.split('T')[0] === dateString
	})
}

// Convert "HH:MM:SS" time layouts into user-friendly displays
const formatTime = (timeString) => {
	if (!timeString) return ''
	const hasDatePart = timeString.includes('-') || timeString.includes('T')
	const dateObj = new Date(hasDatePart ? timeString : `1970-01-01T${timeString}`)
	return dateObj.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true })
}

// Handlers for modal interactions
const openAddModal = (dateString) => {
	selectedSession.value = null
	targetDate.value = dateString
	isModalOpen.value = true
}

const openEditModal = (session) => {
	targetDate.value = session.date.split('T')[0]
	selectedSession.value = { ...session }
	isModalOpen.value = true
}
</script>

<template>
	<div class="space-y-6 p-6 max-w-7xl mx-auto">
		<div class="flex justify-center">
			<Calendar v-model="date" class="rounded-md border shadow-sm max-w-sm" layout="month-and-year"
				:min-value="new CalendarDate(1925, 1, 1)" :max-value="new CalendarDate(2035, 1, 1)" />
		</div>

		<Separator />

		<div class="grid grid-cols-1 md:grid-cols-7 gap-4 items-start">
			<div v-for="day in weekDays" :key="day.dateString"
				class="p-4 border rounded-xl bg-muted/40 min-h-[420px] flex flex-col justify-between">
				<div>
					<div class="text-center border-b pb-3 mb-3">
						<div class="text-xs font-semibold text-muted-foreground uppercase tracking-wider">
							{{ day.dayName }}
						</div>
						<div class="text-2xl font-extrabold text-foreground mt-0.5">
							{{ day.dayNumber }}
						</div>

						<Button variant="outline" size="sm"
							class="mt-3 w-full text-xs font-medium h-8 text-primary border-primary/20 hover:bg-primary/5"
							@click="openAddModal(day.dateString)">
							+ Add Session
						</Button>
					</div>

					<div class="space-y-2">
						<div v-for="session in getSessionsForDay(day.dateString)" :key="session.id"
							@click="openEditModal(session)"
							class="p-3 text-xs bg-card text-card-foreground border rounded-lg shadow-sm hover:border-primary/50 transition-all cursor-pointer text-left group">
							<div class="font-bold text-foreground group-hover:text-primary transition-colors truncate"
								:title="session.subject_name">
								{{ session.subject_name }}
							</div>
							<div class="text-muted-foreground font-medium mt-1 flex items-center gap-1">
								<span>{{ formatTime(session.start_time) }}</span>
								<span>-</span>
								<span>{{ formatTime(session.end_time) }}</span>
							</div>
						</div>
					</div>
				</div>

				<div v-if="getSessionsForDay(day.dateString).length === 0"
					class="text-center text-muted-foreground/60 py-6 text-xs italic mt-auto">
					No sessions
				</div>
			</div>
		</div>

		<SessionModal v-model:open="isModalOpen" :session-data="selectedSession" :default-date="targetDate"
			@refresh="fetchWeekSessions" />
	</div>
</template>
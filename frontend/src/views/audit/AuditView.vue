<script setup>
import AuditDetail from '@/components/audit/AuditDetail.vue'
import { Badge } from '@/components/ui/badge'
import { Calendar } from '@/components/ui/calendar'
import { Input } from '@/components/ui/input'
import {
	Pagination,
	PaginationContent,
	PaginationItem,
	PaginationNext,
	PaginationPrevious,
} from '@/components/ui/pagination'
import {
	Popover,
	PopoverContent,
	PopoverTrigger,
} from '@/components/ui/popover'
import {
	Select,
	SelectContent,
	SelectItem,
	SelectTrigger,
	SelectValue,
} from '@/components/ui/select'
import {
	Table,
	TableBody,
	TableCell,
	TableHead,
	TableHeader,
	TableRow,
} from '@/components/ui/table'
import { useAuditStore } from '@/stores/audit.js'
import { formatAuditDetailPreview } from '@/utils/auditFormat'
import { CalendarIcon, Eye, Loader2, Search, X } from 'lucide-vue-next'
import { computed, onMounted, ref, watch } from 'vue'

const auditStore = useAuditStore()

const selectedAudit = ref(null)
const openDetail = ref(false)
const searchInput = ref('')
const searchTimeout = ref(null)

const localFilters = ref({
	action: 'all',
	target_model: '',
	search: '',
	date_from: '',
	date_to: '',
})

// Calendar state
const dateFrom = ref(null)
const dateTo = ref(null)
const openFrom = ref(false)
const openTo = ref(false)

function calendarDateToString(cd) {
	if (!cd) return ''
	return `${cd.year}-${String(cd.month).padStart(2, '0')}-${String(cd.day).padStart(2, '0')}`
}

function formatDisplayDate(dateStr) {
	if (!dateStr) return 'Pick a date'
	const [y, m, d] = dateStr.split('-')
	return new Date(y, m - 1, d).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}

watch(dateFrom, (val) => {
	localFilters.value.date_from = calendarDateToString(val)
	openFrom.value = false
	handleApplyFilters()
})

watch(dateTo, (val) => {
	localFilters.value.date_to = calendarDateToString(val)
	openTo.value = false
	handleApplyFilters()
})

// Target model suggestions
const targetModelSuggestions = [
	'Grade', 'Assessment', 'Student', 'Course', 'Subject',
	'Enrollment', 'Attendance', 'ClassSession',
]
const showSuggestions = ref(false)
const filteredSuggestions = computed(() => {
	const val = localFilters.value.target_model.toLowerCase()
	if (!val) return targetModelSuggestions
	return targetModelSuggestions.filter(s => s.toLowerCase().includes(val))
})

function selectSuggestion(s) {
	localFilters.value.target_model = s
	showSuggestions.value = false
	handleApplyFilters()
}

const hasActiveFilters = computed(() =>
	localFilters.value.action !== 'all'
	|| localFilters.value.target_model !== ''
	|| localFilters.value.search !== ''
	|| localFilters.value.date_from !== ''
	|| localFilters.value.date_to !== ''
)

onMounted(async () => {
	await auditStore.fetchAudits()
})

function syncFiltersFromStore() {
	localFilters.value = {
		...auditStore.filters,
		action: auditStore.filters.action || 'all',
	}
	searchInput.value = auditStore.filters.search || ''
}
syncFiltersFromStore()

// Debounced search
watch(searchInput, (val) => {
	clearTimeout(searchTimeout.value)
	searchTimeout.value = setTimeout(() => {
		localFilters.value.search = val
		handleApplyFilters()
	}, 400)
})

// Auto-apply on action change
watch(() => localFilters.value.action, () => handleApplyFilters())

async function handleApplyFilters() {
	const filters = { ...localFilters.value }
	if (filters.action === 'all') filters.action = ''
	await auditStore.applyFilters(filters)
}

async function handleClearFilters() {
	await auditStore.clearFilters()
	localFilters.value = { action: 'all', target_model: '', search: '', date_from: '', date_to: '' }
	searchInput.value = ''
	dateFrom.value = null
	dateTo.value = null
}

function clearDateFrom() {
	dateFrom.value = null
	localFilters.value.date_from = ''
	handleApplyFilters()
}

function clearDateTo() {
	dateTo.value = null
	localFilters.value.date_to = ''
	handleApplyFilters()
}

function handleViewDetail(audit) {
	selectedAudit.value = audit
	openDetail.value = true
}

function formatTimestamp(value) {
	if (!value) return '—'
	return new Date(value).toLocaleString('en-US', {
		year: 'numeric', month: 'short', day: 'numeric',
		hour: '2-digit', minute: '2-digit',
	})
}

function actionColor(action) {
	if (action === 'create') return 'bg-green-100 text-green-700'
	if (action === 'update') return 'bg-blue-100 text-blue-700'
	if (action === 'delete') return 'bg-red-100 text-red-700'
	return 'bg-neutral-100 text-neutral-700'
}

const totalPages = computed(() => Math.ceil(auditStore.count / (auditStore.pageSize || 10)))
</script>

<template>
	<div class="space-y-4">

		<!-- Filter bar -->
		<div class="flex flex-col gap-3 p-4 bg-white border border-neutral-200 rounded-lg shadow-xs">
			<div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-3">

				<!-- Search -->
				<div class="flex flex-col gap-1.5 sm:col-span-2 xl:col-span-1">
					<label class="text-xs font-medium text-neutral-500">Search</label>
					<div class="relative">
						<Search
							class="absolute left-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-neutral-400 pointer-events-none" />
						<Input v-model="searchInput" placeholder="Action, model, detail…" class="pl-8 pr-8" />
						<button v-if="searchInput"
							class="absolute right-2.5 top-1/2 -translate-y-1/2 text-neutral-400 hover:text-neutral-600"
							@click="searchInput = ''">
							<X class="w-3.5 h-3.5" />
						</button>
					</div>
				</div>

				<!-- Action -->
				<div class="flex flex-col gap-1.5">
					<label class="text-xs font-medium text-neutral-500">Action</label>
					<Select v-model="localFilters.action">
						<SelectTrigger class="w-full">
							<SelectValue placeholder="All actions" />
						</SelectTrigger>
						<SelectContent>
							<SelectItem value="all">All actions</SelectItem>
							<SelectItem value="create">Create</SelectItem>
							<SelectItem value="update">Update</SelectItem>
							<SelectItem value="delete">Delete</SelectItem>
						</SelectContent>
					</Select>
				</div>

				<!-- Target model with suggestions -->
				<div class="flex flex-col gap-1.5 relative">
					<label class="text-xs font-medium text-neutral-500">Target model</label>
					<Input v-model="localFilters.target_model" placeholder="e.g. Grade" autocomplete="off"
						@focus="showSuggestions = true" @blur="setTimeout(() => showSuggestions = false, 150)"
						@keyup.enter="handleApplyFilters" />
					<div v-if="showSuggestions && filteredSuggestions.length"
						class="absolute top-full left-0 right-0 mt-1 z-20 bg-white border border-neutral-200 rounded-md shadow-md overflow-hidden">
						<button v-for="s in filteredSuggestions" :key="s"
							class="w-full text-left px-3 py-2 text-sm hover:bg-neutral-50 transition-colors"
							@mousedown="selectSuggestion(s)">
							{{ s }}
						</button>
					</div>
				</div>

				<!-- Date range — two calendar popovers -->
				<div class="flex flex-col gap-1.5">
					<label class="text-xs font-medium text-neutral-500">Date range</label>
					<div class="flex gap-2 items-center">

						<!-- From -->
						<Popover v-model:open="openFrom">
							<PopoverTrigger as-child>
								<button
									class="flex-1 flex items-center gap-2 h-9 px-3 rounded-md border border-input bg-background text-sm text-left hover:bg-neutral-50 transition-colors min-w-0">
									<CalendarIcon class="w-3.5 h-3.5 text-neutral-400 shrink-0" />
									<span class="truncate text-xs"
										:class="localFilters.date_from ? 'text-neutral-900' : 'text-neutral-400'">
										{{ localFilters.date_from ? formatDisplayDate(localFilters.date_from) : 'From'
										}}
									</span>
									<X v-if="localFilters.date_from"
										class="w-3 h-3 text-neutral-400 hover:text-neutral-600 shrink-0 ml-auto"
										@click.stop="clearDateFrom" />
								</button>
							</PopoverTrigger>
							<PopoverContent class="w-auto p-0" align="start">
								<Calendar v-model="dateFrom" />
							</PopoverContent>
						</Popover>

						<span class="text-neutral-400 text-xs shrink-0">–</span>

						<!-- To -->
						<Popover v-model:open="openTo">
							<PopoverTrigger as-child>
								<button
									class="flex-1 flex items-center gap-2 h-9 px-3 rounded-md border border-input bg-background text-sm text-left hover:bg-neutral-50 transition-colors min-w-0">
									<CalendarIcon class="w-3.5 h-3.5 text-neutral-400 shrink-0" />
									<span class="truncate text-xs"
										:class="localFilters.date_to ? 'text-neutral-900' : 'text-neutral-400'">
										{{ localFilters.date_to ? formatDisplayDate(localFilters.date_to) : 'To' }}
									</span>
									<X v-if="localFilters.date_to"
										class="w-3 h-3 text-neutral-400 hover:text-neutral-600 shrink-0 ml-auto"
										@click.stop="clearDateTo" />
								</button>
							</PopoverTrigger>
							<PopoverContent class="w-auto p-0" align="start">
								<Calendar v-model="dateTo" />
							</PopoverContent>
						</Popover>

					</div>
				</div>
			</div>

			<!-- Active filter chips -->
			<div v-if="hasActiveFilters" class="flex flex-wrap gap-2 items-center pt-1 border-t border-neutral-100">
				<span class="text-xs text-neutral-400">Filters:</span>
				<Badge v-if="localFilters.action !== 'all'" variant="secondary"
					class="gap-1 cursor-pointer text-xs capitalize" @click="localFilters.action = 'all'">
					{{ localFilters.action }}
					<X class="w-3 h-3" />
				</Badge>
				<Badge v-if="localFilters.target_model" variant="secondary" class="gap-1 cursor-pointer text-xs"
					@click="localFilters.target_model = ''; handleApplyFilters()">
					{{ localFilters.target_model }}
					<X class="w-3 h-3" />
				</Badge>
				<Badge v-if="localFilters.search" variant="secondary" class="gap-1 cursor-pointer text-xs"
					@click="searchInput = ''">
					"{{ localFilters.search }}"
					<X class="w-3 h-3" />
				</Badge>
				<Badge v-if="localFilters.date_from" variant="secondary" class="gap-1 cursor-pointer text-xs"
					@click="clearDateFrom">
					From {{ formatDisplayDate(localFilters.date_from) }}
					<X class="w-3 h-3" />
				</Badge>
				<Badge v-if="localFilters.date_to" variant="secondary" class="gap-1 cursor-pointer text-xs"
					@click="clearDateTo">
					To {{ formatDisplayDate(localFilters.date_to) }}
					<X class="w-3 h-3" />
				</Badge>
				<button class="text-xs text-neutral-400 hover:text-neutral-600 underline ml-auto"
					@click="handleClearFilters">
					Clear all
				</button>
			</div>
		</div>

		<div v-if="auditStore.loading" class="flex items-center justify-center py-12 text-neutral-500">
			<Loader2 class="w-6 h-6 animate-spin mr-2" />
			Loading audit log…
		</div>

		<div v-else-if="auditStore.error" class="text-center py-12 text-red-500">
			{{ auditStore.error }}
		</div>

		<template v-else>
			<div class="rounded-lg border overflow-x-auto">
				<Table>
					<TableHeader>
						<TableRow>
							<TableHead class="w-40">Timestamp</TableHead>
							<TableHead class="w-24">Action</TableHead>
							<TableHead class="w-36">Target</TableHead>
							<TableHead class="hidden md:table-cell">Detail</TableHead>
							<TableHead class="w-16 text-center">View</TableHead>
						</TableRow>
					</TableHeader>
					<TableBody>
						<TableRow v-if="auditStore.audits.length === 0">
							<TableCell colspan="5" class="text-center py-10 text-neutral-500">
								No audit entries found.
							</TableCell>
						</TableRow>
						<TableRow v-for="audit in auditStore.audits" :key="audit.id" class="hover:bg-neutral-50">
							<TableCell class="text-sm text-neutral-600 whitespace-nowrap">
								{{ formatTimestamp(audit.timestamp) }}
							</TableCell>
							<TableCell>
								<Badge :class="actionColor(audit.action)" variant="secondary" class="capitalize">
									{{ audit.action }}
								</Badge>
							</TableCell>
							<TableCell class="font-medium whitespace-nowrap">
								{{ audit.target_model }} #{{ audit.target_id }}
							</TableCell>
							<TableCell class="text-sm text-neutral-500 max-w-xs truncate hidden md:table-cell">
								{{ formatAuditDetailPreview(audit.detail) }}
							</TableCell>
							<TableCell>
								<div class="flex justify-center">
									<button
										class="p-1.5 rounded hover:bg-neutral-100 hover:text-blue-500 transition-colors cursor-pointer"
										@click="handleViewDetail(audit)">
										<Eye class="w-4 h-4" />
									</button>
								</div>
							</TableCell>
						</TableRow>
					</TableBody>
				</Table>
			</div>

			<!-- Pagination -->
			<div v-if="auditStore.count > 0" class="flex items-center justify-between mt-4 gap-2 flex-wrap">
				<p class="text-xs text-neutral-500">
					Page {{ auditStore.currentPage }} of {{ totalPages }} &middot; {{ auditStore.count }} entries
				</p>
				<Pagination v-slot="{ page }" :total="auditStore.count" :items-per-page="auditStore.pageSize || 10"
					:page="auditStore.currentPage" @update:page="auditStore.goToPage($event)">
					<PaginationContent v-slot="{ items }">
						<PaginationPrevious class="cursor-pointer" />
						<template v-for="(item, index) in items" :key="index">
							<PaginationItem v-if="item.type === 'page'" :value="item.value"
								:is-active="item.value === page" class="cursor-pointer">
								{{ item.value }}
							</PaginationItem>
						</template>
						<PaginationNext class="cursor-pointer" />
					</PaginationContent>
				</Pagination>
			</div>
		</template>

		<AuditDetail :audit="selectedAudit" :open="openDetail" @update:open="openDetail = $event" />
	</div>
</template>
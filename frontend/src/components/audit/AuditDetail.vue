<script setup>
import { Badge } from '@/components/ui/badge'
import { Separator } from '@/components/ui/separator'
import {
	Sheet,
	SheetContent,
	SheetDescription,
	SheetHeader,
	SheetTitle,
} from '@/components/ui/sheet'

const props = defineProps({
	audit: {
		type: Object,
		default: null,
	},
	open: {
		type: Boolean,
		default: false,
	},
})

const emit = defineEmits(['update:open'])

function formatTimestamp(value) {
	if (!value) return '—'
	return new Date(value).toLocaleString('en-US', {
		year: 'numeric',
		month: 'short',
		day: 'numeric',
		hour: '2-digit',
		minute: '2-digit',
		second: '2-digit',
	})
}

function actionColor(action) {
	if (action === 'create') return 'bg-green-100 text-green-700'
	if (action === 'update') return 'bg-blue-100 text-blue-700'
	if (action === 'delete') return 'bg-red-100 text-red-700'
	return 'bg-neutral-100 text-neutral-700'
}

function isObject(val) {
	return val !== null && typeof val === 'object' && !Array.isArray(val)
}

function formatValue(val) {
	if (val === null || val === undefined) return '—'
	if (typeof val === 'object') return JSON.stringify(val)
	return String(val)
}
</script>

<template>
	<Sheet :open="open" @update:open="emit('update:open', $event)">
		<SheetContent class="sm:max-w-lg overflow-y-auto">

			<SheetHeader class="pb-4 border-b">
				<SheetTitle class="text-lg font-bold text-neutral-900">
					Audit Entry #{{ audit?.id }}
				</SheetTitle>
				<SheetDescription class="flex items-center gap-2 mt-1">
					<Badge :class="actionColor(audit?.action)" variant="secondary" class="capitalize">
						{{ audit?.action }}
					</Badge>
					<span class="text-xs text-neutral-400">{{ formatTimestamp(audit?.timestamp) }}</span>
				</SheetDescription>
			</SheetHeader>

			<div v-if="audit" class="mt-6 space-y-6 px-4 ">

				<!-- Meta -->
				<div class="space-y-3">
					<div class="flex justify-between text-sm">
						<span class="text-neutral-500">Teacher</span>
						<span class="font-medium text-neutral-900">{{ audit.teacher?.username || '—' }}</span>
					</div>
					<div v-if="audit.teacher?.school_name" class="flex justify-between text-sm">
						<span class="text-neutral-500">School</span>
						<span class="font-medium text-neutral-900">{{ audit.teacher.school_name }}</span>
					</div>
					<div class="flex justify-between text-sm">
						<span class="text-neutral-500">Target</span>
						<span class="font-medium text-neutral-900">{{ audit.target_model }} #{{ audit.target_id
							}}</span>
					</div>
				</div>

				<Separator />

				<!-- Detail -->
				<div class="space-y-3">
					<p class="text-sm font-semibold text-neutral-900">Change Detail</p>

					<div v-if="!audit.detail" class="text-sm text-muted-foreground italic">
						No detail recorded.
					</div>

					<div v-else class="space-y-3">
						<!-- Before -->
						<div v-if="audit.detail.before !== undefined" class="rounded-lg border bg-red-50/60 p-3">
							<p class="text-[11px] font-semibold text-red-500 uppercase tracking-wide mb-2">Before</p>
							<!-- If before is an object, iterate its keys -->
							<div v-if="isObject(audit.detail.before)" class="space-y-1.5">
								<div v-for="(value, key) in audit.detail.before" :key="key"
									class="flex justify-between text-xs gap-4">
									<span class="text-muted-foreground capitalize shrink-0">{{ String(key).replace(/_/g,
										' ') }}</span>
									<span class="font-medium text-neutral-800 text-right break-all">{{
										formatValue(value) }}</span>
								</div>
							</div>
							<!-- If before is a plain value (string/number) -->
							<p v-else class="text-xs font-medium text-neutral-800">{{ formatValue(audit.detail.before)
								}}</p>
						</div>

						<!-- After -->
						<div v-if="audit.detail.after !== undefined" class="rounded-lg border bg-green-50/60 p-3">
							<p class="text-[11px] font-semibold text-green-600 uppercase tracking-wide mb-2">After</p>
							<div v-if="isObject(audit.detail.after)" class="space-y-1.5">
								<div v-for="(value, key) in audit.detail.after" :key="key"
									class="flex justify-between text-xs gap-4">
									<span class="text-muted-foreground capitalize shrink-0">{{ String(key).replace(/_/g,
										' ') }}</span>
									<span class="font-medium text-neutral-800 text-right break-all">{{
										formatValue(value) }}</span>
								</div>
							</div>
							<p v-else class="text-xs font-medium text-neutral-800">{{ formatValue(audit.detail.after) }}
							</p>
						</div>

						<!-- Fallback: no before/after keys at all -->
						<div v-if="audit.detail.before === undefined && audit.detail.after === undefined"
							class="rounded-lg border bg-neutral-50 p-3">
							<div v-if="isObject(audit.detail)" class="space-y-1.5">
								<div v-for="(value, key) in audit.detail" :key="key"
									class="flex justify-between text-xs gap-4">
									<span class="text-muted-foreground capitalize shrink-0">{{ String(key).replace(/_/g,
										' ') }}</span>
									<span class="font-medium text-neutral-800 text-right break-all">{{
										formatValue(value) }}</span>
								</div>
							</div>
							<p v-else class="text-xs font-medium text-neutral-800">{{ formatValue(audit.detail) }}</p>
						</div>
					</div>
				</div>

			</div>

		</SheetContent>
	</Sheet>
</template>
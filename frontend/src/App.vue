<script setup>
import { Toaster } from 'vue-sonner';
</script>

<template>
	<RouterView />
	<!-- Added placement, color themes, and a close button helper -->
	<Toaster position="bottom-right" richColors closeButton />
</template>
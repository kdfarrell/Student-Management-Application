<script setup>
import { Toaster } from 'vue-sonner'
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50">
    <div class="w-full max-w-md">
      <RouterView />
    </div>
  </div>
  <Toaster position="bottom-right" richColors closeButton />
</template>
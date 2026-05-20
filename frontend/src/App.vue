<script setup>
import { Toaster } from 'vue-sonner'
</script>

<template>
  <RouterView />
  
  <Toaster 
    position="bottom-right"
    richColors
    closeButton
    duration="4000"
    :visible-toasts="5"
    theme="light"
  />
</template>
<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import AIfloating from './components/AIfloating.vue'
</script>

<template>
  <div id="app">
    <RouterView />
  </div>
  <AIfloating />
</template>

<style scoped></style>

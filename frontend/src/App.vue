<script setup>
import { RouterView } from 'vue-router'
import Footer from './components/Footer.vue'
</script>

<template>
  <div class="app-container">
    <RouterView />
    <Footer />
  </div>
</template>

<style>
.page-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.page-container > *:last-child {
  margin-top: auto;
}
</style>

<script setup>
import { RouterView } from 'vue-router'
import Footer from './components/Footer.vue'
</script>

<template>
  <div class="app-container">
    <div class="main-content">
      <RouterView />
    </div>
    <Footer />
  </div>
</template>

<style>
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}
</style>
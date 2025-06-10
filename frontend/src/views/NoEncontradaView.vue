<template>
  <div class="noencontrada">
    <p>La página que buscas no existe.</p>
    <router-link to="/">Volver al inicio</router-link>
  </div>
</template>

<script setup>
</script>

<style scoped>
.noencontrada {
  text-align: center;
  margin-top: 10vh;
}

p {
  font-size: 1.5rem;
  margin-bottom: 2rem;
}
a {
  color: #1976d2;
  text-decoration: underline;
}
</style>
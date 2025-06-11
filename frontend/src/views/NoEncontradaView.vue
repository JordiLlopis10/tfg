<template>
  <div class="noencontrada">
    <img 
      src="/404.png" 
      alt="Página no encontrada" 
      class="imagen-404"
    />
    <p>La página que buscas no existe.</p>
    <router-link to="/">Volver al inicio</router-link>
  </div>
</template>

<script setup>
</script>

<style scoped>
.noencontrada {
  text-align: center;
  margin-top: 5vh;
  padding: 2rem;
}

.imagen-404 {
  max-width: 300px;
  margin-bottom: 2rem;
  border-radius: 10px;
}

p {
  font-size: 1.5rem;
  margin-bottom: 2rem;
}

a {
  color: #1976d2;
  text-decoration: underline;
  font-size: 1.1rem;
}


a:hover {
  color: #1565c0;
}
</style>
<template>
  <div>
    <header class="header">
      <img src="/logo.png" alt="Logo" class="logo" />
      <nav class="nav">
        <RouterLink to="/">Inicio</RouterLink>
        <RouterLink to="/noticias">Noticias</RouterLink>
        <RouterLink to="/tienda">Tienda</RouterLink>
        <RouterLink to="/carrito">Carrito</RouterLink>
        <RouterLink to="/login">Inicio Sesión</RouterLink>
      </nav>
    </header>
    <h2>Bienvenido a tu perfil</h2>
    <p>Has iniciado sesión correctamente.</p>
  </div>
</template>


<script setup>

</script>

<style scoped>
.header {
  background-color: #eac6c6;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  height: 60px;
}

.nav {
  display: flex;
  gap: 1.5rem;
  font-weight: bold;
}

.nav a {
  color: #000;
  text-decoration: none;
  font-size: 0.9rem;
}

.nav a:hover {
  text-decoration: underline;
}


</style>
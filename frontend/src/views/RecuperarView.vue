<template>
  <div>
    <header class="header">
      <RouterLink to="/">
        <img src="/logo.png" alt="Logo" class="logo" />
      </RouterLink>

      <button class="hamburger" @click="menuVisible = !menuVisible">
        ☰
      </button>

      <nav class="nav" :class="{ open: menuVisible }">
        <RouterLink to="/" @click="menuVisible = false">Inicio</RouterLink>
        <RouterLink to="/tienda" @click="menuVisible = false">Tienda</RouterLink>
        <RouterLink to="/carrito" @click="menuVisible = false">Carrito</RouterLink>
        <RouterLink to="/contacto" @click="menuVisible = false">Contacto</RouterLink>
      </nav>
    </header>
  <div class="form-container">
    <h2>Recuperar Contraseña</h2>
    <form @submit.prevent="solicitarRecuperacion">
      <input v-model="email" type="email" placeholder="Correo electrónico" required />
      <button type="submit">Enviar enlace</button>
      <p v-if="mensaje" class="success">{{ mensaje }}</p>
      <p v-if="error" class="error">{{ error }}</p>
    </form>
  </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const email = ref('')
const mensaje = ref('')
const error = ref('')
const menuVisible = ref(false)

async function solicitarRecuperacion() {
  mensaje.value = ''
  error.value = ''
  try {
    const res = await fetch('https://detallspatch.onrender.com/recuperar', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: email.value })
    })
    const data = await res.json()
    if (!res.ok) {
      error.value = data.error || 'Algo salió mal'
    } else {
      mensaje.value = data.message
      email.value = ''
    }
  } catch (e) {
    error.value = 'Error al conectar con el servidor'
  }
}
</script>

<style scoped>
.header {
  background-color: #eac6c6;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
}

.logo {
  height: 60px;
}

.hamburger {
  display: none;
  font-size: 1.8rem;
  background: none;
  border: none;
  cursor: pointer;
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

@media (max-width: 768px) {
  .hamburger {
    display: block;
  }

  .nav {
    display: none;
    flex-direction: column;
    position: absolute;
    top: 100%;
    right: 0;
    background-color: #f4dada;
    width: 100%;
    padding: 1rem 2rem;
    box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.1);
    z-index: 10;
    text-align: center;
  }

  .nav.open {
    display: flex;
  }

  .nav a {
    font-size: 1.1rem;
    padding: 0.5rem 0;
  }
  
}

.form-container {
  max-width: 400px;
  margin: 4rem auto;
  background: #fff7f7;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 0 8px rgba(0, 0, 0, 0.05);
  text-align: center;
}
input, button {
  width: 100%;
  padding: 0.75rem;
  margin: 0.5rem 0;
  border-radius: 6px;
}
button {
  background-color: #eac6c6;
  border: none;
  cursor: pointer;
}
.success { color: green; }
.error { color: red; }
</style>

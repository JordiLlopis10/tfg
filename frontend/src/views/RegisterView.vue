<template>
  <div class="carrito-container">
    <header class="header">
      <RouterLink to="/">
        <img src="/logo.png" alt="Logo" class="logo" />
      </RouterLink>

      <button class="hamburger" @click="menuVisible = !menuVisible">☰</button>

      <nav class="nav" :class="{ open: menuVisible }">
        <RouterLink to="/" @click="menuVisible = false">Inicio</RouterLink>
        <RouterLink to="/tienda" @click="menuVisible = false">Tienda</RouterLink>
        <RouterLink to="/carrito" @click="menuVisible = false">Carrito</RouterLink>
        <RouterLink to="/contacto" @click="menuVisible = false">Contacto</RouterLink>
      </nav>
    </header>

    <div class="form-container">
      <h2>Registrar nuevo usuario</h2>
      <form @submit.prevent="handleRegister">
        <input v-model="email" type="email" placeholder="Correo electrónico" required />
        <input v-model="password" type="password" placeholder="Contraseña" required />


        <button type="submit">Crear Usuario</button>
        <p v-if="error" class="error-msg">{{ error }}</p>
        <p v-if="success" class="success-msg">{{ success }}</p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const email = ref('')
const password = ref('')
const error = ref('')
const success = ref('')
const router = useRouter()
const menuVisible = ref(false)

onMounted(async () => {
  try {
    const res = await fetch('https://detallspatch.onrender.com/auth/user', {
      credentials: 'include'
    });
    if (!res.ok) {
      router.push('/');
      return;
    }
    const user = await res.json();
    if (user.email !== 'pedritoue2@gmail.com') {
      router.push('/');
    }
  } catch {
    router.push('/');
  }
});

const handleRegister = async () => {
  error.value = ''
  success.value = ''

  const payload = {
    email: email.value,
    password: password.value,
  }

  try {
    const response = await fetch('https://detallspatch.onrender.com/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })

    const data = await response.json()

    if (!response.ok) {
      error.value = data.error || 'Registro fallido'
    } else {
      success.value = data.message
      email.value = ''
      password.value = ''
    }
  } catch (err) {
    error.value = 'Error al conectar con el servidor'
  }
}
</script>

<style scoped>
.auth-container {
  font-family: 'Arial', sans-serif;
  background-color: #ffffff;
  min-height: 100vh;
}

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
  background-color: #fff7f7;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 0 12px rgba(0, 0, 0, 0.05);
  text-align: center;
}

form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 1rem;
}

input, select {
  padding: 0.75rem;
  border-radius: 6px;
  border: 1px solid #ccc;
  font-size: 1rem;
}

button {
  padding: 0.75rem;
  background-color: #eac6c6;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
}

button:hover {
  background-color: #d5a8a8;
}

.error-msg {
  color: red;
}

.success-msg {
  color: green;
}
</style>

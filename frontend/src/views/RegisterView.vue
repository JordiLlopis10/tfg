<template>
  <div class="auth-container">
    <header class="header">
      <RouterLink to="/">
        <img src="/logo.png" alt="Logo" class="logo" />
      </RouterLink>
      <nav class="nav">
        <RouterLink to="/">Inicio</RouterLink>
        <RouterLink to="/tienda">Tienda</RouterLink>
        <RouterLink to="/carrito">Carrito</RouterLink>
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

onMounted(() => {
  const isAdmin = localStorage.getItem('admin-auth') === 'true'
  if (!isAdmin) {
    router.push('/')
  }
})

const handleRegister = async () => {
  error.value = ''
  success.value = ''

  const payload = {
    email: email.value,
    password: password.value,
  }

  try {
    const response = await fetch('http://localhost:5000/register', {
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

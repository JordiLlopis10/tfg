<template>
  <div class="home-container">
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
      <h2>Iniciar sesión</h2>
      <form @submit.prevent="login">
        <input v-model="email" type="email" placeholder="Correo electrónico" required />
        <input v-model="password" type="password" placeholder="Contraseña" required />
        <button type="submit">Iniciar sesión</button>
        <p v-if="error" class="error-msg">{{ error }}</p>
        <p v-if="success" class="success-msg">{{ success }}</p>
        <p class="recuperar">
          <RouterLink to="/recuperar">¿Olvidaste tu contraseña?</RouterLink>
        </p>
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

const admins = ['pedritoue2@gmail.com', 'llopisgodinojordi@gmail.com']

onMounted(() => {
  const isAdmin = localStorage.getItem('admin-auth') === 'true'
  if (isAdmin) {
    router.push('/admin')
  }
})

const login = async () => {
  error.value = ''
  success.value = ''

  try {
    const response = await fetch('http://localhost:5000/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ email: email.value, password: password.value })
    })

    const data = await response.json()

    if (response.ok) {
      localStorage.setItem('token', data.token)

      if (admins.includes(email.value)) {
        localStorage.setItem('admin-auth', 'true')
        success.value = 'Bienvenido administrador'
        router.push('/admin')
      } else {
        error.value = 'Este usuario no tiene acceso como administrador'
        localStorage.removeItem('admin-auth')
      }
    } else {
      error.value = data.error || 'Credenciales incorrectas'
    }
  } catch (err) {
    error.value = 'No se pudo conectar con el servidor'
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
    .portada-texto {
    font-size: 1.1rem;
    padding: 1rem 1.2rem;
    width: 80%;
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
}

input {
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

.recuperar {
  margin-top: 1rem;
  font-size: 0.9rem;
}
.recuperar a {
  color: #333;
  text-decoration: underline;
}

</style>

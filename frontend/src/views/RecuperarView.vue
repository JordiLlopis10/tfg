<template>
  <div class="form-container">
    <h2>Recuperar Contraseña</h2>
    <form @submit.prevent="solicitarRecuperacion">
      <input v-model="email" type="email" placeholder="Correo electrónico" required />
      <button type="submit">Enviar enlace</button>
      <p v-if="mensaje" class="success">{{ mensaje }}</p>
      <p v-if="error" class="error">{{ error }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const email = ref('')
const mensaje = ref('')
const error = ref('')

async function solicitarRecuperacion() {
  mensaje.value = ''
  error.value = ''
  try {
    const res = await fetch('http://localhost:5000/recuperar', {
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

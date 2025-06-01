<template>
  <div class="form-container">
    <h2>Establecer Nueva Contraseña</h2>
    <form @submit.prevent="resetear">
      <input v-model="password" type="password" placeholder="Nueva contraseña" required />
      <button type="submit">Restablecer</button>
      <p v-if="mensaje" class="success">{{ mensaje }}</p>
      <p v-if="error" class="error">{{ error }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const password = ref('')
const mensaje = ref('')
const error = ref('')
const route = useRoute()
const router = useRouter()
const token = ref('')

onMounted(async () => {
  token.value = route.params.token

  try {
    const res = await fetch(`http://localhost:5000/resetear/${token.value}`, {
      method: 'GET',
    })
    const data = await res.json()
    if (!res.ok) {
      router.push('/login')
    }
  } catch (e) {
    router.push('/login')
  }
})

async function resetear() {
  mensaje.value = ''
  error.value = ''
  try {
    const res = await fetch(`http://localhost:5000/resetear/${token.value}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ password: password.value })
    })
    const data = await res.json()
    if (!res.ok) {
      error.value = data.error || 'No se pudo restablecer'
    } else {
      mensaje.value = data.message
      password.value = ''

      setTimeout(() => {
        router.push('/')
      }, 3000)
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

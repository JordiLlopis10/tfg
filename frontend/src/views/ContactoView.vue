<template>
  <div class="pasarela-container">
    <header class="header">
      <RouterLink to="/">
        <img src="/logo.png" alt="Logo" class="logo" />
      </RouterLink>
      <nav class="nav">
        <RouterLink to="/">Inicio</RouterLink>
        <RouterLink to="/tienda">Tienda</RouterLink>
        <RouterLink to="/carrito">Carrito</RouterLink>
        <RouterLink to="/contacto">Contacto</RouterLink>
      </nav>
    </header>

    <div class="contenido">
      <h2 class="titulo">Contacto para Artículos Personalizados</h2>

      <form @submit.prevent="enviarFormulario" class="form-pago">
        <div class="campo">
          <label for="nombre">Tu nombre</label>
          <input id="nombre" v-model="nombre" type="text" required placeholder="Raul Navarro" />
        </div>

        <div class="campo">
          <label for="email">Correo electrónico</label>
          <input id="email" v-model="email" type="email" required placeholder="raulnavarro@gmail.com" />
        </div>

        <div class="campo">
          <label for="mensaje">Mensaje</label>
          <textarea
            id="mensaje"
            v-model="mensaje"
            rows="5"
            placeholder="Describe el artículo personalizado que deseas... O cualquier otra consulta"
            required
          ></textarea>
        </div>

        <button type="submit" class="btn">Enviar Mensaje</button>

        <p v-if="confirmacion" class="mensaje">{{ confirmacion }}</p>
        <p v-if="error" class="mensaje error">{{ error }}</p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const nombre = ref("")
const email = ref("")
const mensaje = ref("")
const confirmacion = ref("")
const error = ref("")

async function enviarFormulario() {
  confirmacion.value = ""
  error.value = ""

  try {
    const res = await fetch("http://localhost:5000/contacto", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({
        nombre: nombre.value,
        email: email.value,
        mensaje: mensaje.value
      })
    });

    const data = await res.json();

    if (res.ok) {
      confirmacion.value = `Gracias, ${nombre.value}. Tu mensaje ha sido enviado correctamente.`;
      nombre.value = "";
      email.value = "";
      mensaje.value = "";
    } else {
      error.value = data.error || "Hubo un error al enviar el mensaje.";
    }
  } catch (err) {
    error.value = "No se pudo conectar con el servidor.";
  }
}
</script>

<style scoped>
.pasarela-container {
  font-family: "Arial", sans-serif;
  background-color: #fff;
  min-height: 100vh;
  color: #000;
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

.contenido {
  max-width: 600px;
  margin: 3rem auto;
  padding: 2rem 2rem;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 0 10px #aaa;
  border: 1px solid #000;
}

.titulo {
  margin-bottom: 2rem;
  font-size: 2rem;
  text-align: center;
  font-weight: 700;
  color: #000;
}

.form-pago {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

.campo {
  display: flex;
  flex-direction: column;
  font-size: 1rem;
}

.campo label {
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #000;
}

.campo input,
.campo textarea {
  padding: 0.7rem 1rem;
  border: 1.5px solid #000;
  border-radius: 6px;
  font-size: 1rem;
  outline-offset: 2px;
  transition: border-color 0.3s ease;
  color: #000;
  background: #fff;
  resize: none;
}

.campo input:focus,
.campo textarea:focus {
  border-color: #333;
  outline: none;
  box-shadow: 0 0 6px #555;
}

.btn {
  margin-top: 1.5rem;
  background-color: #000;
  color: #fff;
  padding: 0.85rem 1.5rem;
  border: none;
  border-radius: 6px;
  font-size: 1.1rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
  font-weight: 700;
}

.btn:hover {
  background-color: #EAC6C6;
}

.mensaje {
  margin-top: 2rem;
  font-size: 1.1rem;
  font-weight: 700;
  color: #000;
  text-align: center;
}

.mensaje.error {
  color: red;
}
</style>

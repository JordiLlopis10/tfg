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

    <div class="contenido">
      <h2 class="titulo">Pasarela de Pago</h2>

      <form v-if="!emailConfirmado" @submit.prevent="confirmarEmail" class="form-email">
        <div class="campo">
          <label for="email">Introduce tu dirección Gmail</label>
          <input
            id="email"
            v-model="email"
            type="email"
            placeholder="ejemplo@gmail.com"
            required
          />
        </div>
        <button type="submit" :disabled="!emailValido" class="btn">
          Confirmar Email
        </button>
      </form>

      <form v-else @submit.prevent="procesarPago" class="form-pago">
        <div class="campo">
          <label for="direccion">Dirección de envío</label>
          <input
            id="direccion"
            v-model="direccion"
            type="text"
            placeholder="Calle Paraiso 123"
            required
          />
        </div>

        <div class="campo">
          <label for="ciudad">Ciudad</label>
          <input
            id="ciudad"
            v-model="ciudad"
            type="text"
            placeholder="Valencia"
            required
          />
        </div>

        <div class="campos-pequenos">
          <div class="campo">
            <label for="cp">Código Postal</label>
            <input
              id="cp"
              v-model="cp"
              type="text"
              maxlength="5"
              placeholder="46021"
              required
            />
          </div>

          <div class="campo">
            <label for="provincia">Provincia</label>
            <input
              id="provincia"
              v-model="provincia"
              type="text"
              placeholder="Valencia"
              required
            />
          </div>
        </div>

        <div class="campo">
          <label for="nombre">Nombre en la tarjeta</label>
          <input
            id="nombre"
            v-model="nombre"
            type="text"
            placeholder="Juan Pérez"
            required
          />
        </div>

        <div class="campo">
          <label for="numero">Número de la tarjeta</label>
          <input
            id="numero"
            v-model="numero"
            type="text"
            maxlength="19"
            placeholder="1234 5678 9012 3456"
            @input="formatNumero"
            required
          />
        </div>

        <div class="campos-pequenos">
          <div class="campo">
            <label for="fecha">Fecha de expiración</label>
            <input
              id="fecha"
              v-model="fecha"
              type="text"
              maxlength="5"
              placeholder="MM/AA"
              @input="formatFecha"
              required
            />
          </div>

          <div class="campo">
            <label for="cvc">CVC</label>
            <input
              id="cvc"
              v-model="cvc"
              type="text"
              maxlength="4"
              placeholder="123"
              required
            />
          </div>
        </div>

        <button
          type="submit"
          :disabled="procesando || !formValido"
          class="btn"
        >
          {{ procesando ? "Procesando..." : "Pagar" }}
        </button>
      </form>

      <p v-if="mensaje" class="mensaje">{{ mensaje }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue"
import { useRouter } from "vue-router"

const router = useRouter()
const menuVisible = ref(false)

const email = ref("")
const emailConfirmado = ref(false)
const nombre = ref("")
const numero = ref("")
const fecha = ref("")
const cvc = ref("")
const direccion = ref("")
const ciudad = ref("")
const cp = ref("")
const provincia = ref("")
const procesando = ref(false)
const mensaje = ref("")
const carrito = ref([])

onMounted(() => {
  const data = localStorage.getItem('carrito')
  carrito.value = data ? JSON.parse(data) : []
})

const emailValido = computed(() => {
  return /^[a-zA-Z0-9._%+-]+@gmail\.com$/.test(email.value)
})

const formValido = computed(() => {
  return (
    nombre.value.trim().length > 3 &&
    /^\d{4} \d{4} \d{4} \d{4}$/.test(numero.value) &&
    /^(0[1-9]|1[0-2])\/\d{2}$/.test(fecha.value) &&
    /^\d{3,4}$/.test(cvc.value) &&
    direccion.value.trim().length > 5 &&
    ciudad.value.trim().length > 2 &&
    provincia.value.trim().length > 2 &&
    /^\d{5}$/.test(cp.value)
  )
})

function confirmarEmail() {
  if (!emailValido.value) return
  emailConfirmado.value = true
  mensaje.value = ""
}

function formatNumero() {
  let val = numero.value.replace(/\D/g, "").substring(0, 16)
  let bloques = val.match(/.{1,4}/g)
  numero.value = bloques ? bloques.join(" ") : ""
}

function formatFecha() {
  let val = fecha.value.replace(/\D/g, "").substring(0, 4)
  if (val.length >= 3) {
    fecha.value = val.substring(0, 2) + "/" + val.substring(2, 4)
  } else {
    fecha.value = val
  }
}

async function procesarPago() {
  if (!formValido.value) return

  procesando.value = true
  mensaje.value = ""

  const total = carrito.value.reduce(
    (acc, item) => acc + item.precio * item.cantidad,
    0
  )

  try {
    const res = await fetch("https://detallspatch.onrender.com/pago", {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email: email.value,
        carrito: carrito.value,
        total,
        direccion: direccion.value,
        ciudad: ciudad.value,
        cp: cp.value,
        provincia: provincia.value,
      }),
    })

    const data = await res.json()

    if (res.ok) {
      mensaje.value = `¡Pago realizado con éxito, ${nombre.value}! Gracias por tu compra.`
      localStorage.removeItem('carrito')

      nombre.value = ""
      numero.value = ""
      fecha.value = ""
      cvc.value = ""
      direccion.value = ""
      ciudad.value = ""
      cp.value = ""
      provincia.value = ""
      emailConfirmado.value = false
      email.value = ""

      setTimeout(() => {
        router.push("/")
      }, 5000)
    } else {
      mensaje.value = data.error || "Error al procesar el pago"
    }
  } catch (err) {
    mensaje.value = "Error de conexión con el servidor"
  }

  procesando.value = false
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
.pasarela-container {
  font-family: "Arial", sans-serif;
  background-color: #fff;
  min-height: 100vh;
  color: #000;
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

.form-email,
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

.campo input {
  padding: 0.7rem 1rem;
  border: 1.5px solid #000;
  border-radius: 6px;
  font-size: 1rem;
  outline-offset: 2px;
  transition: border-color 0.3s ease;
  color: #000;
  background: #fff;
}

.campo input:focus {
  border-color: #333;
  outline: none;
  box-shadow: 0 0 6px #555;
}

.campos-pequenos {
  display: flex;
  gap: 1rem;
}

.campos-pequenos .campo {
  flex: 1;
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

.btn:disabled {
  background-color: #555;
  cursor: not-allowed;
}

.btn:not(:disabled):hover {
  background-color: #222;
}

.mensaje {
  margin-top: 2rem;
  font-size: 1.2rem;
  font-weight: 700;
  color: #000;
  text-align: center;
}
</style>

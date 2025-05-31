<template>
  <div class="carrito-container">
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
      <h2>Tu carrito</h2>
      <div v-if="carrito.length === 0">
        <p>No hay productos en el carrito.</p>
      </div>
      <div v-else class="lista-carrito">
        <div v-for="(item, index) in carrito" :key="item.id" class="item-carrito">
          <img :src="item.imagen" alt="Producto" class="img-carrito" />
          <div class="info-item">
            <h4>{{ item.nombre }}</h4>
            <p>Precio por unidad: {{ item.precio }} €</p>

            <div class="cantidad-controles">
              <button @click="reducirCantidad(index)">➖</button>
              <span>{{ item.cantidad }}</span>
              <button @click="aumentarCantidad(index)">➕</button>
            </div>

            <p>Total: {{ (item.precio * item.cantidad).toFixed(2) }} €</p>
            <button class="eliminar-btn" @click="eliminarItem(index)">Eliminar</button>
          </div>
        </div>

        <div class="total">
          <p><strong>Total del carrito:</strong> {{ totalCarrito }} €</p>
        </div>
        <div class="finalizar-compra">
          <button class="finalizar-btn" @click="finalizarCompra">Finalizar compra</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const carrito = ref([])

onMounted(() => {

  const data = localStorage.getItem('carrito')
  carrito.value = data ? JSON.parse(data) : []
})

const guardarEnLocalStorage = () => {
  localStorage.setItem('carrito', JSON.stringify(carrito.value))
}

const aumentarCantidad = (index) => {
  carrito.value[index].cantidad++
  guardarEnLocalStorage()
}

const reducirCantidad = (index) => {
  if (carrito.value[index].cantidad > 1) {
    carrito.value[index].cantidad--
  } else {
    carrito.value.splice(index, 1)
  }
  guardarEnLocalStorage()
}

const eliminarItem = (index) => {
  carrito.value.splice(index, 1)
  guardarEnLocalStorage()
}

const totalCarrito = computed(() =>
  carrito.value.reduce((acc, item) => acc + item.precio * item.cantidad, 0).toFixed(2)
)

const finalizarCompra = () => {
  if (carrito.value.length === 0) return
  router.push('/pago')
}
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

.carrito-container {
  font-family: 'Arial', sans-serif;
  background-color: #fff;
  min-height: 100vh;
}

.contenido {
  padding: 2rem;
  max-width: 1100px;
  margin: 0 auto;
}

.contenido h2 {
  margin-bottom: 1.5rem;
  font-size: 1.8rem;
  color: #111;
}

.lista-carrito {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.item-carrito {
  display: flex;
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 12px;
  padding: 1rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
  gap: 1rem;
  align-items: center;
}

.img-carrito {
  width: 100px;
  border-radius: 8px;
  border: 1px solid #eee;
}

.info-item {
  flex: 1;
}

.cantidad-controles {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin: 0.5rem 0;
}

.cantidad-controles button {
  background-color: #f0f0f0;
  border: 1px solid #ccc;
  padding: 0.3rem 0.6rem;
  border-radius: 4px;
  cursor: pointer;
}

.eliminar-btn {
  margin-top: 0.5rem;
  background-color: #ffe5e5;
  border: none;
  padding: 0.4rem 0.8rem;
  border-radius: 5px;
  cursor: pointer;
  color: #a00;
}

.eliminar-btn:hover {
  background-color: #ffcccc;
}

.total {
  text-align: right;
  font-size: 1.2rem;
  font-weight: bold;
  margin-top: 1rem;
}

.finalizar-compra {
  display: flex;
  justify-content: flex-end;
  margin-top: 1rem;
}

.finalizar-btn {
  background-color: #111;
  color: white;
  padding: 0.8rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.finalizar-btn:hover {
  background-color: #333;
}
</style>

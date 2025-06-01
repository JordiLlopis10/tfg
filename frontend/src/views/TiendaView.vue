<template>
  <div>
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

    <main class="tienda-panel">
      <h1>Tienda</h1>

      <div class="productos-grid">
        <div
          v-for="producto in productos"
          :key="producto.id"
          class="producto-card"
          @click="irADetalle(producto.id)"
        >
          <img :src="producto.imagen" alt="Imagen producto" />
          <h3>{{ producto.nombre }}</h3>
          <p>{{ producto.precio }} €</p>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const productos = ref([])
const router = useRouter()

onMounted(async () => {
  try {
    const res = await fetch('http://localhost:5000/tienda')
    if (!res.ok) throw new Error('Error al cargar los productos')
    productos.value = await res.json()
  } catch (error) {
    alert(error.message)
  }
})

function irADetalle(id) {
  router.push(`/tienda/producto/${id}`)
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

.tienda-panel {
  max-width: 1440px;
  margin: 2rem auto;
  padding: 1rem;
  background-color: #fff7f7;
  border-radius: 16px;
  box-shadow: 0 0 12px rgba(0, 0, 0, 0.05);
  text-align: center;
}

.productos-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 1.5rem;
  justify-items: center;
  margin-top: 2rem;
}

.producto-card {
  width: 180px;
  background-color: #ffffff;
  border: 1px solid #ddd;
  border-radius: 10px;
  padding: 0.75rem;
  text-align: center;
  cursor: pointer;
  transition: transform 0.2s ease;
}

.producto-card:hover {
  transform: scale(1.03);
}

.producto-card img {
  width: 100%;
  height: 160px;
  object-fit: cover;
  border-radius: 6px;
  margin-bottom: 0.5rem;
}

.producto-card h3 {
  font-size: 0.95rem;
  margin: 0.5rem 0 0.25rem;
}

.producto-card p {
  font-weight: bold;
  color: #333;
  font-size: 0.85rem;
}
</style>

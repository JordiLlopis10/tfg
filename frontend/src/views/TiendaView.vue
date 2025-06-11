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

    <main class="tienda-panel">
      <h1>Tienda</h1>

      <div class="productos-fila">
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
const menuVisible = ref(false)

onMounted(async () => {
  try {
    const res = await fetch('https://detallspatch.onrender.com/tienda')
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

.tienda-panel {
  max-width: 1440px;
  margin: 2rem auto;
  padding: 1rem;
  background-color: #fff7f7;
  border-radius: 16px;
  box-shadow: 0 0 12px rgba(0, 0, 0, 0.05);
  text-align: center;
}

.productos-fila {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  justify-content: center;
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

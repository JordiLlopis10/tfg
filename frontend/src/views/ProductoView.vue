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

    <div v-if="producto" class="detalle-producto">
      <div class="producto-main">
        <div class="galeria">
          <img :src="producto.imagen" alt="Imagen producto" class="imagen-principal" />
        </div>

        <div class="info">
          <h1>{{ producto.nombre }}</h1>
          <p class="descripcion">{{ producto.descripcion }}</p>
          <p class="precio"><strong>Precio:</strong> {{ producto.precio }} €</p>

          <div class="acciones">
            <input type="number" v-model="cantidad" min="1" />
            <button @click="añadirAlCarrito" :disabled="cantidad <= 0">
              AÑADIR AL CARRITO
            </button>
          </div>

          <p v-if="mensajeVisible" class="mensaje-carrito">Añadido al carrito correctamente</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const producto = ref(null)
const cantidad = ref(1)
const mensajeVisible = ref(false)
const menuVisible = ref(false)

onMounted(async () => {
  try {
    const res = await fetch('https://detallspatch.onrender.com/tienda')
    if (!res.ok) throw new Error('Error al cargar productos')
    const productos = await res.json()
    producto.value = productos.find(p => p.id == route.params.id)
  } catch (err) {
    console.error('Error al cargar el producto:', err)
  }
})

function añadirAlCarrito() {
  const item = {
    id: producto.value.id,
    nombre: producto.value.nombre,
    imagen: producto.value.imagen,
    precio: producto.value.precio,
    cantidad: cantidad.value
  }

  let carrito = JSON.parse(localStorage.getItem('carrito')) || []
  const index = carrito.findIndex(p => p.id === item.id)

  if (index !== -1) {
    carrito[index].cantidad += item.cantidad
  } else {
    carrito.push(item)
  }

  localStorage.setItem('carrito', JSON.stringify(carrito))

  mensajeVisible.value = true
  setTimeout(() => {
    mensajeVisible.value = false
  }, 3000)
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
    .producto-main {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  .galeria {
    width: 180px;
  }

  .info {
    text-align: center;
  }

  .imagen-principal {
    max-height: 200px;
  }
}

.detalle-producto {
  max-width: 900px;
  margin: 4rem auto;
  padding: 2rem;
  border-radius: 16px;
  display: flex;
  justify-content: center;
}

.producto-main {
  display: flex;
  gap: 2rem;
  align-items: center;
  flex-wrap: wrap;
}

.galeria {
  flex-shrink: 0;
  width: 220px;
}

.imagen-principal {
  width: 100%;
  border-radius: 12px;
  object-fit: cover;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.info {
  text-align: left;
  max-width: 500px;
}

.info h1 {
  font-size: 2rem;
  margin-bottom: 1rem;
  color: #222;
}

.descripcion {
  font-size: 1rem;
  color: #444;
  margin-bottom: 1rem;
}

.precio {
  font-size: 1rem;
  margin-bottom: 1rem;
  font-weight: bold;
  color: #000;
}

.acciones {
  display: flex;
  gap: 1rem;
  align-items: center;
  margin-top: 1rem;
}

.acciones input {
  width: 60px;
  padding: 0.5rem;
  font-size: 1rem;
  border-radius: 6px;
  border: 1px solid #ccc;
}

.acciones button {
  background-color: #eac6c6;
  border: none;
  padding: 0.6rem 1.2rem;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.2s;
}

.acciones button:hover {
  background-color: #d5a8a8;
}

.mensaje-carrito {
  margin-top: 1rem;
  color: green;
  font-weight: bold;
  font-size: 0.95rem;
}
</style>

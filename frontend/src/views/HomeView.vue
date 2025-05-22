<template>
  <div class="home-container">
    <header class="header">
      <RouterLink to="/">
        <img src="/logo.png" alt="Logo" class="logo" />
      </RouterLink>
      <nav class="nav">
        <RouterLink to="/">Inicio</RouterLink>
        <RouterLink to="/noticias">Noticias</RouterLink>
        <RouterLink to="/tienda">Tienda</RouterLink>
        <RouterLink to="/carrito">Carrito</RouterLink>
        <RouterLink to="/login">Inicio Sesión</RouterLink>
      </nav>
    </header>

    <main class="main-content">
      <section class="noticia">
        <h2>{{ noticia }}</h2>
      </section>

      <section class="destacados">
        <h3>Productos Destacados</h3>
        <div class="productos">
          <RouterLink
            v-for="producto in destacados"
            :key="producto.id"
            :to="`/tienda/producto/${producto.id}`"
            class="producto"
            >

            <img
              :src="producto.imagen"
              alt="Imagen del producto"
              class="producto-img"
            />
            <h4>{{ producto.nombre }}</h4>
            <p>Precio: {{ producto.precio }}€</p>
          </RouterLink>
        </div>

        <div class="ver-mas-container">
          <RouterLink to="/tienda" class="ver-mas-btn">Ver más</RouterLink>
        </div>
      </section>
    </main>
  </div>
</template>


<script setup>
import { onMounted, ref } from 'vue'

const noticia = ref('')
const destacados = ref([])

onMounted(async () => {
  try {
    const res = await fetch('http://localhost:5000/')
    const data = await res.json()
    noticia.value = data.noticia
    destacados.value = data.destacados
  } catch (err) {
    console.error('Error al cargar el home:', err)
  }
})
</script>

<style scoped>
html, body {
  height: 100%;
  width: 100%;
  margin: 0;
  padding: 0;
}

.home-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  font-family: 'Arial', sans-serif;
  background-color: #ffffff;
  color: #333;
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

.main-content {
  flex: 1;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  justify-content: flex-start; /* Puedes usar 'center' si quieres centrar todo */
}

.noticia {
  background-color: #fcdada;
  padding: 1rem;
  border-radius: 8px;
  text-align: center;
  font-size: 1.2rem;
  margin-bottom: 2rem;
}

.destacados h3 {
  margin-bottom: 1rem;
}

.productos {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  justify-content: center;
}

.producto {
  width: 200px;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  padding: 1rem;
  background-color: #fff7f7;
  text-align: center;
}

.producto-img {
  width: 100px;
  border-radius: 6px;
}


.ver-mas-container {
  margin-top: 2rem;
  text-align: center;
}

.ver-mas-btn {
  background-color: #eac6c6;
  color: #000;
  padding: 0.7rem 1.5rem;
  border-radius: 8px;
  font-weight: bold;
  text-decoration: none;
  transition: background-color 0.2s;
}

.ver-mas-btn:hover {
  background-color: #d5a8a8;
}

.producto {
  width: 200px;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  padding: 1rem;
  background-color: #fff7f7;
  text-align: center;
  cursor: pointer;
  text-decoration: none;
  color: inherit;
  transition: box-shadow 0.2s;
}

.producto:hover {
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

</style>

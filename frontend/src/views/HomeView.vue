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

    <section class="portada-container">
      <img src="/portada.png" alt="Portada" class="portada-img" />
      <div class="portada-texto">{{ noticia }}</div>
    </section>

    <section class="bienvenida">
      <h2>Bienvenido a Detalls de Patch</h2>
      <p>
        Creamos a mano productos únicos llenos de amor y dedicación. Descubre el detalle perfecto para ti o para regalar a alguien especial.
      </p>
    </section>

    <main class="main-content">
      <section class="destacados">
        <h3>Productos Destacados</h3>
        <div class="productos">
          <RouterLink
            v-for="producto in destacados"
            :key="producto.id"
            :to="`/tienda/producto/${producto.id}`"
            class="producto"
          >
            <div class="producto-img-container">
              <img
                :src="producto.imagen"
                alt="Imagen del producto"
                class="producto-img"
              />
              <span class="precio">{{ producto.precio }} €</span>
            </div>
          </RouterLink>
        </div>

        <div class="ver-mas-container">
          <RouterLink to="/tienda" class="ver-mas-btn">Ver más</RouterLink>
        </div>
      </section>
    </main>

    <footer class="footer">
      <div class="footer-content">
        <p>© 2025 Detalls de Patch. Todos los derechos reservados.</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const noticia = ref('')
const destacados = ref([])
const menuVisible = ref(false)

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

.main-content {
  flex: 1;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
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
  gap: 2rem;
  justify-content: center;
}

.producto {
  width: 200px;
  background-color: #fff7f7;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  padding: 1rem;
  text-align: center;
  cursor: pointer;
  text-decoration: none;
  color: inherit;
  overflow: hidden;
  transition: transform 0.2s ease, box-shadow 0.2s;
}

.producto:hover {
  transform: translateY(-5px);
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.producto-img-container {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
}

.producto-img {
  width: 100%;
  height: 180px;
  object-fit: cover;
  display: block;
  border-radius: 12px;
}

.precio {
  position: absolute;
  bottom: 8px;
  left: 10px;
  background-color: rgba(255, 255, 255, 0.85);
  padding: 0.2rem 0.6rem;
  font-size: 0.85rem;
  border-radius: 999px;
  font-weight: bold;
  color: #444;
  box-shadow: 0 0 4px rgba(0,0,0,0.1);
}

.portada-container {
  position: relative;
  width: 100%;
  max-height: 700px;
  overflow: hidden;
  margin-bottom: 2rem;
}

.portada-img {
  width: 100%;
  height: auto;
  object-fit: cover;
  filter: brightness(0.85);
}

.portada-texto {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: rgba(255, 240, 245, 0.75);
  color: #842c56;
  padding: 1.5rem 2rem;
  border-radius: 12px;
  font-size: 1.6rem;
  font-weight: bold;
  text-align: center;
  font-family: 'Georgia', serif;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s ease, background-color 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;
}

.portada-texto:hover {
  transform: translate(-50%, -50%) scale(1.05) rotate(-1deg);
  background-color: rgba(255, 230, 240, 0.9);
  box-shadow: 0 0 15px rgba(132, 44, 86, 0.4);
}

.bienvenida {
  background-color: #fff3f3;
  padding: 2rem;
  border-radius: 12px;
  text-align: center;
  margin: 2rem auto;
  max-width: 900px;
  box-shadow: 0 0 10px rgba(233, 178, 178, 0.3);
}

.bienvenida h2 {
  font-size: 1.8rem;
  margin-bottom: 0.5rem;
  color: #842c56;
}

.bienvenida p {
  font-size: 1.1rem;
  color: #555;
  font-style: italic;
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

.nombre {
  text-align: center;
  margin-top: 0.5rem;
  font-size: 1rem;
  font-weight: 600;
}
.footer {
  background-color: #eac6c6;
  padding: 1.5rem 2rem;
  text-align: center;
  font-size: 0.9rem;
  color: #333;
  border-top: 1px solid #d8b5b5;
  margin-top: 2rem;
}

.footer-content {
  max-width: 900px;
  margin: 0 auto;
}


</style>

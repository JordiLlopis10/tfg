<template>
  <div class="home-container">
    <header class="header">
      <RouterLink to="/">
        <img src="/logo.png" alt="Logo" class="logo" />
      </RouterLink>

      <button class="hamburger" @click="menuVisible = !menuVisible">☰</button>

      <nav class="nav" :class="{ open: menuVisible }">
        <RouterLink to="/" @click="menuVisible = false">Inicio</RouterLink>
        <RouterLink to="/tienda" @click="menuVisible = false"
          >Tienda</RouterLink
        >
        <RouterLink to="/carrito" @click="menuVisible = false"
          >Carrito</RouterLink
        >
        <RouterLink to="/contacto" @click="menuVisible = false"
          >Contacto</RouterLink
        >
      </nav>
    </header>

    <section class="portada-container">
      <img src="/portada.png" alt="Portada" class="portada-img" />
      <div class="portada-texto">{{ noticia }}</div>
    </section>

    <section class="bienvenida">
      <h2>Bienvenido a Detalls de Patch</h2>
      <p>
        Creamos a mano productos únicos llenos de amor y dedicación. Descubre el
        detalle perfecto para ti o para regalar a alguien especial.
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

    <section class="por-que-detalls">
      <h2>¿Por qué comprar en Detalls de Patch?</h2>
      <div class="beneficios">
        <div class="beneficio">
          <i class="fas fa-shield-alt"></i>
          <h3>100% Pago Seguro</h3>
          <p>Tu seguridad es nuestra prioridad.</p>
        </div>
        <div class="beneficio">
          <i class="fas fa-undo-alt"></i>
          <h3>14 Días de Devolución</h3>
          <p>Si no estás satisfecha, lo solucionamos.</p>
        </div>
        <div class="beneficio">
          <i class="fas fa-headset"></i>
          <h3>Atención Personalizada</h3>
          <p>Estamos siempre disponibles para ti.</p>
        </div>
      </div>
    </section>

    <section class="sobre-nosotros">
      <h2>Nuestra esencia</h2>

      <div class="sobre-grid">
        <p>
          Detalls de Patch nació en un pequeño rincón de casa, rodeado de telas,
          botones y muchas ganas de crear. Creemos que los objetos hechos a mano
          tienen un poder especial: capturan historias, emociones y momentos
          irrepetibles. Cada puntada, cada color y cada elección de material
          reflejan nuestro deseo de compartir calidez y cercanía con quienes
          confían en nosotros.
        </p>

        <p>
          Con el tiempo, nuestro taller creció, pero mantenemos intactos
          nuestros valores: <strong>calidad artesanal</strong>,
          <strong>materiales responsables</strong> y
          <strong>trato humano</strong>. Trabajamos en colecciones limitadas
          para garantizar la exclusividad y minimizar el impacto ambiental, y
          colaboramos con proveedores locales para apoyar la economía de
          proximidad.
        </p>

        <p>
          Ya sea un regalo para alguien especial o un capricho para ti, queremos
          que cada pieza te recuerde que los detalles importan. Gracias por
          formar parte de esta aventura y permitirnos seguir hilando historias
          juntos.
        </p>
      </div>
    </section>

    <footer class="footer">
      <div class="footer-content">
        <p>© 2025 Detalls de Patch. Todos los derechos reservados.</p>
        <div class="redes-sociales">
          <a href="https://www.youtube.com/@detallspatch" target="_blank"
            ><i class="fab fa-youtube"></i
          ></a>
          <a href="https://www.instagram.com/detallspatch" target="_blank"
            ><i class="fab fa-instagram"></i
          ></a>
          <a href="https://www.tiktok.com/@detallspatch" target="_blank"
            ><i class="fab fa-tiktok"></i
          ></a>
          <a href="https://www.facebook.com/detallspatch" target="_blank"
            ><i class="fab fa-facebook-f"></i
          ></a>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

const noticia = ref("");
const destacados = ref([]);
const menuVisible = ref(false);

onMounted(async () => {
  try {
    const res = await fetch("https://detallspatch.onrender.com/");
    const data = await res.json();
    noticia.value = data.noticia;
    destacados.value = data.destacados;
  } catch (err) {
    console.error("Error al cargar el home:", err);
  }
});
</script>

<style scoped>
html,
body {
  height: 100%;
  width: 100%;
  margin: 0;
  padding: 0;
}

.home-container {
  font-family: "Arial", sans-serif;
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
  .beneficios {
    flex-direction: row;
    justify-content: space-around;
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
  box-shadow: 0 0 4px rgba(0, 0, 0, 0.1);
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
  font-family: "Georgia", serif;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s ease, background-color 0.3s ease,
    box-shadow 0.3s ease;
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

.redes-sociales {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 1rem;
}

.redes-sociales a {
  color: #000000;
  font-size: 1.5rem;
  transition: color 0.2s;
}

.redes-sociales a:hover {
  color: #842c56;
}
.por-que-detalls {
  background-color: #fef3f7;
  padding: 3rem 1rem;
  text-align: center;
  border-radius: 16px;
  max-width: 1200px;
  margin: 0 auto;
  box-shadow: 0 0 20px rgba(230, 180, 200, 0.15);
}

.por-que-detalls h2 {
  font-size: 2rem;
  color: #a33666;
  margin-bottom: 2rem;
  font-weight: bold;
}

.beneficios {
  display: flex;
  flex-direction: column;
  gap: 2.5rem;
}

@media (min-width: 768px) {
  .beneficios {
    flex-direction: row;
    justify-content: space-around;
  }
}

.beneficio {
  max-width: 240px;
  margin: 0 auto;
}

.beneficio i {
  font-size: 3rem;
  color: #d84a8c;
  margin-bottom: 1rem;
}

.beneficio h3 {
  color: #842c56;
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
}

.beneficio p {
  color: #444;
  font-size: 0.95rem;
}

.sobre-nosotros {
  background-color: #fff8fa;
  padding: 3rem 1.5rem;
  border-radius: 16px;
  margin: 3rem auto;
  max-width: 1000px;
  box-shadow: 0 0 15px rgba(220, 170, 190, 0.15);
  text-align: center;
}

.sobre-nosotros h2 {
  color: #842c56;
  font-size: 1.9rem;
  margin-bottom: 2rem;
}

.sobre-grid {
  display: grid;
  gap: 1.8rem;
}

.sobre-grid p {
  font-size: 1.05rem;
  line-height: 1.7;
  color: #555;
  text-align: justify;
}

@media (min-width: 900px) {
  .sobre-grid {
    grid-template-columns: 1fr 1fr;
  }

  .sobre-grid p:nth-child(3) {
    grid-column: span 2;
  }
}

</style>

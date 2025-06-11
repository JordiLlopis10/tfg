<template>
  <div class="home-container">
    <header class="header">
      <RouterLink to="/">
        <img src="/logo.png" alt="Logo" class="logo" />
      </RouterLink>

      <button class="hamburger" @click="menuVisible = !menuVisible">☰</button>

      <nav class="nav" :class="{ open: menuVisible }">
        <RouterLink to="/" @click="menuVisible = false">Inicio</RouterLink>
        <RouterLink to="/tienda" @click="menuVisible = false">Tienda</RouterLink>
        <RouterLink to="/carrito" @click="menuVisible = false">Carrito</RouterLink>
        <RouterLink to="/contacto" @click="menuVisible = false">Contacto</RouterLink>
      </nav>
    </header>

    <section class="portada-container">
      <img src="/portada-sobre.png" alt="Sobre Nosotros" class="portada-img" />
      <div class="portada-texto">Conoce nuestra historia y pasión</div>
    </section>

    <section class="bienvenida">
      <h2>Sobre Detalls de Patch</h2>
      <p>
        Nacimos del amor por los detalles y la artesanía. Cada creación es una
        expresión de dedicación, cariño y creatividad.
      </p>
    </section>

    <main class="main-content">
      <section class="texto-nosotros">
        <h3>Nuestra Historia</h3>
        <p>
          Desde nuestros inicios, en un pequeño taller familiar, hemos trabajado con ilusión para ofrecer productos únicos y personalizados. 
          Creemos en el poder de los detalles para transmitir emociones y hacer sentir especial a quien los recibe.
        </p>

        <h3>Nuestros Valores</h3>
        <ul>
          <li>🎨 Creatividad en cada pieza</li>
          <li>💖 Amor por lo artesanal</li>
          <li>🌱 Compromiso con lo sostenible</li>
          <li>🤝 Atención cercana y humana</li>
        </ul>
      </section>
    </main>

    <footer class="footer">
      <div class="footer-content">
        <p>© 2025 Detalls de Patch. Todos los derechos reservados.</p>
        <div class="redes-sociales">
          <a href="https://www.youtube.com/@detallspatch" target="_blank"><i class="fab fa-youtube"></i></a>
          <a href="https://www.instagram.com/detallspatch" target="_blank"><i class="fab fa-instagram"></i></a>
          <a href="https://www.tiktok.com/@detallspatch" target="_blank"><i class="fab fa-tiktok"></i></a>
          <a href="https://www.facebook.com/detallspatch" target="_blank"><i class="fab fa-facebook-f"></i></a>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref } from "vue";

const menuVisible = ref(false);
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
.texto-nosotros {
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem;
  background-color: #fff3f3;
  border-radius: 12px;
  box-shadow: 0 0 10px rgba(233, 178, 178, 0.3);
}

.texto-nosotros h3 {
  color: #842c56;
  margin-bottom: 1rem;
  font-size: 1.5rem;
}

.texto-nosotros p {
  color: #444;
  font-size: 1.1rem;
  line-height: 1.6;
  margin-bottom: 2rem;
}

.texto-nosotros ul {
  list-style: none;
  padding: 0;
}

.texto-nosotros li {
  font-size: 1.1rem;
  margin-bottom: 0.8rem;
  color: #555;
  display: flex;
  align-items: center;
}
</style>

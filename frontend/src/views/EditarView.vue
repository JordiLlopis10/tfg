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
    <div class="editar-panel" v-if="producto">
      <h1>Editar Producto</h1>
      <form @submit.prevent="guardarCambios">
        <label>Nombre</label>
        <input v-model="producto.nombre" required />

        <label>Descripción</label>
        <input v-model="producto.descripcion" required />

        <label>Precio</label>
        <input type="number" v-model.number="producto.precio" required min="0" step="0.01" />

        <label>Stock</label>
        <input type="number" v-model.number="producto.stock" required min="0" />

        <label>Imagen (URL)</label>
        <input v-model="producto.imagen" required />

        <button type="submit">Guardar Cambios</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const id = route.params.id
const producto = ref(null)
const menuVisible = ref(false)

onMounted(async () => {
  try {
    const res = await fetch(`http://localhost:5000/admin/editar/${id}`)
    if (!res.ok) throw new Error('Error al cargar producto')
    producto.value = await res.json()
  } catch (err) {
    alert('Error al cargar producto')
  }
})

async function guardarCambios() {
  try {
    const res = await fetch(`http://localhost:5000/admin/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(producto.value),
    })
    if (!res.ok) throw new Error('Error al actualizar producto')
    alert('Producto actualizado')
    router.push('/admin')
  } catch (err) {
    alert('Error al actualizar producto')
  }
}
onMounted(async () => {
  try {
    const res = await fetch("http://localhost:5000/auth/user", {
      credentials: "include"
    });
    if (!res.ok) throw new Error();
    const user = await res.json();
    if (!["pedritoue2@gmail.com", "llopisgodinojordi@gmai.com"].includes(user.email)) {
      router.push("/login");
      return;
    }
    const productoRes = await fetch(`http://localhost:5000/admin/editar/${id}`);
    if (!productoRes.ok) throw new Error('Error al cargar producto');
    producto.value = await productoRes.json();
  } catch (err) {
    router.push("/login");
  }
});
</script>


<style scoped>
.editar-panel {
  max-width: 400px;
  margin: 2rem auto;
  background: #fff7f7;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 0 8px rgb(0 0 0 / 0.1);
}

h1 {
  margin-bottom: 1.5rem;
  font-weight: bold;
}

label {
  font-weight: bold;
  margin-top: 1rem;
  display: block;
}

input,
button {
  display: block;
  width: 100%;
  margin-bottom: 1rem;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
  box-sizing: border-box;
}

button {
  background-color: #eac6c6;
  border: none;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #d49a9a;
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

}

</style>

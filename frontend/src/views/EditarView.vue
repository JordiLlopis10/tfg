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
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const id = route.params.id
const producto = ref(null)

onMounted(async () => {
  try {
    const res = await axios.get(`http://localhost:5000/admin/editar/${id}`)
    producto.value = res.data
  } catch (err) {
    alert('Error al cargar producto')
  }
})

async function guardarCambios() {
  try {
    await axios.put(`http://localhost:5000/admin/${id}`, producto.value)
    alert('Producto actualizado')
    router.push('/admin')
  } catch (err) {
    alert('Error al actualizar producto')
  }
}
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

</style>

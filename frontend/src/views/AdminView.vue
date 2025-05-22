<template>
  <div>
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

    <div class="admin-container">
      <section class="add-product">
        <h1>Añadir Producto</h1>
        <form @submit.prevent="añadirProducto">
          <label>Nombre</label>
          <input v-model="producto.nombre" type="text" required />

          <label>Descripción</label>
          <input v-model="producto.descripcion" type="text" required />

          <label>Precio</label>
          <input v-model.number="producto.precio" type="number" min="0" step="0.01" required />

          <label>Stock</label>
          <input v-model.number="producto.stock" type="number" min="0" required />

          <label>Imagen (URL)</label>
          <input v-model="producto.imagen" type="text" required />

          <button type="submit">Añadir</button>
        </form>
      </section>

      <section class="product-list">
        <h2>Productos Existentes</h2>
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Nombre</th>
              <th>Descripción</th>
              <th>Precio</th>
              <th>Stock</th>
              <th>Imagen</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="prod in productos" :key="prod.id">
              <td>{{ prod.id }}</td>
              <td>{{ prod.nombre }}</td>
              <td>{{ prod.descripcion }}</td>
              <td>{{ prod.precio }} €</td>
              <td>{{ prod.stock }}</td>
              <td><img :src="prod.imagen" alt="imagen" class="product-img" /></td>
              <td class="acciones-cell">
                <button @click="editarProducto(prod.id)" class="accion-btn">Editar</button>
                <button @click="eliminarProducto(prod.id)" class="accion-btn">Eliminar</button>
              </td>
            </tr>
          </tbody>
        </table>
      </section>
    </div>
  </div>
</template>

<script setup>
// Mantén igual el script, pero elimina la variable isAdmin
import { ref, reactive, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
const router = useRouter()

function editarProducto(id) {
  router.push(`/admin/editar/${id}`)
}

const producto = reactive({
  nombre: '',
  descripcion: '',
  precio: 0,
  stock: 0,
  imagen: ''
})

const productos = ref([])

async function cargarProductos() {
  try {
    const res = await axios.get('http://localhost:5000/productos') 
    productos.value = res.data
  } catch (err) {
    console.error('Error al cargar productos:', err)
  }
}

async function añadirProducto() {
  try {
    const productoEnviar = { ...producto }
    await axios.post('http://localhost:5000/admin', productoEnviar)
    alert('Producto añadido correctamente')
    Object.assign(producto, { nombre: '', descripcion: '', precio: 0, stock: 0, imagen: '' })
    await cargarProductos()
  } catch (err) {
    alert('Error al añadir producto')
  }
}

async function eliminarProducto(id) {
  if (!confirm('¿Estás seguro de eliminar este producto?')) return
  try {
    await axios.delete(`http://localhost:5000/admin/${id}`)
    alert('Producto eliminado')
    await cargarProductos()
  } catch (err) {
    alert('Error al eliminar producto')
  }
}

onMounted(() => {
  cargarProductos()
})
</script>

<style scoped>
/* Header */
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

/* Contenedor admin */
.admin-container {
  display: flex;
  max-width: 1200px;
  margin: 2rem auto;
  gap: 2rem;
  padding: 0 1rem;
}

/* Panel añadir producto */
.add-product {
  flex: 1;
  background: #fff7f7;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 0 8px rgb(0 0 0 / 0.1);
  max-width: 400px;
}

.add-product h1 {
  margin-bottom: 1.5rem;
}

.add-product label {
  font-weight: bold;
  margin-top: 1rem;
  display: block;
}

.add-product input,
.add-product button {
  display: block;
  width: 100%;
  margin-bottom: 1rem;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.add-product button {
  background-color: #eac6c6;
  border: none;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.add-product button:hover {
  background-color: #d49a9a;
}

/* Panel lista productos */
.product-list {
  flex: 2;
  background: #fff7f7;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 0 8px rgb(0 0 0 / 0.1);
  overflow-x: auto;
}

.product-list h2 {
  margin-bottom: 1rem;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  border: 1px solid #ccc;
  padding: 0.5rem;
  text-align: left;
}

th {
  background-color: #f4f4f4;
}

.product-img {
  width: 60px;
  height: auto;
  border-radius: 4px;
}

/* Botones acciones */
.acciones-cell {
  text-align: center;
  white-space: nowrap;
}

.accion-btn {
  background-color: #eac6c6;
  border: none;
  padding: 0.4rem 0.8rem;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.3s ease;
  margin: 0 0.25rem;
  width: 80px;
  display: inline-block;
  text-align: center;
}

.accion-btn:hover {
  background-color: #d49a9a;
}
</style>

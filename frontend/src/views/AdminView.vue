<template>
  <div>
    <header class="header">
  <RouterLink to="/">
    <img src="/logo.png" alt="Logo" class="logo" />
  </RouterLink>
  
  <button class="hamburger" @click="menuAbierto = !menuAbierto">
    ☰
  </button>

  <nav :class="['nav', { open: menuAbierto }]">
    <RouterLink to="/">Inicio</RouterLink>
    <RouterLink to="/tienda">Tienda</RouterLink>
    <RouterLink to="/carrito">Carrito</RouterLink>
    <RouterLink to="/contacto">Contacto</RouterLink>
    <button class="logout-btn" @click="logout">Cerrar sesión</button>
  </nav>
</header>


    <div class="admin-container">
      <div class="admin-top">
        <section class="add-product">
          <h1>Añadir Producto</h1>
          <form @submit.prevent="añadirProducto">
            <label>Nombre</label>
            <input v-model="producto.nombre" type="text" required />

            <label>Descripción</label>
            <input v-model="producto.descripcion" type="text" required />

            <label>Precio</label>
            <input
              v-model.number="producto.precio"
              type="number"
              min="0"
              step="0.01"
              required
            />

            <label>Stock</label>
            <input
              v-model.number="producto.stock"
              type="number"
              min="0"
              required
            />

            <label>Imagen (URL)</label>
            <input v-model="producto.imagen" type="text" required />

            <button type="submit">Añadir</button>
          </form>
        </section>

        <section class="product-list">
            <h2>Productos Existentes</h2>
            <div class="table-wrapper">
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
                <td>
                  <img :src="prod.imagen" alt="imagen" class="product-img" />
                </td>
                <td class="acciones-cell">
                  <button @click="editarProducto(prod.id)" class="accion-btn">
                    Editar
                  </button>
                  <button @click="eliminarProducto(prod.id)" class="accion-btn">
                    Eliminar
                  </button>
                </td>
              </tr>
            </tbody>
            </table>
        </div>
        </section>
      </div>

    <section class="order-list">
    <h2>Pedidos Recientes</h2>
    <div class="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Email</th>
              <th>Productos</th>
              <th>Total</th>
              <th>Dirección</th>
              <th>Ciudad</th>
              <th>CP</th>
              <th>Provincia</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="pedido in pedidos" :key="pedido.id">
              <td>{{ pedido.id }}</td>
              <td>{{ pedido.email }}</td>
              <td><pre>{{ pedido.productos }}</pre></td>
              <td>{{ pedido.total }} €</td>
              <td>{{ pedido.direccion }}</td>
              <td>{{ pedido.ciudad }}</td>
              <td>{{ pedido.cp }}</td>
              <td>{{ pedido.provincia }}</td>
            </tr>
          </tbody>
        </table>
    </div>
    </section>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const menuAbierto = ref(false);

const logout = async () => {
  try {
    await fetch("https://detallspatch.onrender.com/logout", {
      method: "POST",
      credentials: 'include'
    });
    localStorage.removeItem("token");
    localStorage.removeItem("admin-auth");
    router.push("/");
  } catch (err) {
    console.error("Error al cerrar sesión:", err);
  }
};

const producto = reactive({
  nombre: "",
  descripcion: "",
  precio: 0,
  stock: 0,
  imagen: "",
});

const productos = ref([]);

function editarProducto(id) {
  router.push(`/admin/editar/${id}`);
}

async function cargarProductos() {
  try {
    const res = await fetch("https://detallspatch.onrender.com/productos", {
      credentials: 'include'
    });
    if (!res.ok) throw new Error("Error al cargar productos");
    productos.value = await res.json();
  } catch (err) {
    console.error("Error al cargar productos:", err);
  }
}
async function añadirProducto() {
  try {
    const productoEnviar = { ...producto };
    const res = await fetch("https://detallspatch.onrender.com/admin", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: 'include',
      body: JSON.stringify(productoEnviar),
    });
    if (!res.ok) throw new Error("Error al añadir producto");
    alert("Producto añadido correctamente");
    Object.assign(producto, {
      nombre: "",
      descripcion: "",
      precio: 0,
      stock: 0,
      imagen: "",
    });
    await cargarProductos();
  } catch (err) {
    alert("Error al añadir producto. Intenta de nuevo.");
  }
}

async function eliminarProducto(id) {
  if (!confirm("¿Estás seguro de eliminar este producto?")) return;
  try {
    const res = await fetch(`https://detallspatch.onrender.com/admin/${id}`, {
      method: "DELETE",
      credentials: 'include'
    });
    
    if (res.status === 401) {
      alert("Debes iniciar sesión como administrador");
      router.push("/login");
      return;
    }
    
    if (res.status === 403) {
      alert("No tienes permisos de administrador");
      return;
    }
    
    if (!res.ok) throw new Error("Error al eliminar producto");
    
    alert("Producto eliminado");
    await cargarProductos();
  } catch (err) {
    alert("Error al eliminar producto. Intenta de nuevo.");
    console.error(err);
  }
}

const pedidos = ref([]);

async function cargarPedidos() {
  try {
    const res = await fetch("https://detallspatch.onrender.com/pedidos");
    if (!res.ok) throw new Error("Error al cargar pedidos");
    pedidos.value = await res.json();
  } catch (err) {
    console.error("Error al cargar pedidos:", err);
  }
}

onMounted(async () => {
  try {
    const authCheck = await fetch("https://detallspatch.onrender.com/auth/user", {
      credentials: 'include'
    });
    
    if (!authCheck.ok) {
      router.push("/login");
      return;
    }
    
    const userData = await authCheck.json();
    
    if (userData.email !== "pedritoue2@gmail.com") {
      router.push("/");
      return;
    }
    
    cargarProductos();
    cargarPedidos();
    
  } catch (err) {
    console.error("Error de autenticación:", err);
    router.push("/login");
  }
});
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

.hamburger {
  display: none;
  background: none;
  font-size: 2rem;
  border: none;
  cursor: pointer;
  color: #000;
}

.admin-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  max-width: 1200px;
  margin: 1rem auto 2rem;
  padding: 0 1rem;
  gap: 2rem;
}

.admin-top {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  gap: 2rem;
}

.add-product {
  width: 100%;
  max-width: 500px;
  background: #fff7f7;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 0 8px rgb(0 0 0 / 0.1);
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

.product-list,
.order-list {
  width: 100%;
  background: #fff7f7;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 0 8px rgb(0 0 0 / 0.1);
  overflow-x: auto;
}

.product-list h2,
.order-list h2 {
  margin-bottom: 1rem;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
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

.logout-btn {
  background-color: #d49a9a;
  border: none;
  padding: 0.4rem 0.8rem;
  border-radius: 4px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.logout-btn:hover {
  background-color: #eac6c6;
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
    z-index: 10;
    text-align: center;
  }

  .nav.open {
    display: flex;
  }

  .nav a,
  .logout-btn {
    font-size: 1.1rem;
    padding: 0.5rem 0;
  }

  .logout-btn {
    width: 100%;
    text-align: center;
  }
  .table-wrapper {
  overflow-x: auto;
  width: 100%;
}

.table-wrapper table {
  min-width: 800px;
  white-space: nowrap;
}

}
</style>


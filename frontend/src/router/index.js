import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'
import PerfilView from '@/views/PerfilView.vue'
import HomeView from '@/views/HomeView.vue'
import AdminView from '@/views/AdminView.vue'
import EditarView from '@/views/EditarView.vue'
import TiendaView from '@/views/TiendaView.vue'
import ProductoView from '@/views/ProductoView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView,
    },
    {
      path: '/perfil',
      name: 'perfil',
      component: PerfilView,
    },
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/admin',
      name: 'admin',
      component: AdminView,
    },
    {
      path: '/admin/editar/:id',
      name: 'editar',
      component: EditarView,
    },
    {
      path: '/tienda',
      name: 'tienda',
      component: TiendaView,
    },
    {
      path: '/tienda/producto/:id',
      name: 'Producto',
      component: ProductoView,
    },
  ],
})

export default router

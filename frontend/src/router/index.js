import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'
import HomeView from '@/views/HomeView.vue'
import AdminView from '@/views/AdminView.vue'
import EditarView from '@/views/EditarView.vue'
import TiendaView from '@/views/TiendaView.vue'
import ProductoView from '@/views/ProductoView.vue'
import CarritoView from '@/views/CarritoView.vue'
import PasarelaView from '@/views/PasarelaView.vue'
import ContactoView from '@/views/ContactoView.vue'
import RecuperarView from '@/views/RecuperarView.vue'
import ResetearView from '@/views/ResetearView.vue'
import NoEncontradaView from '@/views/NoEncontradaView.vue'

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
    {
      path: '/carrito',
      name: 'carrito',
      component: CarritoView,
    },
    {
      path: '/pago',
      name: 'pago',
      component: PasarelaView,
    },
    {
      path: '/contacto',
      name: 'contacto',
      component: ContactoView,
    },
    {
      path: '/recuperar',
      name: 'recuperar',
      component: RecuperarView,
    },
    {
      path: '/resetear/:token',
      name: 'resetear',
      component: ResetearView,
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'error',
      component: NoEncontradaView,
    },
  ],
})

export default router

// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '@/store/auth';
import Login from '@/views/Login.vue';
import RegisterCustomer from '../views/RegisterCustomer.vue';
import RegisterProfessional from '../views/RegisterProfessional.vue';

// Admin Views
import AdminLayout from '@/views/admin/Layout.vue';
import AdminDashboard from '@/views/admin/Dashboard.vue';
import AdminSearch from '@/views/admin/Search.vue';
import Service from '@/views/admin/Service.vue';

// Professional Views
import ProfessionalLayout from '@/views/professional/Layout.vue';
import ProfessionalDashboard from '@/views/professional/Dashboard.vue';

// Customer Views
import CustomerLayout from '@/views/customer/Layout.vue';
import CustomerDashboard from '@/views/customer/Dashboard.vue';
import CustomerSearch from '@/views/customer/Search.vue';


const routes = [
  { path: '/', component: Login },

  { path: '/register/customer', component: RegisterCustomer },
  { path: '/register/service-professional', component: RegisterProfessional },

  {
    path: '/admin/:id',
    component: AdminLayout,
    meta: { requiresRole: 'admin' },
    children: [
      { path: 'dashboard', component: AdminDashboard },
      { path: 'service/:id', name: 'Service', component: Service },
      { path: 'search', component: AdminSearch },
    ],
  },
  {
    path: '/professional/:id',
    component: ProfessionalLayout,
    meta: { requiresRole: 'professional' },
    children: [
      { path: 'dashboard', component: ProfessionalDashboard },
    ],
  },
  {
    path: '/customer/:id',
    component: CustomerLayout,
    meta: { requiresRole: 'customer' },
    children: [
      { path: 'dashboard', component: CustomerDashboard },
      { path: 'search', component: CustomerSearch },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  const userRole = authStore.userRole;
  if (to.meta.requiresRole && userRole !== to.meta.requiresRole) {
    next('/');
  } else {
    next();
  }
});

export default router;

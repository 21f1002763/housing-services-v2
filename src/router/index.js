// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '@/store/auth';
import Login from '@/views/Login.vue';

// Admin Views
import AdminLayout from '@/views/admin/Layout.vue';
import AdminDashboard from '@/views/admin/Dashboard.vue';
import AdminSearch from '@/views/admin/Search.vue';
import AdminSummary from '@/views/admin/Summary.vue';
import AdminProfile from '@/views/admin/Profile.vue';
import Service from '@/views/admin/Service.vue';

// Professional Views
import ProfessionalLayout from '@/views/professional/Layout.vue';
import ProfessionalDashboard from '@/views/professional/Dashboard.vue';
import ProfessionalSearch from '@/views/professional/Search.vue';
import ProfessionalSummary from '@/views/professional/Summary.vue';
import ProfessionalProfile from '@/views/professional/Profile.vue';

// Customer Views
import CustomerLayout from '@/views/customer/Layout.vue';
import CustomerDashboard from '@/views/customer/Dashboard.vue';
import CustomerSearch from '@/views/customer/Search.vue';
import CustomerSummary from '@/views/customer/Summary.vue';
import CustomerProfile from '@/views/customer/Profile.vue';

const routes = [
  { path: '/', component: Login },

  {
    path: '/admin',
    component: AdminLayout,
    meta: { requiresRole: 'admin' },
    children: [
      { path: 'dashboard', component: AdminDashboard },
      { path: 'service/:id', name: 'Service', component: Service },
      { path: 'search', component: AdminSearch },
      { path: 'summary', component: AdminSummary },
      { path: 'profile', component: AdminProfile },
    ],
  },
  {
    path: '/professional',
    component: ProfessionalLayout,
    meta: { requiresRole: 'professional' },
    children: [
      { path: 'dashboard', component: ProfessionalDashboard },
      { path: 'search', component: ProfessionalSearch },
      { path: 'summary', component: ProfessionalSummary },
      { path: 'profile', component: ProfessionalProfile },
    ],
  },
  {
    path: '/customer',
    component: CustomerLayout,
    meta: { requiresRole: 'customer' },
    children: [
      { path: 'dashboard', component: CustomerDashboard },
      { path: 'search', component: CustomerSearch },
      { path: 'summary', component: CustomerSummary },
      { path: 'profile', component: CustomerProfile },
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

import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    userRole: localStorage.getItem('role') || null,
    token: localStorage.getItem('token') || null,
  }),
  actions: {
    login(userData) {
      this.token = userData.token;
      this.role = userData.role;
      localStorage.setItem('token', userData.token);
      localStorage.setItem('role', userData.role);
    },
    logout() {
      this.token = null;
      this.role = null;
      localStorage.removeItem('token');
      localStorage.removeItem('role');
    }
  }
});

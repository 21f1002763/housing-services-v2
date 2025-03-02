import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    userRole: localStorage.getItem('role') || null,
    token: localStorage.getItem('token') || null,
    userId: localStorage.getItem('userId') || null,
  }),
  actions: {
    login(userData) {
      this.token = userData.token;
      this.role = userData.role;
      this.userId = userData.userId;

      localStorage.setItem('token', userData.token);
      localStorage.setItem('role', userData.role);
      localStorage.setItem('userId', userData.userId);
    },
    logout() {
      this.token = null;
      this.role = null;
      this.userId = null;

      localStorage.removeItem('token');
      localStorage.removeItem('role');
      localStorage.removeItem('userId');
    }
  }
});

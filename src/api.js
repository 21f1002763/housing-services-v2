import axios from 'axios';
import { useAuthStore } from '@/store/auth';

const api = axios.create({
  baseURL: "http://127.0.0.1:5000",
});


api.interceptors.request.use((config) => {
  const authStore = useAuthStore();  // Initialize Pinia store
  const token = authStore.token;  // Get token from Pinia store
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;



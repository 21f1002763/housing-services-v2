import axios from "axios";
import { useAuthStore } from "@/store/auth";
import router from "@/router";

const api = axios.create({
  baseURL: "http://127.0.0.1:5000/api",
});

api.interceptors.request.use((config) => {
  const authStore = useAuthStore();  
  const token = authStore.token;  
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Add response interceptor
api.interceptors.response.use(
  response => response, 
  error => {
    if (error.response?.status === 401) {
      const authStore = useAuthStore();
      alert("Session expired. Redirecting to home.");
      authStore.logout();  // Clear token from Pinia store
      router.push("/"); // Redirect to Vue home page
    }
    return Promise.reject(error);
  }
);

export default api;

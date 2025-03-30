<template>
  <div class="d-flex align-items-center justify-content-center min-vh-100 bg-light">
    <div class="card login-card shadow-lg p-4">
      <h3 class="text-center text-dark mb-3"
        style="font-family:'Lato', Arial, sans-serif; font-weight: 300; font-size: 1.75rem;">Sign In</h3>
      <form @submit.prevent="login">
        <div class="form-group">
          <div class="icon d-flex align-items-center justify-content-center">
            <span class="fa fa-user"></span>
          </div>
          <input v-model="username" type="text" class="form-control" placeholder="Username" style="padding-left: 60px;" required />
        </div>
        <div class="form-group">
          <div class="icon d-flex align-items-center justify-content-center">
            <span class="fa fa-lock"></span>
          </div>
          <input id="passwordInput" v-model="password" :type="showPassword ? 'text' : 'password'" style="padding-left: 60px;" class="form-control"
            placeholder="Password" required />
          <span class="input-group-text password-toggle" @click="togglePasswordVisibility">
            <i :class="showPassword ? 'fa fa-eye' : 'fa fa-eye-slash'"></i>
          </span>
        </div>
        <button type="submit" class="btn btn-success w-100 py-2">Login</button>
      </form>
      <div class="form-group mt-4">
        <div class="w-100 text-center">
          <p class="mb-1">Don't have an account?</p>
          <div class="register-links">
            <a><router-link to="/register/customer">Customer Register</router-link></a>
            <a><router-link to="/register/service-professional">Service Professional Register</router-link></a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '@/store/auth';
import { useRouter } from 'vue-router';
import { ref, onMounted } from 'vue';
import api from '@/api';

export default {
  setup() {
    const store = useAuthStore();
    const router = useRouter();
    const username = ref('');
    const password = ref('');

    const showPassword = ref(false);
    const passwordInput = ref(null);

    onMounted(() => {
      passwordInput.value = document.querySelector('#passwordInput');
    });

    const togglePasswordVisibility = () => {
      showPassword.value = !showPassword.value;
      // Small delay to avoid reactivity issues
      if (passwordInput.value) {
        passwordInput.value.focus(); // Ensure focus remains on input
      }
    };

    const login = async () => {
      try {
        const response = await api.post('/login', { username: username.value, password: password.value });

        // Store the token
        const token = response.data.access_token;

        // Set token in headers for future requests
        api.defaults.headers.common['Authorization'] = `Bearer ${token}`;

        store.login({ role: response.data.role, token: token, userId: response.data.user_id });
        router.push(`/${response.data.role}/${store.userId}/dashboard`);
      } catch (error) {
        if (error.response) {
          alert(error.response.data.message || "Failed to login.");
        } else if (error.request) {
          alert("No response from server. Please check your network.");
        } else {
          alert("Invalid credentials");
        }
      }
    };

    return { username, password, login, showPassword, togglePasswordVisibility };
  }
};
</script>

<style>
* {
  font-family: "Lato", Arial, sans-serif;
  font-size: 16px;
  line-height: 1.8;
  font-weight: normal;
  color: gray;
}

.bg-light {
  background-color: #f8f9fa;
}

.login-card {
  width: 35rem !important;
  border-radius: 10px;
  background: #fff;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  padding: 2rem;
  text-align: center;
}

.form-control {
  border-left: none;
  height: 48px;
}

.btn-success {
  background-color: #483434;
  border: none;
  font-weight: bold;
}

.btn-success:hover {
  background-color: #6B4F4F;
}

.form-group {
  position: relative;
  margin-bottom: 1rem;
}

.form-group .icon {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  width: 48px;
  height: 48px;
  background: #483434;
  font-size: 20px;
  border-radius: 5px 0 0 5px;
}

.form-group .icon span {
  color: #fff;
}

.form-control {
  height: 48px;
  background: #fff;
  color: #000;
  font-size: 16px;
  border-radius: 5px;
  -webkit-box-shadow: none;
  box-shadow: none;
  border: 1px solid rgba(0, 0, 0, 0.1);
  padding-left: 60px;
}

.form-control:focus,
.form-control:active {
  outline: none !important;
  -webkit-box-shadow: none;
  box-shadow: none;
  border: 1px solid #483434;
}

a {
  transition: .3s all ease;
  color: #483434;
  text-decoration: none;
}

a:hover,
a:focus {
  color: #007bff;
}

.password-toggle {
  cursor: pointer;
  background: white;
  border: none;
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  padding: 5px;
  font-size: 1.3rem;
}

.register-links {
  display: flex;
  justify-content: center;
  gap: 20px; /* Space between links */
}

.register-links a {
  flex: 1; /* Equal width */
  text-align: center;
  padding: 10px;
}
</style>

<template>
  <div class="d-flex align-items-center justify-content-center min-vh-100 bg-light">
      <div class="card login-card shadow-lg p-4">
          <h3 class="text-center text-dark mb-3"
              style="font-family:'Lato', Arial, sans-serif; font-weight: 300; font-size: 1.75rem;">Customer Register
          </h3>
          <form @submit.prevent="registerCustomer">
              <div class="form-group">
                  <label class="input-label" for="usernameInput">Username</label>
                  <input v-model="username" type="text" class="form-control" required />
              </div>
              <div class="form-group">
                  <label class="input-label" for="passwordInput">Password</label>
                  <input id="passwordInput" v-model="password" :type="showPassword ? 'text' : 'password'"
                      class="form-control" required />
                  <span class="input-group-text password-toggle" style="margin-top: 13px;"
                      @click="togglePasswordVisibility">
                      <i :class="showPassword ? 'fa fa-eye' : 'fa fa-eye-slash'"></i>
                  </span>
              </div>
              <div class="form-group">
                  <label class="input-label" for="emailInput">Email</label>
                  <input v-model="email" type="text" class="form-control" required />
              </div>
              <div class="form-group">
                  <label class="input-label" for="nameInput">Name</label>
                  <input v-model="name" type="text" class="form-control" required />
              </div>
              <div class="form-group">
                  <label class="input-label" for="serviceInput">Service</label>
                  <div class="custom-dropdown">
                      <select v-model="selectedService" class="form-control" id="service">
                          <option value="" disabled>Select a service</option>
                          <option v-for="service in services" :key="service.service_id" :value="service.service_id">
                              {{ service.service_name }}
                          </option>
                      </select>
                  </div>
              </div>
              <div class="form-group">
                  <label class="input-label" for="expInput">Experience</label>
                  <input v-model="experience" type="number" min=0 max=100 class="form-control" required />
              </div>
              <div class="form-group">
                  <label class="input-label" for="mobNoInput">Mobile Number</label>
                  <input v-model="mob_no" type="text" class="form-control" required />
              </div>
              <div class="form-group">
                  <label class="input-label" for="addressInput">Address</label>
                  <input v-model="address" type="text" class="form-control" required />
              </div>
              <div class="form-group">
                  <label class="input-label" for="cityInput">City</label>
                  <div class="custom-dropdown">
                      <select v-model="selectedCity" class="form-control" id="city">
                          <option value="" disabled>Select a city</option>
                          <option v-for="city in cities" :key="city.city_id" :value="city.city_id">
                              {{ city.city_name }}
                          </option>
                      </select>
                  </div>
              </div>
              <div class="form-group">
                  <label class="input-label" for="pincodeInput">Pincode</label>
                  <input v-model="pincode" type="text" class="form-control" required />
              </div>
              <button type="submit" class="btn btn-success w-100 py-2 mt-2">Register</button>
          </form>
          <div class="form-group mt-4">
              <div class="w-100 text-center">
                <p class="mb-1"><router-link to="/">Go to Login...</router-link></p>
              </div>
          </div>
      </div>
  </div>
</template>

<script>
import { useRouter } from 'vue-router';
import { ref, onMounted } from 'vue';
import api from '@/api';

export default {
  setup() {
      const router = useRouter();
      const username = ref('');
      const password = ref('');
      const email = ref('');
      const name = ref('');
      const mob_no = ref('');
      const address = ref('');
      const pincode = ref('');
      const experience = ref('');


      const showPassword = ref(false);
      const passwordInput = ref(null);

      const cities = ref([]); // Store fetched cities
      const selectedCity = ref(''); // Store selected city
      const services = ref([]); // Store fetched cities
      const selectedService = ref(''); // Store selected city

      onMounted(() => {
          passwordInput.value = document.querySelector('#passwordInput');
          fetchCities();
          fetchServices();
      });

      const togglePasswordVisibility = () => {
          showPassword.value = !showPassword.value;
          // Small delay to avoid reactivity issues
          if (passwordInput.value) {
              passwordInput.value.focus(); // Ensure focus remains on input
          }
      };

      const registerCustomer = async () => {
          try {
              const response = await api.post('/user', { username: username.value, password: password.value, role_name: 'professional' });

              const user_id = response.data.user_id;

              const registerProf = await api.post(`/professional`, {
                  user_id: user_id,
                  email: email.value,
                  name: name.value,
                  mobile_no: mob_no.value,
                  address: address.value,
                  pincode: pincode.value,
                  city_id: selectedCity.value,
                  experience: experience.value,
                  service_id: selectedService.value
              });

              if (registerProf.status === 201) {
                  console.log("Service Professional created successfully:", response.data);
                  alert("Service Professional created successfully!");
                  router.push(`/`);
              }
          } catch (error) {
              console.error("Update failed:", error);
              // Handle server response errors
              if (error.response) {
                  alert(error.response.data.message || "Failed to add user.");
              } else if (error.request) {
                  alert("No response from server. Please check your network.");
              } else {
                  alert("An unexpected error occurred.");
              }
          }
      };

      const fetchCities = async () => {
          try {
              const response = await api.get('/cities'); // API endpoint to fetch cities
              cities.value = response.data; // Assign cities to reactive variable
          } catch (error) {
              console.error('Failed to fetch cities', error);
          }
      };

      const fetchServices = async () => {
          try {
              const response = await api.get('/service'); // API endpoint to fetch cities
              services.value = response.data; // Assign cities to reactive variable
          } catch (error) {
              console.error('Failed to fetch services', error);
          }
      };

      return {
          username, 
          password, 
          registerCustomer, 
          showPassword, 
          togglePasswordVisibility, 
          cities, 
          selectedCity,
          services,
          selectedService,
          email,
          name,
          mob_no,
          address,
          pincode,
          experience
      };
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
  width: 25rem;
  border-radius: 10px;
  background: #fff;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  padding: 2rem;
  text-align: center;
}

.form-control {
  height: 48px;
  padding: 20px;
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
  margin-bottom: 0.53rem;
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

.input-label {
  display: block;
  text-align: left;
}

/* Ensure dropdown arrow is visible */
.custom-dropdown {
  position: relative;
  width: 100%;
}

.custom-dropdown select {
  appearance: none;
  /* Hide default arrow */
  -webkit-appearance: none;
  -moz-appearance: none;
  width: 100%;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #ccc;
  background-color: white;
  cursor: pointer;
  font-size: 16px;
  color: #333;
}

/* Add custom arrow */
.custom-dropdown::after {
  content: "▼";
  font-size: 14px;
  color: #333;
  position: absolute;
  right: 15px;
  top: 50%;
  transform: translateY(-50%);
  pointer-events: none;
}

.custom-dropdown select:focus {
  border-color: #483434;
  outline: none;
}
</style>
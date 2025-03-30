<template>
  <div class="container">
    <h3 class="mt-3">Services</h3>

    <!-- Search Bar -->
    <div class="search-container">
      <input 
        v-model="searchQuery" 
        type="text" 
        class="form-control" 
        placeholder="Search services..." 
      />
      <span class="search-icon">
        <i class="fa fa-search"></i>
      </span>
    </div>
    
    <!-- Services Grid -->
    <div v-if="filteredServices.length > 0" class="services-grid">
      <ServiceCard v-for="service in filteredServices" 
          :key="service.service_id" 
          :id="service.service_id" 
          :hideDelete="true"
          :title="service.service_name" 
          :description="service.description" 
          :time_required="service.time_required"
          @click-card="openBookServiceModal"/>
    </div>
    <BookServiceModal v-if="showBookServiceModal" :serviceId="selectedServiceId" @close="showBookServiceModal = false" />
  </div>
</template>

<script>
import { useAuthStore } from '@/store/auth';
import Table from "@/components/Table.vue";
import ServiceCard from '@/components/ServiceCard.vue';
import BookServiceModal from '../../components/BookServiceModal.vue';
import api from "@/api";

export default {
  components: { ServiceCard, BookServiceModal },
  data() {
    return {
      services: [],
      searchQuery: "",
      showBookServiceModal: false,
      selectedServiceId: null,
      loading: false,
      error: null,
      authStore: useAuthStore(),
    };
  },
  computed: {
    filteredServices() {
      return this.services.filter(service =>
        service.service_name.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    }
  },
  methods: {
    async fetchServices() {
      this.loading = true;
      this.error = null;
      try {
        const response = await api.get(`customer/${this.authStore.userId}/services`);
        console.log("Fetched Service Data:", response.data); // Debugging step
        this.services = response.data;
      } catch (err) {
        this.error = "Failed to load professionals";
        console.error(err);
      } finally {
        this.loading = false;
      }
    },
    openBookServiceModal(serviceId) {
      this.selectedServiceId = serviceId;
      this.showBookServiceModal = true;
    },
  },
  mounted() {
    this.fetchServices();
  }
};
</script>

<style scoped>
/* Grid Layout */
.services-grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 20px;
  max-width: 100%;
  margin: 0 auto;
}

/* Center search bar */
.search-container {
  display: flex;
  align-items: center;
  width: 100%;
  max-width: 400px;
  margin: 20px auto; /* Center horizontally */
  position: relative;
}

/* Search input field */
.form-control {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 1rem;
}

/* Search icon */
.search-icon {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 1.3rem;
  color: #6c757d;
  cursor: pointer;
}
</style>

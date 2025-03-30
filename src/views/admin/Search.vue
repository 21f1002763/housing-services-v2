<template>
  <div>
    <h3 class="mt-3">Service Professionals</h3>

    <!-- Search Bar -->
    <div class="search-container">
      <input 
        v-model="searchQuery" 
        type="text" 
        class="form-control" 
        placeholder="Search professionals..." 
      />
      <span class="search-icon">
        <i class="fa fa-search"></i>
      </span>
    </div>

    <!-- Professionals Table -->
    <Table :columns="professionalColumns" :data="filteredProfessionals">
      <template v-slot:actions="{ row }">
        <!-- If status is "requested", show Accept and Reject buttons -->
        <template v-if="row.status === 'requested'">
          <button class="btn btn-success btn-sm" @click="acceptProfessional(row)">Accept</button>
          <button class="btn btn-danger btn-sm" @click="rejectProfessional(row)">Reject</button>
        </template>

        <!-- If status is "accepted", show Block button -->
        <template v-else-if="row.status === 'accepted'">
          <button class="btn btn-warning btn-sm" @click="blockProfessional(row)">Block</button>
        </template>

        <!-- If status is "blocked", show Unblock button -->
        <template v-else-if="row.status === 'blocked'">
          <button class="btn btn-secondary btn-sm" @click="unblockProfessional(row)">Unblock</button>
        </template>
      </template>
    </Table>
  </div>
</template>

<script>
import Table from "@/components/Table.vue";
import api from "@/api";

export default {
  components: { Table },
  data() {
    return {
      professionals: [],
      searchQuery: "", // Search query state
      professionalColumns: [
        { key: "professional_id", label: "ID" },
        { key: "name", label: "Name" },
        { key: "email", label: "Email" },
        { key: "city", label: "City" },
        { key: "service", label: "Service" },
        { key: "experience", label: "Experience (Years)" },
        { key: "status", label: "Status" },
        { key: "actions", label: "Actions" }
      ]
    };
  },
  computed: {
    filteredProfessionals() {
      if (!this.searchQuery) return this.professionals;
      return this.professionals.filter(professional =>
        professional.name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
        professional.email.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
        professional.city.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
        professional.service.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    }
  },
  methods: {
    async fetchProfessionals() {
      try {
        const response = await api.get("/professional");
        this.professionals = response.data.map(professional => ({
          professional_id: professional.professional_id,
          name: professional.name || "N/A",
          email: professional.email || "N/A",
          city: professional.city.city_name || "N/A",
          service: professional.service.service_name || "N/A",
          experience: professional.experience,
          status: professional.status
        }));
      } catch (err) {
        console.error("Failed to load professionals:", err);
      }
    }
  },
  mounted() {
    this.fetchProfessionals();
  }
};
</script>

<style scoped>
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

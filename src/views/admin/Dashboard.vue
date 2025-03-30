<template>
  <div>
    <h1 style="color: black;">Admin Dashboard</h1>
    <h3 class="mt-3">Service Professionals</h3>
    <Table :columns="professionalColumns" :data="professionals">
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

  <div>
    <h3 class="mt-3">Customers</h3>
    <Table :columns="customerColumns" :data="customers">
      <template v-slot:actions="{ row }">

        <!-- If status is "accepted", show Block button -->
        <template v-if="row.status === 'active'">
          <button class="btn btn-warning btn-sm" @click="blockCustomer(row)">Block</button>
        </template>

        <!-- If status is "blocked", show Unblock button -->
        <template v-else-if="row.status === 'blocked'">
          <button class="btn btn-secondary btn-sm" @click="unblockCustomer(row)">Unblock</button>
        </template>
      </template>
    </Table>
  </div>

  <div>
    <h3 class="mt-3">Service Requests</h3>
    <Table :columns="serviceRequestColumns" :data="serviceRequests" />
  </div>

  <div class="container">
    <h3 class="mt-3">Our Services</h3>
    <!-- Add Service Button -->
    <button class="add-service-btn" @click="showModal = true">
      + Add Service
    </button>
    <!-- Services Grid -->
    <div v-if="services.length > 0" class="services-grid">
      <ServiceCard v-for="service in services" :key="service.service_id" :id="service.service_id"
        :title="service.service_name" :description="service.description" :time_required="service.time_required"
        :hideDelete="false" @click-card="goToService" @delete-service="deleteService" />
    </div>

    <!-- Add Service Modal -->
    <AddServiceModal v-if="showModal" @close="showModal = false" @service-added="fetchServices" />
  </div>

  <button class="add-service-btn" @click="exportCsv()">
    Export Data
  </button>
</template>

<script>
import Table from "@/components/Table.vue";
import api from "@/api";
import ServiceCard from '@/components/ServiceCard.vue';
import AddServiceModal from "@/components/AddServiceModal.vue";

export default {
  components: { Table, ServiceCard, AddServiceModal },
  data() {
    return {
      showModal: false,
      professionals: [],
      customers: [],
      serviceRequests: [],
      services: [],
      loading: false,
      error: null,
      professionalColumns: [
        { key: "professional_id", label: "ID" },
        { key: "name", label: "Name" },
        { key: "email", label: "Email" },
        { key: "city", label: "City" },
        { key: "service", label: "Service" },
        { key: "experience", label: "Experience (Years)" },
        { key: "status", label: "Status" },
        { key: "actions", label: "Actions" }
      ],
      customerColumns: [
        { key: "customer_id", label: "ID" },
        { key: "name", label: "Name" },
        { key: "email", label: "Email" },
        { key: "city", label: "City" },
        { key: "status", label: "Status" },
        { key: "actions", label: "Actions" }
      ],
      serviceRequestColumns: [
        { key: "request_id", label: "Request ID" },
        { key: "package_name", label: "Package Name" },
        { key: "customer_name", label: "Customer Name" },
        { key: "professional_name", label: "Professional Name" },
        { key: "request_date", label: "Request Date" },
        { key: "complete_date", label: "Complete Date" },
        { key: "service_status", label: "Service Status" },
        { key: "service_rating", label: "Service Rating" }
      ]
    };
  },
  methods: {
    async fetchProfessionals() {
      this.loading = true;
      this.error = null;
      try {
        const response = await api.get("/professional");
        console.log("Fetched Professional Data:", response.data); // Debugging step

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
        this.error = "Failed to load professionals";
        console.error(err);
      } finally {
        this.loading = false;
      }
    },
    async fetchCustomers() {
      this.loading = true;
      this.error = null;
      try {
        const response = await api.get("/customer"); // Debugging step

        this.customers = response.data.map(customer => ({
          customer_id: customer.customer_id,
          name: customer.name || "N/A",
          email: customer.email || "N/A",
          city: customer.city.city_name || "N/A",
          service: customer.service?.service_name || "N/A",
          status: customer.status
        }));
      } catch (err) {
        this.error = "Failed to load professionals";
        console.error(err);
      } finally {
        this.loading = false;
      }
    },
    async fetchServiceRequests() {
      this.loading = true;
      this.error = null;
      try {
        const response = await api.get("/service-request");
        console.log("Fetched Service Request Data:", response.data); // Debugging step

        const usersResponse = await api.get("/user"); // Get response object
        const users = usersResponse.data; // Extract actual user data

        this.serviceRequests = response.data.map(serviceRequest => ({
          request_id: serviceRequest.request_id,
          package_name: serviceRequest.packages.package_name,
          customer_name: serviceRequest.customers.name,
          professional_name: serviceRequest.professionals.name,
          request_date: serviceRequest.request_date,
          complete_date: serviceRequest.complete_date,
          service_status: serviceRequest.service_status,
          service_rating: serviceRequest.service_rating,
        }));
      } catch (err) {
        this.error = "Failed to load service requests";
        console.error(err);
      } finally {
        this.loading = false;
      }
    },
    async acceptProfessional(row) {
      try {
        await api.put(`/professional/${row.professional_id}/accept`);
        row.status = "accepted"; // Update UI
        console.log("Professional accepted successfully");
      } catch (error) {
        console.error("Failed to accept professional", error);
      }
    },
    async rejectProfessional(row) {
      try {
        await api.put(`/professional/${row.professional_id}/reject`);
        row.status = "rejected"; // Update UI
        console.log("Professional rejected successfully");
      } catch (error) {
        console.error("Failed to reject professional", error);
      }
    },
    async blockProfessional(row) {
      try {
        await api.put(`/professional/${row.professional_id}/block`);
        row.status = "blocked"; // Update UI
        console.log("Professional blocked successfully");
      } catch (error) {
        console.error("Failed to block professional", error);
      }
    },
    async unblockProfessional(row) {
      try {
        await api.put(`/professional/${row.professional_id}/unblock`);
        row.status = "accepted"; // Update UI
        console.log("Professional unblocked successfully");
      } catch (error) {
        console.error("Failed to unblock professional", error);
      }
    },
    async blockCustomer(row) {
      try {
        await api.put(`/customer/${row.customer_id}/block`);
        row.status = "blocked"; // Update UI
        console.log("Customer blocked successfully");
      } catch (error) {
        console.error("Failed to block customer", error);
      }
    },
    async unblockCustomer(row) {
      try {
        await api.put(`/customer/${row.customer_id}/unblock`);
        row.status = "active"; // Update UI
        console.log("Customer unblocked successfully");
      } catch (error) {
        console.error("Failed to unblock customer", error);
      }
    },
    async fetchServices() {
      this.loading = true;
      this.error = null;
      try {
        const response = await api.get("/service");
        console.log("Fetched Professional Data:", response.data); // Debugging step
        this.services = response.data;
      } catch (err) {
        this.error = "Failed to load professionals";
        console.error(err);
      } finally {
        this.loading = false;
      }
    },
    async deleteService(serviceId) {
      try {
        await api.delete(`/service/${serviceId}`);
        this.services = this.services.filter(service => service.service_id !== serviceId);
      } catch (error) {
        console.error("Failed to delete service:", error);
      }
    },
    goToService(id) {
      this.$router.push({ name: "Service", params: { id } });
    },
    async exportCsv() {
      try {
        // Start the CSV export
        await api.post('/export-csv');

        // Wait a few seconds for the file to be generated
        setTimeout(async () => {
          // Download the file
          const response = await api.get('/download-csv', { responseType: 'blob' });

          // Create a URL for the file and trigger download
          const url = window.URL.createObjectURL(new Blob([response.data]));
          const link = document.createElement('a');
          link.href = url;
          link.setAttribute('download', 'closed_service_requests.csv');
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
        }, 10000); // Adjust the delay based on how long the task takes
      } catch (error) {
        console.error('Error exporting CSV:', error);
      }
    }
  },
  mounted() {
    this.fetchProfessionals();
    this.fetchCustomers();
    this.fetchServiceRequests();
    this.fetchServices();
  }
};
</script>

<style scoped>
/* Container Styling */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  text-align: center;
}

/* Title Styling */
.title {
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 20px;
}

h3 {
  color: black;
}

.add-service-btn {
  background-color: #007bff;
  color: white;
  padding: 10px 15px;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  margin-bottom: 15px;
}

/* Grid Layout */
.services-grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 20px;
  max-width: 100%;
  margin: 0 auto;
}
</style>

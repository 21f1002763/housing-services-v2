<template>
  <div>
    <h1>Admin Dashboard</h1>
    <h3 class="mt-5">Service Professionals</h3>
    <Table :columns="professionalColumns" :data="professionals"/>
    <h3 class="mt-5">Customers</h3>
    <Table :columns="customerColumns" :data="customers"/>
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
      customers: [],
      loading: false,
      error: null,
      professionalColumns: [
        { key: "professional_id", label: "ID" },
        { key: "name", label: "Name" },
        { key: "email", label: "Email" },
        { key: "service", label: "Service" },
        { key: "experience", label: "Experience (Years)" },
        { key: "status", label: "Status" },
        { key: "actions", label: "Actions" }
      ],
      customerColumns: [
      { key: "customer_id", label: "ID" },
        { key: "name", label: "Name" },
        { key: "email", label: "Email" },
        { key: "status", label: "Status" },
        { key: "actions", label: "Actions" }
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
          name: professional.user?.name || "N/A",
          email: professional.user?.email || "N/A",
          service: professional.service?.service_name || "N/A",
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
        const response = await api.get("/customer");
        console.log("Fetched Customer Data:", response.data); // Debugging step

        this.customers = response.data.map(customer => ({
          customer_id: customer.customer_id,
          name: customer.user?.name || "N/A",
          email: customer.user?.email || "N/A",
          service: customer.service?.service_name || "N/A",
          experience: customer.experience,
          status: customer.status
        }));
      } catch (err) {
        this.error = "Failed to load professionals";
        console.error(err);
      } finally {
        this.loading = false;
      }
    }
  },
  mounted() {
    this.fetchProfessionals();
    this.fetchCustomers();
  }
};
</script>

<style scoped>
/* Add styles if needed */
</style>

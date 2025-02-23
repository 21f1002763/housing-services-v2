<template>
  <div>
    <h1>Admin Dashboard</h1>
    <Table :columns="columns" :data="professionals">
      <!-- Extract Name -->
      <template v-slot:cell(name)="props">
        {{ props.item.user?.name || "N/A" }}
      </template>

      <!-- Extract Email -->
      <template v-slot:cell(email)="props">
        {{ props.item.user?.email || "N/A" }}
      </template>

      <!-- Extract Service Name -->
      <template v-slot:cell(service)="props">
        {{ props.item.service?.service_name || "N/A" }}
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
      loading: false,
      error: null,
      columns: [
        { key: "professional_id", label: "ID" },
        { key: "name", label: "Name" },
        { key: "email", label: "Email" },
        { key: "service", label: "Service" },
        { key: "experience", label: "Experience (Years)" },
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
        console.log("Fetched Data:", response.data); // Debugging step

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
    }
  },
  mounted() {
    this.fetchProfessionals();
  }
};
</script>

<style scoped>
/* Add styles if needed */
</style>

<template>
  <div>
    <h1 style="color: black;">Professional Dashboard</h1>
    <h3 class="mt-3">Service Requests</h3>
    <Table :columns="serviceRequestColumns" :data="serviceRequests">
      <template v-slot:actions="{ row }">
        <!-- If status is "requested", show Accept and Reject buttons -->
        <template v-if="row.service_status === 'requested'">
          <button class="btn btn-success btn-sm" @click="acceptServiceRequest(row)">Accept</button>
          <button class="btn btn-danger btn-sm" @click="rejectServiceRequest(row)">Reject</button>
        </template>
      </template>
    </Table>
  </div>
</template>
  
  <script>
  import { useAuthStore } from '@/store/auth';
  import Table from "@/components/Table.vue";
  import api from "@/api";

  export default {
    components: { Table },
  data() {
    return {
      serviceRequests: [],
      loading: false,
      error: null,
      authStore: useAuthStore(),
      serviceRequestColumns: [
        { key: "request_id", label: "Request ID" },
        { key: "package_name", label: "Package Name" },
        { key: "customer_name", label: "Customer Name" },
        { key: "customer_mob_no", label: "Customer Mobile"},
        { key: "request_date", label: "Request Date" },
        { key: "complete_date", label: "Complete Date" },
        { key: "service_status", label: "Service Status" },
        { key: "service_rating", label: "Service Rating" },
        { key: "actions", label: "Actions" }
      ]
    };
  },
  methods: {
    async fetchServiceRequests() {
      this.loading = true;
      this.error = null;
      try {
        const response = await api.get(`professional/${this.authStore.userId}/service-request`);
        console.log("Fetched Service Request Data:", response.data); // Debugging step

        this.serviceRequests = response.data.map(serviceRequest => ({
          request_id: serviceRequest.request_id,
          package_name: serviceRequest.packages.package_name,
          customer_name: serviceRequest.customers.name,
          customer_mob_no: serviceRequest.customers.mobile_no,
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
    async acceptServiceRequest(row) {
      try {
        await api.put(`/service-request/${row.request_id}/accept`);
        row.service_status = "in-progress"; // Update UI
        console.log("Service request accepted successfully");
      } catch (error) {
        console.error("Failed to accept service request", error);
      }
    },
    async rejectServiceRequest(row) {
      try {
        await api.put(`/service-request/${row.request_id}/reject`);
        row.service_status = "rejected"; // Update UI
        console.log("Service request rejected successfully");
      } catch (error) {
        console.error("Failed to reject service request", error);
      }
    },
  },
  mounted() {
    this.fetchServiceRequests();
  }
  };
  </script>
  
  <style scoped>
  /* Add styles if needed */
  </style>
  
<template>
  <div class="container">
    <h1 style="color: black;">Customer Dashboard</h1>
    <h3 class="mt-3">Available Services</h3>
    <!-- Services Grid -->
    <div v-if="services.length > 0" class="services-grid">
      <ServiceCard v-for="service in services" 
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

  <div>
    <h3 class="mt-3">Service Requests</h3>
    <Table :columns="serviceRequestColumns" :data="serviceRequests">
    <template v-slot:actions="{ row }">
        <!-- If status is "requested", show Accept and Reject buttons -->
        <template v-if="row.service_status === 'requested'">
          <button class="btn btn-success btn-sm" @click="openAddRemarksModal(row)">Add Remarks</button>
        </template>

        <!-- If status is "accepted", show Block button -->
        <template v-else-if="row.service_status === 'in-progress'">
          <button class="btn btn-success btn-sm" @click="openAddRemarksModal(row)">Add Remarks</button>
          <button class="btn btn-danger btn-sm" @click="openCloseRequestModal(row)">Close Request</button>
        </template>
      </template> 
    </Table>
    <CloseRequestModal v-if="showCloseRequestModal" :requestId="selectedServiceRequestId" @close="showCloseRequestModal = false" />
    <AddRemarksModal v-if="showAddRemarksModal" :requestId="selectedServiceRequestId" @close="showAddRemarksModal = false" />
  </div>
</template>

<script>
import { useAuthStore } from '@/store/auth';
import Table from "@/components/Table.vue";
import ServiceCard from '@/components/ServiceCard.vue';
import BookServiceModal from '../../components/BookServiceModal.vue';
import CloseRequestModal from "@/components/CloseRequestModal.vue";
import api from "@/api";
import AddRemarksModal from '../../components/AddRemarksModal.vue';

export default {
  components: { Table, ServiceCard, BookServiceModal, CloseRequestModal, AddRemarksModal },
  data() {
    return {
      serviceRequests: [],
      services: [],
      showBookServiceModal: false,
      showCloseRequestModal: false,
      showAddRemarksModal: false,
      selectedServiceId: null,
      loading: false,
      error: null,
      authStore: useAuthStore(),
      serviceRequestColumns: [
        { key: "request_id", label: "Request ID" },
        { key: "package_name", label: "Package Name" },
        { key: "professional_name", label: "Professional Name" },
        { key: "professional_mob_no", label: "Professional Mobile"},
        { key: "request_date", label: "Request Date" },
        { key: "complete_date", label: "Complete Date" },
        { key: "service_status", label: "Service Status" },
        { key: "service_rating", label: "Service Rating" },
        { key: "remarks", label: "Remarks" },
        { key: "actions", label: "Actions" }
      ]
    };
  },
  methods: {
    async fetchServiceRequests() {
      this.loading = true;
      this.error = null;
      try {
        const response = await api.get(`customer/${this.authStore.userId}/service-request`);
        console.log("Fetched Service Request Data:", response.data); // Debugging step

        this.serviceRequests = response.data.map(serviceRequest => ({
          request_id: serviceRequest.request_id,
          package_name: serviceRequest.packages.package_name,
          professional_name: serviceRequest.professionals.name,
          professional_mob_no: serviceRequest.professionals.mobile_no,
          request_date: serviceRequest.request_date,
          complete_date: serviceRequest.complete_date,
          service_status: serviceRequest.service_status,
          service_rating: serviceRequest.service_rating,
          remarks: serviceRequest.remarks,
        }));
      } catch (err) {
        this.error = "Failed to load service requests";
        console.error(err);
      } finally {
        this.loading = false;
      }
    },
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
    openCloseRequestModal(row) {
      this.selectedServiceRequestId = row.request_id;
      this.showCloseRequestModal = true;
    },
    openAddRemarksModal(row) {
      this.selectedServiceRequestId = row.request_id;
      this.showAddRemarksModal = true;
    },

  },
  mounted() {
    this.fetchServiceRequests();
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
</style>
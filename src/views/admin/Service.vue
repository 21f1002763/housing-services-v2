<template>
    <div class="service-edit">
        <h1>Edit Service</h1>
        <div v-if="service">
            <label>Service Name:</label>
            <input v-model="this.service.service_name" type="text" />

            <label>Description:</label>
            <textarea v-model="this.service.description"></textarea>

            <label>Time Required (in Days):</label>
            <input v-model="this.service.time_required" type="number" min="1" max="100" />

            <button @click="updateService">Save Changes</button>
        </div>
        <div v-else>
            <p>Loading...</p>
        </div>
    </div>

    <div class="container">
        <h3 class="mt-3">Service Packages</h3>
        <!-- Add Service Button -->
        <button class="add-package-btn" @click="showAddPackageModal = true">
            + Add Package
        </button>
        <!-- Services Grid -->
        <div v-if="packages.length > 0" class="services-grid">
            <ServicePackageCard v-for="servicePackage in packages" :key="servicePackage.package_id"
                :id="servicePackage.package_id" :title="servicePackage.package_name"
                :description="servicePackage.description" :cost="servicePackage.cost" @click-card="openEditModal"
                @delete-package="deletePackage" />
        </div>

        <!-- Add Service Modal -->
        <AddPackageModal v-if="showAddPackageModal" @close="showAddPackageModal = false"
            @service-package-added="fetchPackages" />
            <!-- Edit Package Modal -->
        <EditPackageModal v-if="showEditPackageModal" :packageId="selectedPackageId" @close="showEditPackageModal = false" />
    </div>
</template>

<script>
import api from "@/api";
import ServicePackageCard from "../../components/ServicePackageCard.vue";
import AddPackageModal from "@/components/AddPackageModal.vue";
import EditPackageModal from "../../components/EditPackageModal.vue";

export default {
    components: { ServicePackageCard, AddPackageModal, EditPackageModal },
    data() {
        return {
            showAddPackageModal: false,
            showEditPackageModal: false,
            service: null,
            packages: [],
            selectedPackageId: null,
        };
    },

    methods: {
        async fetchService() {
            console.log("Fetching service details for ID:", this.$route.params.id);
            const serviceId = this.$route.params.id;
            try {
                const response = await api.get(`/service/${serviceId}`);
                console.log("Response received:", response.data);
                this.service = response.data;
            } catch (error) {
                console.error("Failed to load service details:", error);
            }
        },
        async fetchPackages() {
            this.loading = true;
            this.error = null;
            try {
                const response = await api.get(`/service/${this.$route.params.id}/service-package`);
                console.log("Fetched Service Package Data:", response.data); // Debugging step
                this.packages = response.data;
            } catch (err) {
                this.error = "Failed to load service packages";
                console.error(err);
            } finally {
                this.loading = false;
            }
        },
        async updateService() {
            try {
                const response = await api.put(`/service/${this.service.service_id}`, {
                    service_name: this.service.service_name,
                    description: this.service.description,
                    time_required: this.service.time_required,
                });
                if (response.status == 200) {
                    console.log("Service updated successfully:", response.data);
                    alert("Service updated successfully!");
                }
            } catch (error) {
                console.error("Update failed:", error);
                // Handle server response errors
                if (error.response) {
                    alert(error.response.data.message || "Failed to update service.");
                } else if (error.request) {
                    alert("No response from server. Please check your network.");
                } else {
                    alert("An unexpected error occurred.");
                }
            }
        },
        openEditModal(packageId) {
      this.selectedPackageId = packageId;
      this.showEditPackageModal = true;
    },
        async deletePackage(packageId) {
            try {
                await api.delete(`/service-package/${packageId}`);
                this.packages = this.packages.filter(servicePackage => servicePackage.package_id !== packageId);
            } catch (error) {
                console.error("Failed to delete service:", error);
            }
        },
    },
    mounted() {
        this.fetchService();
        this.fetchPackages();
    }
};
</script>

<style scoped>
.service-edit {
    max-width: 600px;
    margin: auto;
}

label {
    display: block;
    font-weight: bold;
}

input,
textarea {
    width: 100%;
    margin-bottom: 10px;
}

.add-package-btn {
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
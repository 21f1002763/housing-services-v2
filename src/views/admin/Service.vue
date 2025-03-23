<template>
    <div class="service-edit">
        <h1>Edit Service</h1>
        <div v-if="service">
            <label>Service Name:</label>
            <input v-model="service.service_name" type="text" />

            <label>Description:</label>
            <textarea v-model="service.description"></textarea>

            <button @click="updateService">Save Changes</button>
        </div>
        <div v-else>
            <p>Loading...</p>
        </div>
    </div>
</template>

<script>
import api from "@/api";

export default {
    data() {
        return {
            service: null,
        };
    },
    async created() {
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
    methods: {
        async updateService() {
            try {
                await api.put(`/service/${this.service.service_id}`, this.service);
                alert("Service updated successfully!");
            } catch (error) {
                console.error("Update failed:", error);
            }
        },
    },
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
</style>
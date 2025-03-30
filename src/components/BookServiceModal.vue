<template>
    <div class="modal-overlay">
      <div class="modal">
        <div style="width: 100%;">
        <h4>Book a Service</h4>
  
        <!-- Service Packages -->
        <div>
          <h5>Select a Package</h5>
          <div v-if="packages.length" class="package-list">
            <label v-for="pkg in packages" :key="pkg.package_id" class="package-item">
              <input type="radio" v-model="selectedPackage" :value="pkg.package_id" />
              {{ pkg.package_name }} ({{ pkg.cost }} Rupees)
            </label>
          </div>
          <p v-else>No packages available</p>
        </div>
  
        <!-- Service Professionals -->
        <div>
          <h5 class="mt-3">Select a Professional</h5>
          <div v-if="professionals.length" class="professional-list">
            <label v-for="pro in professionals" :key="pro.professional_id" class="professional-item">
              <input type="radio" v-model="selectedProfessional" :value="pro.professional_id" />
              {{ pro.name }} ({{ pro.city.city_name }})
              {{ pro.experience }} years of experience
            </label>
          </div>
          <p v-else>No professionals available</p>
        </div>
  
        <!-- Buttons -->
        <div class="button-group mt-3">
          <button @click="bookService" :disabled="!selectedPackage || !selectedProfessional">
            Book Now
          </button>
          <button @click="$emit('close')">Cancel</button>
        </div>
      </div>
    </div>
    </div>
  </template>
  
  <script>
  import api from "@/api";
  
  export default {
    props: {
      serviceId: Number
    },
    data() {
      return {
        packages: [],
        professionals: [],
        selectedPackage: null,
        selectedProfessional: null,
      };
    },
    async mounted() {
      await this.fetchData();
    },
    methods: {
      async fetchData() {
        try {
          // Fetch service packages
          const packageResponse = await api.get(`/service/${this.serviceId}/service-package`);
          this.packages = packageResponse.data;
  
          // Fetch professionals
          const professionalResponse = await api.get(`/customer/${this.$route.params.id}/professionals/${this.serviceId}`);
          this.professionals = professionalResponse.data;
        } catch (error) {
          console.error("Error fetching data:", error);
        }
      },
      async bookService() {
        try {
          await api.post("/service-request", {
            user_id: this.$route.params.id,
            package_id: this.selectedPackage,
            professional_id: this.selectedProfessional
          });
  
          alert("Service booked successfully!");
          this.$emit("service-booked");
          this.$emit("close");
          window.location.reload();
        } catch (error) {
          console.error("Booking failed:", error);
        }
      }
    }
  };
  </script>
  
  <style scoped>
  /* Overlay (background) */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5); /* Dim background */
  display: flex;
  justify-content: center;
  align-items: center;
}

/* Center modal properly */
.modal {
  background: white;
  padding: 20px;
  border-radius: 10px;
  width:30%;
  height: fit-content;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  
  /* Centering */
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  justify-content: center;
  align-items: center;

  /* Fix stacking issue */
  display: flex;
  flex-direction: column;
  gap: 15px; /* Space between elements */
}

/* Heading */
h2 {
  text-align: center;
}

/* Input and Textarea */
input, textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px;
  box-sizing: border-box;
  display: block; /* Ensures block-level behavior */
}

/* Textarea Adjustments */
textarea {
  min-height: 80px;
  resize: vertical;
}

/* Button Group */
.button-group {
  display: flex;
  justify-content: space-between;
  gap: 10px;
}

/* Buttons */
button {
  flex: 1;
  padding: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
}

button:first-of-type {
  background: #007bff;
  color: white;
}

button:last-of-type {
  background: #ccc;
}

/* Ensure modal is not hidden */
.modal-overlay,
.modal {
  display: flex;
}
  /* Package and Professional List */
.package-list, .professional-list {
  display: flex;
  flex-direction: column;
  width:100%;
  gap: 10px;
}

/* Package and Professional Item */
.package-item, .professional-item {
  display: flex;
  align-items: center;
  width: 100%; /* Make them take full width */
  padding: 12px; /* Increase padding */
  border: 1px solid #ddd;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.2s;
}

.package-item:hover, .professional-item:hover {
  background: #f9f9f9;
}

/* Radio Buttons */
input[type="radio"] {
  accent-color: #007bff;
  margin-right: 10px; /* Add spacing between radio and text */
  width: fit-content;
}
  </style>
  
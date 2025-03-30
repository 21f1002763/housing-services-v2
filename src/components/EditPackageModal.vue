<template>
  <div class="modal-overlay">
    <div class="modal">
      <h2>Edit Package</h2>

      <input v-model="this.package.package_name" type="text" placeholder="Package Name" />
      <textarea v-model="this.package.description" placeholder="Description"></textarea>
      <input v-model="this.package.cost" type="number" min="1" max="100" placeholder="Time Required (in Days)" />

      <div class="button-group">
        <button @click="editPackage">Save</button>
        <button @click="$emit('close')">Cancel</button>
      </div>
    </div>
  </div>
</template>

<script>
import api from "@/api";

export default {
  props: {
    packageId: Number
  },
  data() {
    return {
      packageName: "",
      description: "",
      package: {}
    };
  },
  methods: {
    async getPackage() {
      try {
        const response = await api.get(`/service-package/${this.packageId}`);
        this.package = response.data;
      } catch (error) {
        console.error("Failed to load package details:", error);
      }
    },
    async editPackage() {
      try {
        const response = await api.put(`/service-package/${this.packageId}`, {
          service_id: this.$route.params.id,
          package_name: this.package.package_name,
          description: this.package.description,
          cost: this.package.cost,
        });
        this.$emit("package-edited");
        this.$emit("close");
        if (response.status === 200) {
          console.log("Service Package updated successfully:", response.data);
          alert("Service Package updated successfully!");
        }
      } catch (error) {
        console.error("Update failed:", error);
        // Handle server response errors
        if (error.response) {
          alert(error.response.data.message || "Failed to update service package.");
        } else if (error.request) {
          alert("No response from server. Please check your network.");
        } else {
          alert("An unexpected error occurred.");
        }
      }
    },
  },
  mounted() {
    this.getPackage();
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
  background: rgba(0, 0, 0, 0.5);
  /* Dim background */
  display: flex;
  justify-content: center;
  align-items: center;
}

/* Center modal properly */
.modal {
  background: white;
  padding: 20px;
  border-radius: 10px;
  width: 400px;
  height: fit-content;
  max-width: 90%;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);

  /* Centering */
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  box-sizing: border-box;
  justify-content: center;
  align-items: center;

  /* Fix stacking issue */
  display: flex;
  flex-direction: column;
  gap: 15px;
  /* Space between elements */
}

/* Heading */
h2 {
  text-align: center;
}

/* Input and Textarea */
input,
textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px;
  box-sizing: border-box;
  display: block;
  /* Ensures block-level behavior */
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
</style>
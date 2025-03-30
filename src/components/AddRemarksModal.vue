<template>
  <div class="modal-overlay">
    <div class="modal">
      <h2>Add Package</h2>

      <input v-model="remarks" type="text" placeholder="Remarks (if any)" />

      <div class="button-group">
        <button @click="editRequest">Save</button>
        <button @click="$emit('close')">Cancel</button>
      </div>
    </div>
  </div>
</template>

<script>
import api from "@/api";

export default {
  props: {
    requestId: Number,
  },
  data() {
    return {
      remarks: "",
      rating: null,

    };
  },
  methods: {
    async editRequest() {
      try {
        await api.put(`/service-request/${this.requestId}`, {
          remarks: this.remarks,
        });
        this.$emit("service-request-edited");
        this.$emit("close");
        window.location.reload();
      } catch (error) {
        console.error("Failed to edit service request", error);
      }
    },
  },
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
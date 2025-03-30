<template>
  <div class="card" @click="$emit('click-card', id)">
    <!-- Delete Icon (Bootstrap Icons) -->
    <button v-if="!hideDelete" class="delete-btn" @click.stop="confirmDelete">
      <i class="bi bi-trash"></i>
    </button>

    <div class="card-content">
      <h3 class="card-title">{{ title }}</h3>
      <p class="card-description">{{ description }}</p>
      <p class="card-description">Time Required: {{ time_required }} Days</p>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    id: Number,
    title: String,
    description: String,
    time_required: String,
    hideDelete: Boolean
  },
  methods: {
    confirmDelete() {
      if (confirm("Are you sure you want to delete this service?")) {
        this.$emit("delete-service", this.id);
      }
    }
  }
};
</script>

<style scoped>
.card {
  position: relative;
  width: 25%;
  background: white;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: 0.3s;
}

.card:hover {
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

/* 🔴 Small Delete Button */
.delete-btn {
  position: absolute;
  top: 5px;
  right: 5px;
  background-color: red;
  border: black;
  font-size: 12px; /* Smaller icon */
  cursor: pointer;
  padding: 3px;
  width: 24px; /* Small button */
  height: 24px; /* Small button */
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 5px;
}

.delete-btn i {
  color: white !important;
  font-size: 15px; /* Smaller icon */
}

.delete-btn:hover {
  background-color: darkred !important;
}
</style>

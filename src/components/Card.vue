<template>
    <div class="card" @click="$emit('click-card', id)">
      <div class="card-content">
        <h3 class="card-title">{{ title }}</h3>
        <p class="card-description">{{ description }}</p>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      id: Number,
      title: String,
      description: String
    }
  };
  </script>
  
  <style scoped>
  /* Card Styling */
  .card {
    background: white;
    border-radius: 10px;
    padding: 15px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    cursor: pointer;
  }
  
  .card:hover {
    transform: scale(1.03);
    box-shadow: 0 6px 10px rgba(0, 0, 0, 0.15);
  }
  
  .card-content {
    text-align: center;
  }
  
  .card-title {
    font-size: 18px;
    font-weight: bold;
  }
  
  .card-description {
    color: gray;
    font-size: 14px;
  }
  
  .view-details {
    margin-top: 10px;
    color: blue;
    text-decoration: underline;
    border: none;
    background: none;
    cursor: pointer;
  }
  
  .view-details:hover {
    color: darkblue;
  }
  </style>
  
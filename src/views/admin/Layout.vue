<template>
  <div class="admin-layout">
    <!-- Sidebar Navigation -->
    <aside class="sidebar">
      <div class="icon-container">
        <router-link to="/admin/profile">
        <div class="icon d-flex align-items-center justify-content-center">
          <span class="fa fa-user"></span>
        </div>
        </router-link>
        <h2>Admin Panel</h2>
      </div>

      <nav>
        <ul>
          <li><router-link to="/admin/dashboard" active-class="active-link">Dashboard</router-link></li>
          <li><router-link to="/admin/search" active-class="active-link">Search</router-link></li>
          <li><router-link to="/admin/summary" active-class="active-link">Summary</router-link></li>
        </ul>
      </nav>
    </aside>

    <!-- Main Content Area -->
    <main class="content">
      <router-view />
    </main>
  </div>
</template>

<script>
export default {
  name: "AdminLayout",
};
</script>

<style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
}

/* Sidebar Styles */
.sidebar {
  min-width: 300px;
  background-color: #483434;
  color: white;
  padding: 20px;
  min-height: 100vh;
}

.sidebar h2 {
  text-align: center;
  font-size: 1.5rem;
  margin-left: 15px;
  color: #ffff;
  font-weight: bold;
}

.sidebar nav ul {
  list-style: none;
  padding: 0;
}

.sidebar nav ul li {
  margin: 15px 0;
}

.sidebar nav ul li a {
  color: white;
  text-decoration: none;
  display: block;
  padding: 10px;
}

.sidebar nav ul li a:hover {
  background-color: #4caf50;
  /* Green */
  color: white;
  font-weight: bold;
  border-radius: 5px;
}

/* Main Content */
.content {
  flex-grow: 1;
  padding: 20px;
}

.active-link {
  background-color: #4caf50;
  /* Green */
  color: white;
  font-weight: bold;
  padding: 8px 12px;
  border-radius: 5px;
}

.icon-container {
  display: flex;
  align-items: center; /* Align icon and text vertically */
}

.icon {
  width: 50px;
  height: 50px;
  background: #ffff;
  font-size: 30px;
  border-radius: 30px;
  display: flex;
  align-items: center;
  justify-content: center; /* Space between icon and heading */
}

.icon span {
  color: #483434;
}

</style>

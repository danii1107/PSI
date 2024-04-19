<template>
    <nav class="navbar">
      <ul>
        <li><router-link to="/">Home</router-link></li>
        <li><button @click="logout">Log-out</button></li>
      </ul>
    </nav>
  </template>
  
  <script>
  export default {
    methods: {
      logout() {
        // Redirigir al usuario a la página /logout
        this.$router.push('/log-out');
      }
    }
  };
  </script>
  
<style scoped>
.navbar {
  background-color: #4d4f57;
  color: white;
  width: 100%;
  padding: 12px 0;
}

.navbar ul {
  list-style-type: none;
  margin: 0;
  padding: 0;
}

.navbar ul li {
  display: inline;
  margin-right: 20px;
}

.navbar ul li button {
  background: none;
  border: none;
  color: rgb(204, 27, 204);
  cursor: pointer;
}
</style>
  
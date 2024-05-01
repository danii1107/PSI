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
        this.$router.push('/log-out');
      }
    }
  };
  </script>
  
<style scoped>
.navbar {
  background-color: #3d3d3c;
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
  color: rgb(245, 244, 245);
  cursor: pointer;
}
</style>
  
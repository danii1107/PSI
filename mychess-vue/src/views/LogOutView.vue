<template>
	<div class="background-image">
		<div class="container">
		<h1>Logout</h1>
		<p>Has cerrado sesión exitosamente. Serás redirigido a la página de inicio en 5 segundos.</p>
		</div>
	</div>
  </template>
  
  <script>
import { useTokenStore } from '../stores/token';


  export default {
	
	name: 'LogOutView',

	setup() {
		const store = useTokenStore();
	},
	mounted() {
	  this.logout();
	},
	methods: {
	  logout() {
		store.removeToken();
		setTimeout(() => {
		  this.$router.push("/log-in");
		}, 5000);
	  }
	}
  }
  </script>
  
  <style scoped>
	.background-image {
		width: 100vw;
		height: 100vh;
		background-image: url('../assets/REINA.jpg');
		background-size: cover;
		background-repeat: no-repeat;
		background-position: center;
	}

	.container {
		color: white;
		text-align: center;
	}
  </style>
  

<template>
	<div>
	  <h1>Logout</h1>
	  <p>Has cerrado sesión exitosamente. Serás redirigido a la página de inicio en 5 segundos.</p>
	</div>
  </template>
  
  <script>
  import iconoCerrarSesion from '@/assets/icono-cerrar-sesion.jpg'; // Asegúrate de que la ruta sea correcta

  export default {
	
	name: 'LogOutView',

	data() {
		return {
			// Asigna la ruta de la imagen a una propiedad de datos
			imagenSrc: iconoCerrarSesion
		};
	},

	mounted() {
	  // Simula la lógica de logout
	  this.logout();
	},
	methods: {
	  logout() {
		// Aquí iría la lógica real de logout, como eliminar variables de sesión
		// Simulamos el redireccionamiento después de 5 segundos
		setTimeout(() => {
		  this.$router.push({ name: 'home_page' }); // Redirecciona a la página de inicio
		}, 5000);
	  }
	}
  }
  </script>
  
  <style scoped>
  /* Estilos opcionales para el componente */
  </style>
  

<template>
	<div>
	  <h1 style="font-size: 24px;">Registro</h1>
	  <form @submit.prevent="submitForm">
		<div>
		  <label for="email">Email:</label>
		  <input type="email" id="email" v-model="email" required>
		</div>
		<div>
		  <label for="password">Contraseña:</label>
		  <input type="password" id="password" v-model="password" required>
		</div>
		<div>
		  <label for="confirmPassword">Confirmar Contraseña:</label>
		  <input type="password" id="confirmPassword" v-model="confirmPassword" required>
		</div>
		<button type="submit">Registrarse</button>
	  </form>
	</div>
  </template>
  
  <script>
  export default {
	data() {
	  return {
		email: '',
		password: '',
		confirmPassword: ''
	  };
	},
	methods: {
	  submitForm() {
		// Verificar si las contraseñas coinciden
		if (this.password !== this.confirmPassword) {
		  alert('Las contraseñas no coinciden');
		  return;
		}
  
		// Aquí iría tu lógica para enviar los datos al servidor, por ejemplo, utilizando axios para hacer una solicitud POST al endpoint de registro
  
		// Simulación de éxito
		// Aquí deberías enviar los datos al servidor para procesar el registro
		// Si la operación es exitosa, puedes redirigir al usuario a la página de inicio de sesión
		alert('¡Registro exitoso!');
		// Redireccionar a la página de inicio de sesión
		this.$router.push('/log-in');
	  }
	}
  };
  </script>
  
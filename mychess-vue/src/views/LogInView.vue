<template>
		<div class="container">
		<h2>Bienvenido/a</h2>
		<form v-if="!showRegisterForm" @submit.prevent="login">
			<input type="email" v-model="loginEmail" placeholder="Correo electrónico" required>
			<input type="password" v-model="loginPassword" placeholder="Contraseña" required>
			<button type="submit">Iniciar Sesión</button>
		</form>
		<p v-if="!showRegisterForm">¿No tienes cuenta? <span class="toggle" @click="toggleForm">Regístrate aquí</span></p>
		<form v-else @submit.prevent="register">
			<input type="text" v-model="registerFullName" placeholder="Nombre completo" required>
			<input type="email" v-model="registerEmail" placeholder="Correo electrónico" required>
			<input type="password" v-model="registerPassword" placeholder="Contraseña" required>
			<button type="submit">Registrarse</button>
		</form>
		</div>
  </template>
  
  <script>
  export default {
	data() {
	  return {
		showRegisterForm: false,
		loginEmail: '',
		loginPassword: '',
		registerFullName: '',
		registerEmail: '',
		registerPassword: '',
	  };
	},
	methods: {
	  toggleForm() {
		this.showRegisterForm = !this.showRegisterForm;
	  },
	  login() {
		// Implement login logic here
		alert('Login attempted');
	  },
	  register() {
		// Implement register logic here
		alert('Register attempted');
	  },
	},
  };
  </script>
  
  <style scoped>
  .container {
	background-color: transparent;
	margin: auto;
	width: 50%;
	padding: 20px;
	text-align: center;
  }
  input, button {
	width: 80%;
	padding: 12px 20px;
	margin: 8px 0;
	display: inline-block;
	border: 1px solid #ccc;
	box-sizing: border-box;
  }
  button {
	background-color: #4CAF50;
	color: white;
	border: none;
	cursor: pointer;
  }
  button:hover {
	opacity: 0.8;
  }
  .toggle {
	color: blue;
	cursor: pointer;
  }
  
  </style>
  
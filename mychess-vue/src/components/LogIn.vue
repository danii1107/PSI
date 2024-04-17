<template>
	<div class="container">
		<form v-if="!showRegisterForm" @submit.prevent="login">
			<input type="email" v-model="loginEmail" placeholder="Correo electrónico" required>
			<input type="password" v-model="loginPassword" placeholder="Contraseña" required>
			<button type="submit">Iniciar Sesión</button>
		</form>
		<p class="register" v-if="!showRegisterForm">¿No tienes cuenta? <span class="toggle" @click="toggleForm">Regístrate aquí</span></p>
	</div>
</template>

<script>
	export default {
		data() {
			return {
				loginEmail: '',
				loginPassword: ''
			};
		},
		methods: {
			handleLogin() {
				console.log('Login');
			},
			toggleForm() {
				this.$router.push('/sign-up');
			}
		}
	}
</script>

<style scoped>
	.container {
		margin-right: 20px;
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
		background-color: #6d260a;
		color: white;
		border: none;
		cursor: pointer;
	}
	button:hover {
		opacity: 0.8;
	}
	.toggle {
		color: whitesmoke;
		cursor: pointer;
	}
	.register {
		color: white;
	}
</style>
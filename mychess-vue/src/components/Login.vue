<template>
	<div class="container">
		<form @submit.prevent="handleLogin">
			<input type="email" v-model="persona.email" placeholder="Correo electrónico" required>
			<input type="password" v-model="persona.password" placeholder="Contraseña" required>
			<button type="submit">Iniciar Sesión</button>
		</form>
	</div>
</template>

<script>
	export default {
		name: "login",
		emits: ['LoginAPI'],
		data() {
			return {
				persona: {
					email: "",
					password: "",
				},
			};
		},
		methods: {
			handleLogin() {
				this.$emit('LoginAPI', this.persona);
				this.persona = {
					email: "",
					password: "",
				};
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
</style>
<template>
	<div class="container">
		<form @submit.prevent="handleLogin">
			<input type="username" v-model="persona.username" placeholder="Nombre de usuario" required>
			<input type="password" v-model="persona.password" placeholder="Contraseña" required>
			<button type="submit">Iniciar Sesión</button>
		</form>
	</div>
</template>

<script>
	export default {
		emits: ['LoginAPI'],
		data() {
			return {
				persona: {
					username: "",
					password: "",
				},
			};
		},
		methods: {
			handleLogin() {
				this.$emit('LoginAPI', this.persona);
				this.persona = {
					username: "",
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
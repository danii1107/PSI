<template>
  <div class="container">
    <form @submit.prevent="handleSignup">
      <input type="email" v-model="persona.email" placeholder="Correo electrónico" required>
      <input type="password" v-model="persona.password" placeholder="Contraseña" required>
      <input type="password" v-model="persona.repeatpwd" placeholder="Repite la contraseña" required>
      <button type="submit">Registrarse</button>
    </form>
  </div>
</template>
  
<script>
  export default {
    name: "signup",
		emits: ['SignupAPI'],
		data() {
			return {
				persona: {
					username: "",
					password: "",
          repeatpwd: "",
          email: "",
				},
			};
		},
		methods: {
			handleSignup() {
        this.persona.username = this.persona.email.split("@")[0];
				this.$emit('SignupAPI', this.persona);
				this.persona = {
					username: "",
					password: "",
          email: "",
				};
			}
		}
	}
</script>
  
<style scoped>
  .container {
		margin-left: 20px;
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
  
<template>
	<div class="wrapper">
		<h2>Welcome</h2>
		<form @submit.prevent="handleLogin">
			<div class="input-field">
				<input type="email" id="email" v-model="persona.username" placeholder="E-mail" required>
				<i class='bx bxs-user'></i>
			</div>
			<div class="input-field">
				<input type="password" id="password" v-model="persona.password" placeholder="Password" required>
				<i class='bx bxs-lock-alt'></i>
			</div>
			<a href="#" class="forgot">
				<p>Forgot password?</p>
			</a>
			<button type="submit" class="login">Login</button>
			<p class="sign-up">Don't have an account? <span class="sign-up" @click="toggleForm">sign up</span></p>
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
					username: "",
					password: "",
				},
			};
		},
		methods: {
			handleLogin() {
				this.persona.username = this.persona.username.split("@")[0];
				this.$emit('LoginAPI', this.persona);
				this.persona = {
					username: "",
					password: "",
				};
				this.$router.push('/creategame');
			},
			toggleForm() {
				this.$router.push('/sign-up');
			}
		}
	}
</script>

<style scoped>
	.wrapper {
		position: absolute;
		top: 50%;
		left: 50%;
		transform: translate(-50%, -50%);
		width: 350px;
		height: 350px;
		text-align: center;
		border: 1px solid rgb(241, 241, 241);
		border-radius: 12px;
		padding: 10px 20px;
		background: transparent;
		backdrop-filter: blur(6px);
		box-shadow: 5px 5px 10px 0 rgba(255, 255, 255, 0.5);
	}

	.wrapper h2 { 
		font-size: 30px;
		color: #fffefe;
	}

	.input-field {
		position: relative;
	}

	.input-field input[type="email"],
	.input-field input[type="password"] {
		border-radius: 10px;
		background: transparent;
		margin: 15px;
		border: 2px solid rgb(255, 255, 255);
		width: 280px;
		height: 2px;
		padding: 20px 20px 20px 20px;
		backdrop-filter: blur(15px);
		color: rgb(255, 255, 255);
	}

	.input-field i {
		position: absolute;
		top: 50%;
		right: 10px;
		transform: translateY(-50%);
		color: rgb(252, 252, 252);
	}

	input::placeholder {
		color: rgb(255, 255, 255);
	}

	.input-field input[type="email"]:focus::placeholder,
	.input-field input[type="password"]:focus::placeholder {
		transform: translateY(-100%);
		transition: transform 0.2s ease-in-out;
		font-size: 14px;
	}

	.input-field input[type="email"]:focus::placeholder,
	.input-field input[type="password"]:focus::placeholder {
		transform: translateY(0%);
		transition: transform 0.2s ease-in-out;
		font-size: 16px;
	}

	a.forgot {
		color: rgb(255, 255, 255, 0.712);
		text-decoration: none;
		position: relative;
	}

	a.forgot:hover {
		text-decoration: underline;
		color: #fffffffd;
	}

	p.sign-up {
		color: rgb(255, 255, 255, 0.712);
	}

	a.sign-up {
		color: rgb(255, 255, 255, 0.712);
		text-decoration: none;
	}

	span.sign-up:hover {
		text-decoration: underline;
		color: #fffffffd;
	}

	.wrapper .login {
		background: #fff;
		border: none;
		outline: none;
		cursor: pointer;
		font-weight: 600;
		border-radius: 45px;
		width: 200px;
		height: 30px;
	}

</style>
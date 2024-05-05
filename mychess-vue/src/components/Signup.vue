<template>
  <div class="wrapper">
    <h2>Welcome</h2>
    <form @submit.prevent="handleSignup">
      <div class="input-field">
        <input
          id="email"
          v-model="persona.email"
          type="email"
          placeholder="E-mail"
          required
          data-cy="username"
        >
        <i class="bx bxs-user" />
      </div>
      <div class="input-field">
        <input
          id="password"
          v-model="persona.password"
          type="password"
          placeholder="Password"
          required
          data-cy="password1"
        >
        <i class="bx bxs-lock-alt" />
      </div>
      <div class="input-field">
        <input
          id="repeat-password"
          v-model="confirmPassword"
          type="password"
          placeholder="Repeat password"
          required
          data-cy="password2"
        >
        <i class="bx bxs-lock-alt" />
      </div>
      <p
        v-if="passwordMismatch"
        class="missmatch"
        data-cy="error-message"
      >
        Passwords do not match!
      </p>
      <br v-else>
      <button
        type="submit"
        class="login"
        data-cy="signup-button"
      >
        Sign Up
      </button>
      <p class="sign-up">
        Already have an account? <span
          class="sign-up"
          @click="toggleForm"
        >log in</span>
      </p>
    </form>
  </div>
</template>
  
  <script>
  export default {
	name: "SignUp",
	emits: ['SignupAPI'],
	data() {
	  return {
		persona: {
		  username: "",
		  password: "",
		  email: "",
		},
		confirmPassword: "",
		passwordMismatch: false
	  };
	},
	methods: {
	  handleSignup() {
		if (this.persona.password === this.confirmPassword) {
		  this.passwordMismatch = false;
		  this.persona.username = this.persona.email;
		  console.log(this.persona);
		  this.$emit('SignupAPI', this.persona);
		  this.resetPersona();
		  this.$router.push('/log-in');
		} else {
		  this.passwordMismatch = true;
		}
	  },
	  resetPersona() {
		this.persona = {
		  username: "",
		  password: "",
		  email: "",
		};
		this.confirmPassword = "";
	  },
	  toggleForm() {
		this.$router.push('/log-in');
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
		height: 425px;
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

	.missmatch {
		color: white;
	}
</style>
  
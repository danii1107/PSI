<template>
    <div class="signup-container">
      <form @submit.prevent="submitForm" class="registration-form">
        <input type="email" id="email" v-model="email" placeholder="Email" required>
        <input type="password" id="password" v-model="password" placeholder="Contraseña" required>
        <input type="password" id="confirmPassword" v-model="confirmPassword" placeholder="Confirmar contraseña" required>
        <button type="submit" class="signup-button">Registrarse</button>
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
  
  <style scoped>
  .signup-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
  }
  
  .registration-form {
    width: 500px;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 5px;
    background-color: #f9f9f9;
  }

  input, button {
		width: 90%;
		padding: 12px 20px;
		margin: 8px 0;
		display: inline-block;
		border: 1px solid #ccc;
		box-sizing: border-box;
	}

  
  label {
    font-weight: bold;
  }
  
  .signup-button {
    background-color: #6d260a;
	color: white;
	border: none;
	cursor: pointer;
  }
  
  .signup-button:hover {
    opacity: 0.8;
  }
  </style>
  
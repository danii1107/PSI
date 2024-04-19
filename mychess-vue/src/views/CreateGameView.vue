<template>
	<div class="container">
	  <header>
		<label>Join or create a game</label>
	  </header>
  
	  <nav>
		<!-- Contenido de la barra de navegación (nav) -->
	  </nav>
  
	  <div class="main-content">
		<article>
		  <!-- Contenido principal del artículo (article) -->
		  <section>
			<!-- Contenido del artículo (section) -->
		  </section>
		</article>
  
		<aside>
		  <!-- Contenido del aside -->
		  <div>
			<label for="gameType">Select game type:</label>
			<form @submit.prevent="submitForm">
			  <select id="gameType" v-model="selectedGameType">
				<option value="any">Join any game</option>
				<option value="specific">Join specific game</option>
			  </select>
			  <input v-if="selectedGameType === 'specific'" type="text" v-model="gameID" placeholder="Enter game ID">
			  <button type="submit">Join Game</button>
			</form>
		  </div>
		</aside>
	  </div>
  
	  <footer>
		<!-- Contenido del pie de página (footer) -->
	  </footer>
	</div>
  </template>
  
  <script>
  export default {
	name: 'CreateGameView',
	components: {
  	},
	data() {
	  return {
		selectedGameType: 'any',
		gameID: ''
	  };
	},
	methods: {
	  submitForm() {
		if (this.selectedGameType === 'any') {
		  console.log('Joining any game');
		} else {
		  console.log('Joining specific game with ID:', this.gameID);
		}
	  }
	}
  }
  </script>
  
  <style scoped>
  .container {
	display: flex;
	flex-direction: column;
	align-items: center;
  }
  
  .main-content {
	display: flex;
	justify-content: space-between;
	width: 80%; /* ajusta el ancho del contenido principal */
  }
  
  main-content > article {
	width: 50%;
	align-items: center;
  }
  
  main-content > aside {
	width: 50%; /* el aside ocupará la mitad del espacio disponible */
	align-items: center;
  }
  
  /* Estilos específicos del componente van aquí */
  </style>
  
<template>
	<div class="container">
	  <header>
		<label>Join or create a game</label>
	  </header>
  
	  <Navbar />
  
	  <div class="main-content">
		<article>
		  <section>
			<CreateGame />
		  </section>
		</article>
  
		<aside>	
          <img src="../assets/REINA.jpg" alt="Reina" class="section-image">
		</aside>
	  </div>
  
	  <footer>

	  </footer>
	</div>
  </template>
  
  <script>
  import Navbar from '../components/Navbar.vue';
  import CreateGame from '../components/CreateGame.vue';
  
  export default {
	components: {
	  CreateGame,
	  Navbar
	}
  };
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
	width: 80%; 
  }
  
  main-content > article {
	width: 70%;
	align-items: center;
  }
  
  main-content > aside {
	width: 100%;
	align-items: center;
	justify-content: center;

  }
  
  .section-image {
  max-width: 100%;
  max-height: 100%;
}
  </style>
  
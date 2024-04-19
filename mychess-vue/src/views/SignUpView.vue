<template>
	<div class="background-image">
	  <Signup />
	</div>
</template>
  
<script>
  import Signup from '../components/Signup.vue';
  
  export default {
	components: {
	  Signup
	}
  };
</script>

<style scoped>
	.background-image {
		display: flex;
		align-items: center; /* Alinea verticalmente al centro */
		justify-content: center; /* Alinea horizontalmente a la derecha */
		width: 100vw;
		height: 100vh;
		background-image: url('../assets/logn-bg.jpg');
		background-size: cover;
		background-repeat: no-repeat;
		background-position: center;
	} 
</style>
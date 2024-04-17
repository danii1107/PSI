<template>
	<div class="background-image">
	  <log-in @login="handleLogin"></log-in>
	</div>
</template>
  
<script>
	import LogIn from '../components/LogIn.vue';

	export default {
		components: {
			LogIn
		},
	}
</script>
  
<style scoped>
	.background-image {
		display: flex;
		align-items: center; /* Alinea verticalmente al centro */
		justify-content: flex-end; /* Alinea horizontalmente a la derecha */
		width: 100vw;
		height: 100vh;
		background-image: url('../assets/logn-bg.jpg');
		background-size: cover;
		background-repeat: no-repeat;
		background-position: center;
	} 
</style>
  
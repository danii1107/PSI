<template>
	<div class="background-image">
		<login @LoginAPI="consumeAPI" />
	</div>
</template>
  
<script>
	import Login from '../components/Login.vue';
	import { ref, onMounted } from 'vue';
	import { useCounterStore } from '../stores/counter';

	const apiURL = import.meta.env.VITE_DJANGOURL

	export default {
		components: {
			Login
		},
		setup() {
			const personas = ref([]);
    		const store = useCounterStore();

			const consumeAPI = async (persona) => {
				try {
					const response = await fetch(
						apiURL + '/api/v1/token/login/', {
							method: 'POST',
							body: JSON.stringify(persona),
							headers: { 'Content-type': 'application/json; charset=UTF-8' },
						}	
					);
					if (response.ok) {
						const personaCreada = await response.json();
						personas.value = [...personas.value, personaCreada];
						store.increment();
					}
				} catch (error) {
					console.error(error);
				}
			};

			return {
				personas,
				consumeAPI,
				store,	
			}
		}
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
  
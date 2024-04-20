<template>
	<div class="background-image">
		<signup @SignupAPI="consumeAPI" />
	</div>
</template>
  
<script>
	import Signup from '../components/Signup.vue';
	import { ref, onMounted } from 'vue';
	import { useCounterStore } from '../stores/counter';

	const apiURL = import.meta.env.VITE_DJANGOURL

	export default {
		components: {
			Signup
		},
		setup() {
			const personas = ref([]);
    		const store = useCounterStore();

			const consumeAPI = async (persona) => {
				try {
					const response = await fetch(
						apiURL + '/api/v1/users/', {
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
		width: 100vw;
		height: 100vh;
		background-image: url('../assets/sign-up-bg.jpg');
		background-size: cover;
		background-repeat: no-repeat;
		background-position: bottom;
	} 
</style>
  
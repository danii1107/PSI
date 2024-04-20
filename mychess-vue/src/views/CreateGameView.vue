<template>
	<div class="container">
		<create-game @newGame="consumeAPInew"/>
	</div>
  </template>
  
<script>
	import Navbar from '../components/Navbar.vue';
	import CreateGame from '../components/CreateGame.vue';
	import { ref, onMounted } from 'vue';
	import { useCounterStore } from '../stores/counter';

	const apiURL = import.meta.env.VITE_DJANGOURL

	export default {
		components: {
			CreateGame,
			Navbar
		},
		setup() {
			const games = ref([]);
    		const store = useCounterStore();

			const consumeAPInew = async () => {
				try {
					const response = await fetch(
						apiURL + '/api/v1/games/', {
							method: 'POST',
							body: {},
							headers: { 'Content-type': 'application/json; charset=UTF-8' },
						}	
					);
					if (response.ok) {
						const newGame = await response.json();
						games.value = [...games.value, newGame];
						store.increment();
					}
				} catch (error) {
					console.error(error);
				}
			};

			const consumeAPIjoin = async () => {
				try {
					const response = await fetch(
						apiURL + '/api/v1/games/', {
							method: 'POST',
							body: {},
							headers: { 'Content-type': 'application/json; charset=UTF-8' },
						}	
					);
					if (response.ok) {
						const newGame = await response.json();
						games.value = [...games.value, newGame];
						store.increment();
					}
				} catch (error) {
					console.error(error);
				}
			};

			return {
				games,
				consumeAPInew,
				consumeAPIjoin,
				store,	
			}
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
  
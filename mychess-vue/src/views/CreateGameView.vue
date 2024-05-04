<template>
	<div class="container">
	  <create-game :gameDataStore="gameDataStore" @newGame="consumeAPInew"/>
	</div>
</template>
  
<script>
	import CreateGame from '../components/CreateGame.vue';
	import { gameDataStore } from '../stores/gameDataStore';
	import router from '../router'




	export default {
		components: {
			CreateGame
		},
		setup() {
			const apiURL = import.meta.env.VITE_DJANGOURL;
			let gameData = null;
			const creategameDataStore = gameDataStore();


			const consumeAPInew = async () => {
				try {
					const response = await fetch(`${apiURL}/api/v1/games/`, {
						method: 'POST',
						headers: { 'Content-Type': 'application/json' },
						body: JSON.stringify({})
					});
					if (response.ok) {
						gameData = await response.json();
						creategameDataStore.setGameData(gameData); 
						console.log(creategameDataStore.gameData.id);
						console.log('Game joined or created:', gameData);
						router.push('/play');
						
					} else {
						console.error('Failed to join or create game:', response.status);
					}
				} catch (error) {
					console.error('Error in consumeAPInew:', error);
				}
			};
			return {
				consumeAPInew,
				gameData
			};
		}
	};
</script>
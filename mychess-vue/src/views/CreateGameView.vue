<template>
	<div class="container">
	  <create-game @newGame="consumeAPInew"/>
	</div>
</template>
  
<script>
	import CreateGame from '../components/CreateGame.vue';
import { useTokenStore } from '../stores/token';

	export default {
		components: {
			CreateGame
		},
		setup() {
			const apiURL = import.meta.env.VITE_DJANGOURL;
			const tokenStore = useTokenStore();
			let gameData = null;

			const consumeAPInew = async () => {
				try {
					const response = await fetch(`${apiURL}/api/v1/games/`, {
						method: 'POST',
						headers: {
							'Authorization': 'token ' + tokenStore.token, 
							'Content-Type': 'application/json' 
						},
						body: JSON.stringify({})
					});
					if (response.ok) {
						gameData = await response.json();
						localStorage.setItem('game_data', JSON.stringify(gameData)); 
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
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
			let games = null;

			const consumeAPInew = async (callback) => {
				try {
					const responseget = await fetch(`${apiURL}/api/v1/games/`, {
						method: 'GET',
						headers: {
							'Authorization': 'token ' + tokenStore.token,
							'Accept': 'application/json',
							'Content-Type': 'application/json' 
						},
					});
					if (responseget.ok){
						games = await responseget.json();
						for (const game of games) {
							console.log("Checking game:", game);
							if (game.status !== 'Finished' && (game.whitePlayer === tokenStore.user_id || game.blackPlayer === tokenStore.user_id)) {
								console.log("Active game found:", game);
								tokenStore.setGameData(game);
								callback(true);
								return;
							}
						}
						const response = await fetch(`${apiURL}/api/v1/games/`, {
							method: 'POST',
							headers: {
								'Authorization': 'token ' + tokenStore.token,
								'Accept': 'application/json',
								'Content-Type': 'application/json' 
							},
							body: JSON.stringify({})
						});
						if (response.ok) {
							gameData = await response.json();
							tokenStore.setGameData(gameData);
							console.log(gameData);
							callback(true); 
						} else {
							console.error('Failed to join or create game:', response.status);
							callback(false, response.status);
						}
					} else {
						console.error('Failed to list games:', response.status);
						callback(false, response.status);
					}
				} catch (error) {
					console.error('Error in consumeAPInew:', error);
					callback(false, error);
				}
			};
 
			return {
				consumeAPInew,
				gameData
			};
		}
	};
</script>

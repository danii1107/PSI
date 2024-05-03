<template>
	<div class="container">
	  <create-game @newGame="consumeAPInew" @joinGame="consumeAPIjoin"/>
	</div>
</template>
  
<script>
	import CreateGame from '../components/CreateGame.vue';

	export default {
		components: {
			CreateGame
		},
		setup() {
			const apiURL = import.meta.env.VITE_DJANGOURL;

			const consumeAPInew = async () => {
				try {
					const response = await fetch(`${apiURL}/api/v1/games/`, {
						method: 'POST',
						headers: { 'Content-Type': 'application/json' },
						body: JSON.stringify({})
					});
					if (response.ok) {
						const gameData = await response.json();
						console.log('Game joined or created:', gameData);
					} else {
						console.error('Failed to join or create game:', response.status);
					}
				} catch (error) {
					console.error('Error in consumeAPInew:', error);
				}
			};

			const consumeAPIjoin = async (gameID) => {
				try {
					const response = await fetch(`${import.meta.env.VITE_DJANGOURL}/api/v1/games/`, {
						method: 'POST',
						headers: { 'Content-Type': 'application/json' },
						body: JSON.stringify({ action: 'join', gameID })
					});
					if (response.ok) {
						const joinedGame = await response.json();
						console.log('Joined game:', joinedGame);
					}
				} catch (error) {
					console.error('Error joining specific game:', error);
				}
			};

			return {
				consumeAPInew,
				consumeAPIjoin
			};
		}
	};
</script>
  
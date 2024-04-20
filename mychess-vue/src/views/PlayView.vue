<template>
	<div class="container">
	  <header>
		<label>Game ID: {{ gameId }}</label>
	  </header>
  
	  <Navbar />
  
	  <div class="main-content">
		<article>
		  <section>
			<div v-if="messages.length">
				<h2>Mensajes:</h2>
				<ul>
				<li v-for="message in messages" :key="message">{{ message }}</li>
				</ul>
			</div>
		  </section>
		</article>
  
		<aside>
		  <TheChessboard :board-config="boardConfig" :player-color="playerColor" @board-created="(api) => (boardApi = api)" />
		</aside>
	  </div>
  
	  <footer>
    </footer>
	</div>
  </template>
  
  <script setup>
import { TheChessboard } from 'vue3-chessboard';
import 'vue3-chessboard/style.css';
import Navbar from '../components/Navbar.vue';
import { ref } from 'vue'; 

const playerColor = 'white';
let boardApi;

function onReceiveMove(move) {
  boardApi?.move(move);
}

const gameId = 'YourGameId';
const messages = ref([]);
const MAX_MESSAGES = 5;


const boardConfig = {
  events: {
    change: () => {
		addMessage('Something changed!');
    },
    move: (from, to, capture) => {
		addMessage(`${from} -> ${to} ${capture ? '(captura)' : ''}`);
    },
    select(key) {
		addMessage(`Square selected: ${key}`);
    },
  },
};

function addMessage(message) {
  if (messages.value.length >= MAX_MESSAGES) {
    messages.value.pop();
  }
  messages.value.unshift(message);
}
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
  

  </style>
  
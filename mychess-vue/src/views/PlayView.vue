<template>
	<div class="container">
	  <header>
		<label>Game ID: {{ gameId }}</label>
	  </header>
	
	  <Navbar />
	
	  <div class="main-content">
		<article>
		  <section>
			<div v-if="moves.length">
			  <h2>Mensajes:</h2>
			  <ul>
				<li v-for="move in moves" :key="move">{{ move }}</li>
			  </ul>
			</div>
		  </section>
		</article>
	
		<aside>
		  <TheChessboard :board-config="boardConfig" @board-created="(api) => (boardApi = api)" @draw="handleDraw" @checkmate="handleCheckmate" @stalemate="handleStalemate" @promotion="handlePromotion" />
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
  import { defineEmits } from 'vue';
  
  // Define los emisores de eventos
  const emit = defineEmits([
  'checkmate',
  'draw',     
  'stalemate', 
  'move',
  'promotion'
]);
  
  const playerColor = 'white';
  let boardApi;
  
  function onReceiveMove(move) {
	boardApi?.move(move);
  }
  
  const gameId = 'YourGameId';
  const moves = ref([]);
  const MAX_MESSAGES = 5;
  
  const boardConfig = {
	fen: 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', 
	orientation: 'white', 
	turnColor: 'white', 
	coordinates: true, 
	autoCastle: true, 
	viewOnly: false, 
	disableContextMenu: false, 
	addPieceZIndex: false,
	blockTouchScroll: false,
	highlight: {
	  lastMove: true,
	  check: true,
	},
	animation: {
	  enabled: true,
	  duration: 200,
	},
	lastMove: undefined,
	movable: {
	  free: false,
	  color: 'white',
	  showDests: true,
	  dests: {},
	  events: {},
	  rookCastle: true,
	},
	premovable: {
	  enabled: true,
	  showDests: true,
	  castle: true,
	  events: {},
	},
	predroppable: {
	  enabled: false,
	  events: {},
	},
	draggable: {
	  enabled: true,
	  distance: 3,
	  autoDistance: true,
	  showGhost: true,
	  deleteOnDropOff: false,
	},
	selectable: {
	  enabled: true,
	},
	events: {
		move: (from, to, capture) => handleMove(from, to, capture),
		checkmate: (isMated) => handleCheckmate(isMated),
		stalemate: () => handleStalemate(),
		draw: () => handleDraw(),
		promotion: (promotion) => handlePromotion(promotion)
	  },
	drawable: {
	  enabled: true,
	  visible: true,
	  defaultSnapToValidMove: true,
	  eraseOnClick: true,
	  shapes: [],
	  autoShapes: [],
	  brushes: {
		green: { key: 'g', color: '#15781B', opacity: 1, lineWidth: 10 },
		red: { key: 'r', color: '#882020', opacity: 1, lineWidth: 10 },
		blue: { key: 'b', color: '#003088', opacity: 1, lineWidth: 10 },
		yellow: { key: 'y', color: '#e68f00', opacity: 1, lineWidth: 10 },
		paleBlue: { key: 'pb', color: '#003088', opacity: 0.4, lineWidth: 15 },
		paleGreen: { key: 'pg', color: '#15781B', opacity: 0.4, lineWidth: 15 },
		paleRed: { key: 'pr', color: '#882020', opacity: 0.4, lineWidth: 15 },
		paleGrey: { key: 'pgr', color: '#4a4a4a', opacity: 0.35, lineWidth: 15 },
	  },
	},
  };
  
  function handleCheckmate(isMated) {
	addMessage(`Jaque mate, fin de la partida. ${isMated}`);
  }
  
  function handleMove(from, to, capture) {
	addMessage(`${from} -> ${to} ${capture ? '(captura)' : ''}`);
  }
  
  function handleStalemate() {
	addMessage('Tablas por ahogado');
  }
  
  function handleDraw() {
	addMessage('Empate, fin de la partida');
  }
  
  function handlePromotion(promotion) {
	addMessage(`¡Peón promovido en ${promotion.square} a la pieza ${promotion.piece}!`);
  }
  
  function addMessage(message) {
	if (moves.value.length >= MAX_MESSAGES) {
	  moves.value.pop();
	}
	moves.value.unshift(message);
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
  
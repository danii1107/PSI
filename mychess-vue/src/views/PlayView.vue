<template>
	<div class="container">
		<header>
			<label>Game ID: {{ gameId }}</label>
		</header>

		<Navbar />

		<div class="main-content">
			<article>
				<section>
					<div>
						<h2>Movimientos:</h2>
						<table>
							<thead>
								<tr>
								<th>Jugador Blanco</th>
								<th>Jugador Negro</th>
								</tr>
							</thead>
							<tbody>
								<template v-for="index in Math.max(moves.white.length, moves.black.length)">
									<tr>
									<td>{{ moves.white[index] || '' }}</td>
									<td>{{ moves.black[index] || '' }}</td>
									</tr>
								</template>
							</tbody>
						</table>
					</div>
				</section>
			</article>

			<aside>
				<TheChessboard :board-config="boardConfig" @board-created="(api) => (boardApi = api)" @draw="handleDraw" @checkmate="handleCheckmate" @stalemate="handleStalemate" @promotion="handlePromotion" @move="handleMove" />
			</aside>
		</div>

		<footer></footer>
	</div>
</template>

<script setup>
import { TheChessboard } from 'vue3-chessboard';
import 'vue3-chessboard/style.css';
import Navbar from '../components/Navbar.vue';
import { ref } from 'vue';
import { onMounted } from 'vue';
import { defineEmits } from 'vue';

const emit = defineEmits([
	'checkmate',
	'draw',
	'stalemate',
	'move',
	'promotion'
]);

let boardApi;

onMounted(() => {
	console.log(boardApi?.getBoardPosition());
});

const gameId = 'YourGameId';
const MAX_MOVES = 5;
const moves = ref({ white: [], black: [] });

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
	events: {},
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

function handleMove(move) {
	let moveText = `${move.from} --> ${move.to}`;

	if (move.captured) {
		moveText += ` (captura ${move.captured})`;
	}
	addMove(move, moveText)
}

function handleCheckmate(isMated) {
	//addMove(`Jaque mate: ${isMated}`);
	emit('checkmate', isMated);
}

function handleDraw() {
	emit('draw');
}

function handleStalemate() {
	emit('stalemate');
}

function handlePromotion(promotion) {
	let moveText = `Promoción: ${promotion.sanMove} (${promotion.promotedTo})`;
	addMove(promotion, moveText);
}


function addMove(move, text) {
  let color;
  if (move.color === 'w') {
    color = 'white';
  } else if (move.color === 'b') {
    color = 'black';
  }else{
	color = move.color;
  }

  const movesByColor = moves.value[color];
  if (movesByColor.length >= MAX_MOVES) {
    movesByColor.shift();
  }
  movesByColor.push(text);
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

<template>
	<div class="container">
		<header>
			<label>Game ID:</label>
		</header>

		<Navbar />

		<div class="main-content">
			<article>
				<section>
					<div class="table-container">
						<h2>Movimientos:</h2>
						<table class="moves-table">
							<thead>
								<tr>
								<th>Jugador Blanco</th>
								<th>Jugador Negro</th>
								</tr>
							</thead>
							<tbody>
								<template v-for="index in Math.max(moves.white.length, moves.black.length)">
									<tr>
									<td>{{ moves.white[index-1] || '' }}</td>
									<td>{{ moves.black[index-1] || '' }}</td>
									</tr>
								</template>
							</tbody>
						</table>
					</div>
					<div>
						<div v-if="materialCount !== null">
						<p>Ventaja de material: {{ materialCount }}</p>
						</div>
					</div>
                    <div v-if="gameOver">
						<p>{{ gameOverMessage }}</p>
						<button @click="restartGame">Jugar de nuevo</button>
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
import { onBeforeMount, reactive, ref } from 'vue';
import { onMounted } from 'vue';
import { defineEmits } from 'vue';
import router from '../router'
import { useTokenStore } from '../stores/token';
import { useGameStore } from '../stores/gameDataStore';



const emit = defineEmits([
	'checkmate',
	'draw',
	'stalemate',
	'move',
	'promotion'
]);

let orientationn = null;

const boardConfig = reactive({
    fen: 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',
    coordinates: true,
    orientation: orientationn,
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
            green: { key: 'g', color: '#2E8B57', opacity: 1, lineWidth: 10 },
            red: { key: 'r', color: '#B22222', opacity: 1, lineWidth: 10 },
            blue: { key: 'b', color: '#4169E1', opacity: 1, lineWidth: 10 },
            yellow: { key: 'y', color: '#FFD700', opacity: 1, lineWidth: 10 },
            paleBlue: { key: 'pb', color: '#ADD8E6', opacity: 0.5, lineWidth: 15 },
            paleGreen: { key: 'pg', color: '#90EE90', opacity: 0.5, lineWidth: 15 },
            paleRed: { key: 'pr', color: '#FFA07A', opacity: 0.5, lineWidth: 15 },
            paleGrey: { key: 'pgr', color: '#D3D3D3', opacity: 0.5, lineWidth: 15 },
        },
    },
});

let boardApi;
const materialCount = ref(null);
let gameOver = false;
let gameOverMessage = '';
let tokenStore = useTokenStore();
let gameStore = useGameStore();

onMounted(() => {
    const gameId = gameStore.id;
    if (tokenStore.user_id === gameStore.whitePlayer) {
        orientationn = 'white';
    } else if (tokenStore.user_id === gameStore.blackPlayer) {
        orientationn = 'black';
    }

    boardConfig.orientation = orientationn;
});

const MAX_MOVES = 5;
const moves = ref({ white: [], black: [] });

function handleMove(move) {
	toAddMove(move);

    let moveMessage = {
        type: 'move',
        from: move.from,
        to: move.to
    };

    if (move.promotion) {
        moveMessage.promotion = move.promotion;
    }

    //socket.send(JSON.stringify(moveMessage));

}

function toAddMove(move){
    let moveText = `${move.from} --> ${move.to}`;
	materialCount.value = boardApi?.getMaterialCount().materialDiff;

	if (move.captured) {
		moveText += ` (captura ${move.captured})`;
	}
	addMove(move, moveText)
}


function handleCheckmate(isMated) {
	gameOver = true;
	gameOverMessage = isMated ? '¡Jaque mate! El juego ha terminado.' : 'El juego ha terminado por jaque mate.';
}

function handleDraw() {
	gameOver = true;
	gameOverMessage = '¡El juego ha terminado en empate!';
}

function handleStalemate() {
	gameOver = true;
	gameOverMessage = '¡El juego ha terminado en ahogado!';
}

function handlePromotion(promotion) {
	let moveText = `Promoción: ${promotion.sanMove} (${promotion.promotedTo})`;
	addMove(promotion, moveText);
}

function restartGame() {
    //HAY QUE BORRAR EL ID DEL STORE
    router.push('/creategame');
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

.main-content > article {
    width: 70%;
    align-items: center;
}

.main-content > aside {
    width: 100%;
    align-items: center;
    justify-content: center;
}

.table-container {
    margin-top: 20px;
}

.moves-table {
    width: 100%;
    border-collapse: collapse;
    border: 2px solid #ddd;
    border-radius: 8px;
    overflow: hidden;
}

.moves-table th, .moves-table td {
    padding: 16px;
    text-align: left;
}

.moves-table th {
    background-color: #38383b;
    color: white;
}

.moves-table tbody tr:nth-child(even) {
    background-color: #464452;
	color: white;
}

.moves-table tbody tr:nth-child(odd) {
    background-color: #6a6675;
	color: white;
}

.moves-table tbody tr:hover {
    background-color: #757577;
}

.moves-table tbody td {
    border-bottom: 1px solid #ddd;
}

.material-advantage {
    font-weight: bold;
    color: #4CAF50;
    margin-top: 10px;
}
</style>

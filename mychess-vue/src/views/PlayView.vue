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
				<TheChessboard :board-config="boardConfig" :player-color="playerColor" @board-created="(api) => (boardApi = api)" @draw="handleDraw" @checkmate="handleCheckmate" @stalemate="handleStalemate" @promotion="handlePromotion" @move="handleMove" />
			</aside>
		</div>

		<footer></footer>
	</div>
</template>

<script setup>
import { defineEmits, onBeforeMount, reactive, ref } from 'vue';
import { useTokenStore } from '../stores/token';
import { TheChessboard } from 'vue3-chessboard';
import 'vue3-chessboard/style.css';
import Navbar from '../components/Navbar.vue';
import router from '../router';

// Emits definition
const emit = defineEmits([
    'checkmate',
    'draw',
    'stalemate',
    'move',
    'promotion'
]);

const boardConfig = reactive({
    fen: null,
    coordinates: true,
    orientation: null, // Will be set onMounted
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
const tokenStore = useTokenStore();
let url;
let socket;
let socketcolor;
let thiscolor;
let playerColor;

onBeforeMount(() => { 
    boardConfig.orientation = tokenStore.user_id === tokenStore.gameData.whitePlayer ? 'white' : 'black';
    boardConfig.fen = tokenStore.gameData.board_state;
    if(tokenStore.gameData.whitePlayer === tokenStore.user_id){
        socketcolor = 'b';
        thiscolor = 'w';
        playerColor = 'white'
    }else{
        socketcolor = 'w';
        thiscolor = 'b';
        playerColor = 'black'
    }
    url = `${import.meta.env.VITE_DJANGOURL}/ws/play/${tokenStore.gameData.id}/?${tokenStore.token}`;
    socket = new WebSocket(url);
    socket.onmessage = handlesocket;
});

const MAX_MOVES = 5;
const moves = ref({ white: [], black: [] });

function handlesocket(e)
{
    console.log(e.data);
    const data = JSON.parse(e.data);
    if (data.type === 'error') {
        if(data.message === "Error: invalid move (game is not active)"){
            boardConfig.fen = tokenStore.gameData.board_state;
            console.log(tokenStore.gameData.board_state);
        }
    } else if (data.type === 'move') {
        if(data.promotion != ""){
            boardApi?.move(data.from + data.to + data.promotion);
        }else{
            boardApi?.move(data.from + data.to);
        }
    }
};

function handleMove(move) {
	toAddMove(move);
    if(move.color === thiscolor){
        let moveMessage = {
            type: 'move',
            from: move.from,
            to: move.to,
            promotion: ''
        };

        if (move.promotion) {
            moveMessage.promotion = move.promotion;
        }
        socket.send(JSON.stringify(moveMessage));
    }
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

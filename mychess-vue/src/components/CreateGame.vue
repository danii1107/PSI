<template>
  <div>
    <label for="selectGame">Select game type:</label>
    <form @submit.prevent="submitForm">
      <select id="selectGame" v-model="selectedGameType" data-cy="selectGame">
        <option value="game_join_any">Join any game</option>
        <option value="Join specific game (gameID required)">Join specific game (gameID required)</option>
      </select>
      <p v-if="selectedGameType === 'Join specific game (gameID required)'" class="gameID" data-cy='gameID'>Enter gameID</p>
      <input v-if="selectedGameType === 'Join specific game (gameID required)'" type="text" v-model="gameID">
      <div class="error-message" v-if="errorMessage" data-cy="error-message">{{ errorMessage }}</div>
      <button type="submit" class="creategame" data-cy="createGame-button">Join Game</button>
    </form>
    <button data-cy="logOutLink" @click="logOut">Log Out</button>
  </div>
</template>

<script>
import { useTokenStore } from '../stores/token';
export default {
  name: "creategame",
  emits: ["newGame"],
  data() {
    return {
      selectedGameType: 'any',
      gameID: '',
      errorMessage: ''
    };
  },
  methods: {
  submitForm() {
    const tokenStore = useTokenStore();
    if (tokenStore.isAuthenticated) {
      this.errorMessage = '';
    } else {
      this.errorMessage = 'Error: Cannot create game';
      return;
    }
    if (this.selectedGameType === 'any') {
      this.$emit("newGame");
      this.$router.push('/play');
    } else if (this.selectedGameType === 'specific' && this.gameID) {
      this.$emit("newGame", this.gameID);
      this.$router.push('/play');
    } else {
      console.error('Game type selected requires additional information.');
    }
  },
  logOut() {
    this.$router.push('/log-out');
  }
}
};
</script>

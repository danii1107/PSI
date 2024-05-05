<template>
  <div>
    <label for="selectGame">Select game type:</label>
    <form @submit.prevent="submitForm">
      <select
        id="selectGame"
        v-model="selectedGameType"
        data-cy="selectGame"
      >
        <option value="game_join_any">
          Join any game
        </option>
        <option value="Join specific game (gameID required)">
          Join specific game (gameID required)
        </option>
      </select>
      <p
        v-if="selectedGameType === 'Join specific game (gameID required)'"
        class="gameID"
        data-cy="gameID"
      >
        Enter gameID
      </p>
      <input
        v-if="selectedGameType === 'Join specific game (gameID required)'"
        v-model="gameID"
        type="text"
      >
      <div
        v-if="errorMessage"
        class="error-message"
        data-cy="error-message"
      >
        {{ errorMessage }}
      </div>
      <button
        type="submit"
        class="creategame"
        data-cy="createGame-button"
      >
        Join Game
      </button>
    </form>
    <button
      data-cy="logOutLink"
      @click="logOut"
    >
      Log Out
    </button>
  </div>
</template>

<script>
import { useTokenStore } from '../stores/token';
export default {
  name: "CreateGame",
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
        setTimeout(() => {
          this.$router.push('/log-in');
        }, 250);
        return;
      }
      if (this.selectedGameType === 'game_join_any' || this.selectedGameType === 'any') {
        this.$emit("newGame", (succes, error) => {
          if (succes) {
            this.$router.push('/play');
          } else {
            console.error('Failed to join or create game:', error);
          }
        });
      } else if (this.selectedGameType === 'Join specific game (gameID required)' && this.gameID) {
        this.errorMessage = error || 'Unimplemented feature: Join specific game by gameID';
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

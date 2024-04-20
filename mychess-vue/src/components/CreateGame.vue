<template>
  <div>
    <label for="gameType">Select game type:</label>
    <form @submit.prevent="submitForm">
      <select id="gameType" v-model="selectedGameType">
        <option value="any">Join any game</option>
        <option value="specific">Join specific game</option>
      </select>
      <input v-if="selectedGameType === 'specific'" type="text" v-model="gameID" placeholder="Enter game ID">
      <button type="submit">Join Game</button>
    </form>
  </div>
</template>

<script>
  export default {
    emits: ["newGame", "joinGame"],
    data() {
      return {
        selectedGameType: 'any',
        gameID: ''
      };
    },
    methods: {
      submitForm() {
        if (this.selectedGameType === 'any') {
          this.$emit("newGame");
          console.log('Joining any game');
        } else {
          this.$emit("joinGame");
          console.log('Joining specific game with ID:', this.gameID);
        }
      }
    }
  };
</script>

<style scoped>
</style>

import { defineStore } from 'pinia';

export const useGameStore = defineStore("games", {
  state: () => ({
    whitePlayer: "",
    blackPlayer: "",
    id: "",
  }),
  actions: {
    setGameData(data) {
      this.whitePlayer = data.whitePlayer;
      this.blackPlayer = data.blackPlayer;
      this.id = data.id;
    }
  }
});
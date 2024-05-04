import { defineStore } from 'pinia';

export const gameDataStore = defineStore({
  id: 'gameData',
  state: () => ({
    gameData: null
  }),
  actions: {
    setGameData(data) {
      this.gameData = data;
    }
  }
});